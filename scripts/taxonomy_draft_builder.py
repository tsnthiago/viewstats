import json
import os
from collections import defaultdict
from config import Config

DRAFT_TAXONOMY_PATH = os.path.join(Config.DATA_DIR, 'draft_taxonomy.json')
PROCESSED_VIDEOS_PATH = Config.OUTPUT_JSON_PATH

def insert_path(taxonomy, path):
    parts = [p.strip() for p in path.split('>')]
    current = taxonomy
    for part in parts:
        if part not in current:
            current[part] = {}
        current = current[part]


def build_draft_taxonomy(processed_videos_path=PROCESSED_VIDEOS_PATH, draft_taxonomy_path=DRAFT_TAXONOMY_PATH):
    if not os.path.exists(processed_videos_path):
        print(f"Arquivo não encontrado: {processed_videos_path}")
        return
    with open(processed_videos_path, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    taxonomy = {}
    for video in videos:
        paths = video.get('hierarchical_topics') or []
        for path in paths:
            insert_path(taxonomy, path)
    # Converter dicts vazios para null
    def clean(d):
        return {k: clean(v) if v else None for k, v in d.items()}
    taxonomy = clean(taxonomy)
    os.makedirs(os.path.dirname(draft_taxonomy_path), exist_ok=True)
    with open(draft_taxonomy_path, 'w', encoding='utf-8') as f:
        json.dump(taxonomy, f, ensure_ascii=False, indent=2)
    print(f"Draft taxonomy salva em {draft_taxonomy_path}")

if __name__ == "__main__":
    build_draft_taxonomy() 