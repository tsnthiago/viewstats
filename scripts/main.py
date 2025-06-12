import asyncio
from dotenv import load_dotenv
import logging
from config import Config
from data_handler import DataHandler
from llm_processor import LlmProcessor
from result_handler import ResultHandler
from taxonomy_draft_builder import build_draft_taxonomy
from taxonomy_refiner import build_canonical_taxonomy
from taxonomy_builder import run_taxonomy_builder
from taxonomy_mapper import add_ids_to_taxonomy, build_path_to_id_map, map_videos_to_taxonomy
import time
import json
import requests
import os

async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    print("\n=== ViewStats Pipeline ===")
    print(f"Sample size: {Config.SAMPLE_SIZE}")
    print(f"LLM model (video extraction): {Config.LLM_MODEL_VIDEO}")
    print(f"LLM model (taxonomy): {Config.LLM_MODEL_TAXONOMY}")
    print(f"Concurrency limit: {Config.CONCURRENCY_LIMIT}")
    print(f"Input CSV: {Config.INPUT_CSV_PATH}")
    print(f"Output JSON: {Config.OUTPUT_JSON_PATH}")
    print("========================\n")

    t0 = time.time()
    print("1. Loading and preparing data...")
    t_load = time.time()
    raw_df = DataHandler.load_data(Config.INPUT_CSV_PATH, Config.SAMPLE_SIZE)
    prepared_df = DataHandler.prepare_data(raw_df, Config.TRANSCRIPT_MIN_LENGTH)
    print(f"Loaded {len(raw_df)} videos, prepared {len(prepared_df)} valid videos for processing. [Tempo: {time.time()-t_load:.2f}s]")

    if prepared_df.empty:
        print("No valid videos to process after cleaning. Exiting.")
        return

    print(f"2. Starting LLM processing for {len(prepared_df)} videos...")
    t_llm = time.time()
    processor = LlmProcessor(api_key=Config.API_KEY, model_name=Config.LLM_MODEL_VIDEO)
    llm_results = await processor.process_batch(prepared_df, Config.CONCURRENCY_LIMIT)
    total_tokens_llm = sum(r.get('total_tokens', 0) for r in llm_results if isinstance(r, dict))
    total_cost_llm = sum(r.get('llm_cost_usd', 0) for r in llm_results if isinstance(r, dict))
    print(f"LLM processing completed. [Tempo: {time.time()-t_llm:.2f}s]")

    print("3. Merging results and saving output...")
    t_merge = time.time()
    final_df = ResultHandler.process_results(prepared_df, llm_results)
    ResultHandler.save_results(final_df, Config.OUTPUT_JSON_PATH)
    print(f"Results merged and saved. [Tempo: {time.time()-t_merge:.2f}s]")

    print("4. Building draft taxonomy from processed videos...")
    t_draft = time.time()
    build_draft_taxonomy()
    print(f"Draft taxonomy built. [Tempo: {time.time()-t_draft:.2f}s]")

    print("5. Refining taxonomy with LLM (two-pass)...")
    t_refine = time.time()
    stats = build_canonical_taxonomy(return_stats=True)
    total_tokens_refine = stats.get('total_tokens', 0)
    total_cost_refine = stats.get('total_cost', 0)
    total_time_refine = stats.get('total_time', 0)
    print(f"Taxonomy refined. [Tempo: {time.time()-t_refine:.2f}s]")

    print("6. Saving master taxonomy for compatibility...")
    t_master = time.time()
    run_taxonomy_builder()
    print(f"Master taxonomy saved. [Tempo: {time.time()-t_master:.2f}s]")

    print("7. Mapping videos to canonical taxonomy (no LLM)...")
    t_map = time.time()
    CANONICAL_TAXONOMY_PATH = 'data/canonical_taxonomy.json'
    PROCESSED_VIDEOS_PATH = 'data/processed_videos.json'
    OUTPUT_MAP_PATH = 'data/video_to_taxonomy_map.json'
    with open(CANONICAL_TAXONOMY_PATH, 'r', encoding='utf-8') as f:
        canonical_taxonomy = json.load(f)
    taxonomy_with_ids = add_ids_to_taxonomy(canonical_taxonomy)
    path_to_id = build_path_to_id_map(taxonomy_with_ids)
    with open(PROCESSED_VIDEOS_PATH, 'r', encoding='utf-8') as f:
        processed_videos = json.load(f)
    video_to_taxonomy_map = map_videos_to_taxonomy(processed_videos, path_to_id)
    with open(OUTPUT_MAP_PATH, 'w', encoding='utf-8') as f:
        json.dump(video_to_taxonomy_map, f, indent=2, ensure_ascii=False)
    print(f"Video-to-taxonomy mapping saved. [Tempo: {time.time()-t_map:.2f}s] ({len(video_to_taxonomy_map)} vídeos mapeados)")

    print("8. Indexando vídeos no Qdrant...")
    t_index = time.time()
    from indexer import prepare_dataframe, index_to_qdrant_async
    from qdrant_client import QdrantClient
    print(f"Usando embeddings OpenAI: {Config.EMBEDDING_MODEL_OPENAI}")
    client = QdrantClient(url=Config.QDRANT_URL)
    import pandas as pd
    df = prepare_dataframe(processed_videos, video_to_taxonomy_map)
    await index_to_qdrant_async(df, client, Config.QDRANT_COLLECTION_NAME)
    print(f"Indexação Qdrant concluída. [Tempo: {time.time()-t_index:.2f}s] ({len(df)} vídeos indexados)")

    # Enviar taxonomia final para o endpoint externo
    API_URL = "http://147.79.111.195:8000/taxonomy/upload"
    API_KEY = os.getenv("INTERNAL_API_KEY")
    taxonomy_path = 'data/canonical_taxonomy.json'
    if API_KEY:
        print("Enviando taxonomia final para o endpoint externo...")
        try:
            with open(taxonomy_path, 'rb') as f:
                files = {'taxonomy_file': f}
                headers = {'X-Internal-API-Key': API_KEY}
                response = requests.post(API_URL, files=files, headers=headers)
            if response.status_code == 200:
                print("Upload da taxonomia concluído com sucesso!")
            else:
                print(f"Falha no upload da taxonomia. Status: {response.status_code}. Resposta: {response.text}")
        except Exception as e:
            print(f"Erro ao enviar taxonomia: {e}")
    else:
        print("INTERNAL_API_KEY não definida. Pulei o upload da taxonomia.")

    print(f"\nPipeline completed in {time.time()-t0:.2f} seconds.")
    print("\n=== RELATÓRIO FINAL ===")
    print(f"Tokens LLM processamento vídeos: {total_tokens_llm}")
    print(f"Tokens LLM refinamento taxonomia: {total_tokens_refine}")
    print(f"Tokens totais: {total_tokens_llm + total_tokens_refine}")
    print(f"Custo LLM processamento vídeos: ${total_cost_llm:.8f}")
    print(f"Custo LLM refinamento taxonomia: ${total_cost_refine:.8f}")
    print(f"Custo total LLM: ${total_cost_llm + total_cost_refine:.8f}")
    print(f"Tempo total refinamento taxonomia: {total_time_refine:.2f}s")
    print("=======================\n")

if __name__ == "__main__":
    asyncio.run(main())