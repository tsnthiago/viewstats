# Parâmetro para sobrescrever o modelo LLM padrão
# LLM_MODEL = "gemini-2.0-flash-lite"  # Altere aqui para o modelo desejado

import json
import os
from typing import Any, Set, List
import google.generativeai as genai
from config import Config

DATA_DIR = Config.DATA_DIR
DRAFT_TAXONOMY_PATH = os.path.join(DATA_DIR, 'draft_taxonomy.json')
CANONICAL_TAXONOMY_PATH = os.path.join(DATA_DIR, 'canonical_taxonomy.json')
MASTER_TAXONOMY_PATH = os.path.join(DATA_DIR, 'master_taxonomy.json')


def extract_topics_from_hierarchy(hierarchy: Any, topics: Set[str]) -> None:
    """
    Extrai recursivamente todos os nomes de tópicos de uma hierarquia aninhada.
    """
    if isinstance(hierarchy, dict):
        if 'name' in hierarchy:
            topics.add(hierarchy['name'])
        for value in hierarchy.values():
            extract_topics_from_hierarchy(value, topics)
    elif isinstance(hierarchy, list):
        for item in hierarchy:
            extract_topics_from_hierarchy(item, topics)


def aggregate_all_unique_topics(json_path: str, output_path: str) -> List[str]:
    """
    Lê o arquivo JSON de vídeos processados, extrai todos os tópicos e salva uma lista única em um arquivo de texto.
    """
    topics = set()
    with open(json_path, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    for video in videos:
        if 'main_topic' in video and video['main_topic']:
            topics.add(video['main_topic'])
        if 'topic_hierarchy' in video and video['topic_hierarchy']:
            extract_topics_from_hierarchy(video['topic_hierarchy'], topics)
    unique_topics = sorted(topics)
    with open(output_path, 'w', encoding='utf-8') as f:
        for topic in unique_topics:
            f.write(f"{topic}\n")
    print(f"Extraídos {len(unique_topics)} tópicos únicos para {output_path}")
    return unique_topics


def build_llm_prompt(topics: List[str]) -> str:
    """
    Monta o prompt para o LLM organizar os tópicos em uma taxonomia hierárquica.
    """
    prompt = (
        "You are an expert information architect and librarian. Your task is to organize a flat list of topics extracted from a large collection of YouTube videos into a single, coherent, multi-level hierarchical taxonomy.\n\n"
        "Group related topics under logical parent categories. Create parent categories where necessary. The final output must be a single JSON object.\n\n"
        "The hierarchy can be nested as deep as it makes sense.\n\n"
        "Here is the list of topics to organize:\n---\n"
        f"{chr(10).join(topics)}\n---\n\n"
        "Return ONLY the final JSON object representing the complete taxonomy.\n"
        "Example of expected output format:\n"
        "{\n  \"entertainment\": {\n    \"reality tv\": {\n      \"love is blind\": null,\n      \"kardashians\": null\n    },\n    \"talk shows\": {\n      \"steve harvey\": null\n    }\n  },\n  \"gaming\": {\n    \"gameplay\": {\n      \"apex legends\": null,\n      \"garry's mod\": null\n    },\n    \"esports\": null\n  }\n}\n"
    )
    return prompt


def call_llm(prompt: str, model_name: str = None) -> str:
    """
    Chama o LLM Gemini com o prompt fornecido e retorna a resposta (JSON da taxonomia).
    Usa o modelo definido em Config.LLM_MODEL_TAXONOMY, a não ser que model_name seja explicitamente passado.
    """
    genai.configure(api_key=Config.API_KEY)
    model = genai.GenerativeModel(model_name or Config.LLM_MODEL_TAXONOMY)
    response = model.generate_content(prompt)
    return response.text


def clean_llm_json_response(response_text: str) -> str:
    """
    Remove delimitadores de bloco de código e espaços extras do texto retornado pelo LLM.
    """
    import re
    cleaned = re.sub(r"^```json|^```|```$", "", response_text.strip(), flags=re.MULTILINE).strip()
    return cleaned


def save_master_taxonomy(taxonomy_json_str: str, output_path: str) -> None:
    """
    Salva o JSON da taxonomia mestra em arquivo, de forma legível e elegante.
    """
    cleaned_json = clean_llm_json_response(taxonomy_json_str)
    try:
        taxonomy = json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON retornado pelo LLM. Salve manualmente.")
        taxonomy = cleaned_json
    with open(output_path, 'w', encoding='utf-8') as f:
        if isinstance(taxonomy, dict):
            json.dump(taxonomy, f, ensure_ascii=False, indent=2)
        else:
            f.write(str(taxonomy))
    print(f"Taxonomia mestra salva em {output_path}")


def run_taxonomy_builder(
    canonical_taxonomy_path=CANONICAL_TAXONOMY_PATH,
    draft_taxonomy_path=DRAFT_TAXONOMY_PATH,
    master_taxonomy_path=MASTER_TAXONOMY_PATH
):
    """
    Copia a taxonomia canônica (ou draft, se não houver canônica) para master_taxonomy.json para retrocompatibilidade.
    """
    if os.path.exists(canonical_taxonomy_path):
        src = canonical_taxonomy_path
    elif os.path.exists(draft_taxonomy_path):
        src = draft_taxonomy_path
        print("Aviso: canonical_taxonomy.json não encontrado, usando draft_taxonomy.json.")
    else:
        print("Nenhuma taxonomia encontrada para salvar como master.")
        return
    with open(src, 'r', encoding='utf-8') as f:
        taxonomy = json.load(f)
    os.makedirs(os.path.dirname(master_taxonomy_path), exist_ok=True)
    with open(master_taxonomy_path, 'w', encoding='utf-8') as f:
        json.dump(taxonomy, f, ensure_ascii=False, indent=2)
    print(f"Taxonomia mestra salva em {master_taxonomy_path}")


if __name__ == "__main__":
    run_taxonomy_builder() 