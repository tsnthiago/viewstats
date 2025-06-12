import json
import os
import google.generativeai as genai
from config import Config
import re
import time

DRAFT_TAXONOMY_PATH = os.path.join(Config.DATA_DIR, 'draft_taxonomy.json')
CANONICAL_TAXONOMY_PATH = os.path.join(Config.DATA_DIR, 'canonical_taxonomy.json')

# --- Passada 1: Refinamento do topo ---
def get_top_level_categories(draft_taxonomy):
    return list(draft_taxonomy.keys())

def prompt_top_level_refinement(categories):
    prompt = (
        "You are an information architect. I have a list of top-level categories from a video taxonomy. "
        "Your task is to consolidate and refine this list into a final, canonical set of no more than 10 main categories.\n\n"
        "Merge semantically similar categories. For example, 'celebrity' could be merged into 'entertainment'.\n\n"
        "Return ONLY a JSON array with the final list of category names.\n\n"
        "Here is the list of categories to refine:\n---\n"
        f"{json.dumps(categories, ensure_ascii=False)}\n---"
    )
    return prompt

def call_llm(prompt, model_name=None):
    genai.configure(api_key=Config.API_KEY)
    model = genai.GenerativeModel(model_name or Config.LLM_MODEL_TAXONOMY)
    response = model.generate_content(prompt)
    return response.text

def clean_json_response(response_text):
    cleaned = re.sub(r"^```json|^```|```$", "", response_text.strip(), flags=re.MULTILINE).strip()
    return cleaned

def extract_json_from_text(text):
    # Extrai o maior bloco JSON da resposta
    matches = list(re.finditer(r'\{[\s\S]*\}', text))
    if matches:
        # Pega o maior bloco
        json_block = max((m.group(0) for m in matches), key=len)
        return json_block
    return text  # fallback: retorna o texto original

def refine_top_categories(draft_taxonomy):
    categories = get_top_level_categories(draft_taxonomy)
    prompt = prompt_top_level_refinement(categories)
    response = call_llm(prompt)
    cleaned = clean_json_response(response)
    try:
        refined = json.loads(cleaned)
    except Exception:
        print("Erro ao decodificar resposta do LLM para topo. Usando lista original.")
        refined = categories
    return refined

# --- Passada 2: Refinamento das sub-árvores ---
def prompt_subtree_refinement(category, subtree):
    prompt = (
        "You are a precise information architect. Your task is to refine the structure of the following JSON sub-tree.\n\n"
        "You must follow these rules strictly:\n"
        "1.  **DO NOT INVENT NEW TOPICS:** You must only use the topics already present in the input JSON. Do not add generic categories like 'Platforms' or 'Genres' unless they are already present.\n"
        "2.  **ALLOWED ACTIONS:** Your only allowed actions are to **merge** semantically similar nodes and **re-parent** nodes to a more logical location *within the provided sub-tree*.\n"
        "3.  **PRESERVE LEAF NODES:** The final output must contain the same set of specific, leaf-node topics (e.g., 'love is blind', 'garry's mod') as the input, just better organized.\n\n"
        "Here is an example of the task:\n\n"
        "<example_input_subtree>\n"
        "{\n  'gaming': { 'esports': { 'apex legends': null } },\n  'video games': { 'gameplay': { 'first-person shooters': null } },\n  'online video': { 'gaming content': { 'live streaming': null } }\n}\n"
        "</example_input_subtree>\n\n"
        "<example_output_subtree>\n"
        "{\n  'gaming': {\n    'esports': { 'apex legends': null },\n    'gameplay': { 'first-person shooters': null, 'live streaming': null }\n  }\n}\n"
        "</example_output_subtree>\n\n"
        "Now, refine the following sub-tree according to these rules:\n---\n"
        f"{json.dumps(subtree, ensure_ascii=False, indent=2)}\n---"
    )
    return prompt

def refine_subtree(category, subtree):
    prompt = prompt_subtree_refinement(category, subtree)
    t0 = time.time()
    response = call_llm(prompt)
    elapsed = time.time() - t0
    input_tokens = len(prompt.split())
    output_tokens = len(response.split())
    total_tokens = input_tokens + output_tokens
    # Novo cálculo de custo
    input_cost = (input_tokens / 1_000_000) * Config.LLM_TAXONOMY_INPUT_COST_PER_M
    output_cost = (output_tokens / 1_000_000) * Config.LLM_TAXONOMY_OUTPUT_COST_PER_M
    cost = input_cost + output_cost
    print(f"[REFINER] Categoria: {category} | input_tokens: {input_tokens} | output_tokens: {output_tokens} | total_tokens: {total_tokens} | custo: ${cost:.8f} | tempo: {elapsed:.2f}s")
    cleaned = clean_json_response(response)
    json_candidate = extract_json_from_text(cleaned)
    try:
        refined = json.loads(json_candidate)
    except Exception as e:
        print(f"[REFINER] Erro ao decodificar resposta do LLM para '{category}'. Usando sub-árvore original.")
        refined = subtree
    return refined, total_tokens, float(f"{cost:.8f}"), elapsed

def aggregate_subtrees_for_canonical(cat, top_categories, draft):
    """
    Para uma categoria canônica (cat), agrega todas as sub-árvores das categorias originais do draft
    que foram fundidas nela (case-insensitive, por similaridade de nome).
    """
    # Estratégia: se a categoria canônica não existir no draft, agregue todas as sub-árvores
    # cujos nomes (lower) contenham a canônica (lower) ou vice-versa, ou que sejam semanticamente próximas.
    # Para robustez, se não encontrar nada, retorna um dicionário vazio.
    matches = []
    cat_lower = cat.lower()
    for orig in draft.keys():
        orig_lower = orig.lower()
        # Critério: igualdade exata, substring, ou igualdade ignorando plural/singular
        if (
            orig_lower == cat_lower or
            cat_lower in orig_lower or
            orig_lower in cat_lower or
            orig_lower.rstrip('s') == cat_lower.rstrip('s')
        ):
            matches.append(draft[orig])
    if not matches:
        return {}
    if len(matches) == 1:
        return matches[0]
    # Agrega múltiplas sub-árvores sob a canônica
    merged = {}
    for subtree in matches:
        if isinstance(subtree, dict):
            for k, v in subtree.items():
                if k not in merged:
                    merged[k] = v
                else:
                    # Se já existe, faz um merge raso (não recursivo)
                    if isinstance(merged[k], dict) and isinstance(v, dict):
                        merged[k].update(v)
    return merged

def build_canonical_taxonomy(draft_taxonomy_path=DRAFT_TAXONOMY_PATH, canonical_taxonomy_path=CANONICAL_TAXONOMY_PATH, return_stats=False):
    print("\n[REFINER] Iniciando refinamento de taxonomia...")
    t0 = time.time()
    if not os.path.exists(draft_taxonomy_path):
        print(f"Draft taxonomy não encontrada: {draft_taxonomy_path}")
        if return_stats:
            return {"total_tokens": 0, "total_cost": 0, "total_time": 0}
        return
    with open(draft_taxonomy_path, 'r', encoding='utf-8') as f:
        draft = json.load(f)
    top_categories = refine_top_categories(draft)
    # Checkpoint: carregar progresso parcial
    canonical = {}
    if os.path.exists(canonical_taxonomy_path):
        try:
            with open(canonical_taxonomy_path, 'r', encoding='utf-8') as f:
                canonical = json.load(f)
            print(f"[REFINER] Checkpoint: {len(canonical)} categorias já refinadas serão puladas.")
        except Exception as e:
            print(f"[REFINER] Falha ao ler checkpoint, começando do zero. Erro: {e}")
            canonical = {}
    total_tokens = 0
    total_cost = 0.0
    total_time = 0
    for cat in top_categories:
        if cat in canonical:
            continue  # Pular categorias já refinadas
        subtree = aggregate_subtrees_for_canonical(cat, top_categories, draft)
        refined, tokens, cost, elapsed = refine_subtree(cat, subtree)
        canonical[cat] = refined
        total_tokens += tokens
        total_cost += cost
        total_time += elapsed
        # Salvar progresso incremental
        os.makedirs(os.path.dirname(canonical_taxonomy_path), exist_ok=True)
        with open(canonical_taxonomy_path, 'w', encoding='utf-8') as f:
            json.dump(canonical, f, ensure_ascii=False, indent=2)
    print(f"[REFINER] Refinamento concluído em {time.time()-t0:.2f}s | Total tokens: {total_tokens} | Custo estimado: ${total_cost:.8f} | Tempo total LLM: {total_time:.2f}s\n")
    if return_stats:
        return {"total_tokens": total_tokens, "total_cost": float(f"{total_cost:.8f}"), "total_time": total_time}

if __name__ == "__main__":
    build_canonical_taxonomy() 