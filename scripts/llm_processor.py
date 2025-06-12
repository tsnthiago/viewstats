import re
import json
import logging
import google.generativeai as genai
from typing import Dict, Any, List
from config import Config
from tqdm.asyncio import tqdm
import asyncio
import time
import os

class LlmProcessor:
    def __init__(self, api_key: str, model_name: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def build_prompt(self, video_data: Dict[str, Any]) -> str:
        prompt_template = f"""
<instructions>
You are an expert agent specialized in extracting structured information from video data.
Your task is to analyze the video content and return a single, rich, valid JSON object.

The JSON object must contain the following keys:
- description: A summarized, detailed description of the video content (max 250 tokens).
- named_entities: An array of objects, each with 'name' and 'type', for all relevant entities (people, organizations, products).
- intention: The main purpose of the video (e.g., "Tutorial", "Product Review", "Entertainment").
- hierarchical_topics: An array of strings representing the main hierarchical topics. Generate up to 3 paths. Each path should go from a broad category to a specific subtopic, using ' > ' as a separator.

RULES:
1.  **Output Format:** You MUST return ONLY a single, valid JSON object. No other text or explanations.
2.  **Case:** All generated text (categories, topics, etc.) MUST be in lower case, EXCEPT for the 'name' value in 'named_entities'.
3.  **Topic Abstraction:** Hierarchical topics should be general and reusable categories, not specific events or details from a single video.
4.  **Consistency:** The paths in 'hierarchical_topics' should be logically consistent with each other.
</instructions>

<example_input>
Video Title: "How to Build a Gaming PC in 2024"
Video Description: "A full walkthrough of picking parts, assembling, and optimizing performance."
Video Transcript: "...we begin with choosing the right CPU for gaming and content creation..."
</example_input>

<example_output>
{{
  "description": "a comprehensive guide on building a gaming pc in 2024, covering part selection like cpus, assembly process, and performance optimization.",
  "named_entities": [
    {{"name": "Intel", "type": "brand"}},
    {{"name": "Nvidia", "type": "brand"}}
  ],
  "intention": "educational tutorial",
  "hierarchical_topics": [
    "technology > hardware > pc building",
    "gaming > equipment > custom builds"
  ]
}}
</example_output>

<video_data>
Video Title: {video_data.get('title', '')}
Video Description: {video_data.get('description', '')}
Video Transcript: {video_data.get('full_transcript', '')[:Config.TRANSCRIPT_MAX_CHARS]}
</video_data>
"""
        return prompt_template

    def clean_json_response(self, response_text: str) -> Dict[str, Any]:
        try:
            cleaned_text = re.sub(r"```json|```", "", response_text).strip()
            data = json.loads(cleaned_text)
            return data
        except json.JSONDecodeError:
            return {"error": "JSON parsing failed", "raw_response": response_text}

    async def process_single_video(self, video_data: Dict[str, Any], semaphore: asyncio.Semaphore) -> Dict[str, Any]:
        async with semaphore:
            prompt = self.build_prompt(video_data)
            t0 = time.time()
            try:
                response = await self.model.generate_content_async(prompt)
                elapsed = time.time() - t0
                usage = getattr(response, 'usage_metadata', None)
                input_tokens = getattr(usage, 'prompt_token_count', 0) if usage else 0
                output_tokens = getattr(usage, 'candidates_token_count', 0) if usage else 0
                total_tokens = getattr(usage, 'total_token_count', 0) if usage else (input_tokens + output_tokens)
                # Novo cálculo de custo
                input_cost = (input_tokens / 1_000_000) * Config.LLM_VIDEO_INPUT_COST_PER_M
                output_cost = (output_tokens / 1_000_000) * Config.LLM_VIDEO_OUTPUT_COST_PER_M
                cost = input_cost + output_cost
                logging.info(f"yt_id={video_data['yt_id']} | input_tokens={input_tokens} | output_tokens={output_tokens} | total_tokens={total_tokens} | cost=${cost:.8f} | elapsed={elapsed:.2f}s")
                parsed_json = self.clean_json_response(response.text)
                return {
                    "yt_id": video_data['yt_id'],
                    **parsed_json,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "llm_cost_usd": float(f"{cost:.8f}"),
                    "llm_input_cost_usd": float(f"{input_cost:.8f}"),
                    "llm_output_cost_usd": float(f"{output_cost:.8f}"),
                    "llm_elapsed_sec": elapsed
                }
            except Exception as e:
                logging.error(f"yt_id={video_data['yt_id']} | error={str(e)}")
                return {"yt_id": video_data['yt_id'], "error": str(e)}

    async def process_batch(self, df, concurrency_limit: int) -> List[Dict[str, Any]]:
        print(f"\n[LLM] Iniciando processamento batch com sample_size={len(df)}, modelo={self.model.model_name}, concurrency={concurrency_limit}")
        t_batch = time.time()
        semaphore = asyncio.Semaphore(concurrency_limit)
        # Checkpoint: carregar resultados já processados
        processed_path = os.path.join('data', 'processed_videos.json')
        processed = []
        processed_ids = set()
        if os.path.exists(processed_path):
            try:
                with open(processed_path, 'r', encoding='utf-8') as f:
                    processed = json.load(f)
                processed_ids = {v['yt_id'] for v in processed if 'yt_id' in v}
                print(f"[LLM] Checkpoint: {len(processed_ids)} vídeos já processados serão pulados.")
            except Exception as e:
                print(f"[LLM] Falha ao ler checkpoint, processando tudo do zero. Erro: {e}")
                processed = []
                processed_ids = set()
        # Filtrar df para só processar vídeos não processados
        to_process = df[~df['yt_id'].isin(processed_ids)]
        results = []
        if len(processed) > 0:
            # Processamento incremental: vídeo a vídeo
            for _, row in to_process.iterrows():
                res = await self.process_single_video(row, semaphore)
                results.append(res)
                # Salvar incrementalmente
                all_results = processed + results
                try:
                    with open(processed_path, 'w', encoding='utf-8') as f:
                        json.dump(all_results, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"[LLM] Falha ao salvar checkpoint incremental: {e}")
            all_results = processed + results
            total_tokens = sum(r.get('total_tokens', 0) for r in all_results if isinstance(r, dict))
            total_cost = sum(r.get('llm_cost_usd', 0) for r in all_results if isinstance(r, dict))
            print(f"[LLM] Batch (com checkpoint) concluído em {time.time()-t_batch:.2f}s | Total tokens: {total_tokens} | Custo estimado: ${total_cost:.8f}")
            return all_results
        else:
            # Processamento batch normal
            tasks = [self.process_single_video(row, semaphore) for index, row in df.iterrows()]
            results = await tqdm.gather(*tasks, desc="Processing Videos")
            with open(processed_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            total_tokens = sum(r.get('total_tokens', 0) for r in results if isinstance(r, dict))
            total_cost = sum(r.get('llm_cost_usd', 0) for r in results if isinstance(r, dict))
            print(f"[LLM] Batch concluído em {time.time()-t_batch:.2f}s | Total tokens: {total_tokens} | Custo estimado: ${total_cost:.8f}")
            return results

    async def process_batch_stream(self, df, concurrency_limit: int):
        """
        Processa vídeos um a um, yieldando cada resultado assim que estiver pronto.
        Permite controle de erros consecutivos e interrupção imediata.
        """
        print(f"\n[LLM] Iniciando processamento batch (stream) com sample_size={len(df)}, modelo={self.model.model_name}, concurrency={concurrency_limit}")
        semaphore = asyncio.Semaphore(concurrency_limit)
        processed_path = os.path.join('data', 'processed_videos.json')
        processed = []
        processed_ids = set()
        if os.path.exists(processed_path):
            try:
                with open(processed_path, 'r', encoding='utf-8') as f:
                    processed = json.load(f)
                processed_ids = {v['yt_id'] for v in processed if 'yt_id' in v}
                print(f"[LLM] Checkpoint: {len(processed_ids)} vídeos já processados serão pulados.")
            except Exception as e:
                print(f"[LLM] Falha ao ler checkpoint, processando tudo do zero. Erro: {e}")
                processed = []
                processed_ids = set()
        to_process = df[~df['yt_id'].isin(processed_ids)]
        results = []
        for _, row in to_process.iterrows():
            try:
                res = await self.process_single_video(row, semaphore)
                results.append(res)
                # Salvar incrementalmente
                all_results = processed + results
                try:
                    with open(processed_path, 'w', encoding='utf-8') as f:
                        json.dump(all_results, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"[LLM] Falha ao salvar checkpoint incremental: {e}")
                yield res
            except Exception as e:
                err = {"yt_id": row.get('yt_id', None), "error": str(e)}
                results.append(err)
                yield err 