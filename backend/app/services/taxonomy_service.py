import json
import os
from threading import Lock

TAXONOMY_FILE_PATH = os.environ.get("TAXONOMY_FILE_PATH", "app/data/canonical_taxonomy.json")
_taxonomy_cache = None
_taxonomy_lock = Lock()

def load_taxonomy():
    global _taxonomy_cache
    with _taxonomy_lock:
        try:
            with open(TAXONOMY_FILE_PATH, "r", encoding="utf-8") as f:
                _taxonomy_cache = json.load(f)
        except FileNotFoundError:
            _taxonomy_cache = {}
        except Exception as e:
            _taxonomy_cache = {}
            print(f"[taxonomy_service] Failed to load taxonomy: {e}")

def get_taxonomy():
    global _taxonomy_cache
    if _taxonomy_cache is None:
        load_taxonomy()
    return _taxonomy_cache

def update_taxonomy(new_taxonomy_data: dict):
    global _taxonomy_cache
    with _taxonomy_lock:
        with open(TAXONOMY_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(new_taxonomy_data, f, ensure_ascii=False, indent=2)
        _taxonomy_cache = new_taxonomy_data 