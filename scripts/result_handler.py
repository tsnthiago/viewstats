import pandas as pd
from typing import List, Dict, Any
from config import Config
import numpy as np

class ResultHandler:
    @staticmethod
    def process_results(df: pd.DataFrame, llm_results: List[Dict[str, Any]]) -> pd.DataFrame:
        df_results = pd.DataFrame(llm_results)
        # Renomear a coluna 'description' do LLM para 'description_llm' se existir
        if 'description' in df_results.columns:
            df_results = df_results.rename(columns={'description': 'description_llm'})
        # Supondo que 'title' é a coluna problemática
        if 'title' in df_results.columns:
            df_results = df_results.drop(columns=['title'])
        # Only keep basic columns and LLM results, drop transcript and subtitles
        basic_cols = ['yt_id', 'title', 'description']
        # Find which basic columns exist in df
        available_basic_cols = [col for col in basic_cols if col in df.columns]
        # Merge only on the basic columns and LLM results
        df_basic = df[available_basic_cols].copy()
        df_merged = pd.merge(df_basic, df_results, on="yt_id", how="left")
        # Garantir unicidade das colunas
        if df_merged.columns.duplicated().any():
            before = list(df_merged.columns)
            _, idx = np.unique(df_merged.columns, return_index=True)
            df_merged = df_merged.iloc[:, sorted(idx)]
            after = list(df_merged.columns)
            removed = set(before) - set(after)
            print(f"[ResultHandler] Colunas duplicadas removidas: {removed}")
        return df_merged

    @staticmethod
    def save_results(df: pd.DataFrame, file_path: str):
        df.to_json(file_path, orient='records', indent=2)
        print(f"Successfully processed and saved {len(df)} videos to {file_path}") 