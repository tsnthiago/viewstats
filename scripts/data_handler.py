import pandas as pd
import os
import ast
from config import Config

class DataHandler:
    @staticmethod
    def load_data(file_path: str, sample_size: int) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        if sample_size > 0 and sample_size < len(df):
            return df.sample(n=sample_size, random_state=42).reset_index(drop=True)
        return df.reset_index(drop=True)

    @staticmethod
    def prepare_data(df: pd.DataFrame, min_transcript_length: int) -> pd.DataFrame:
        def extract_full_transcript(row: pd.Series) -> str:
            try:
                transcript_data = ast.literal_eval(row['subtitles'])
                texts = [item['t'] for item in transcript_data.get('transcript', {}).get('text', [])]
                return ' '.join(texts)
            except (ValueError, SyntaxError, KeyError):
                return ""

        df['full_transcript'] = df.apply(extract_full_transcript, axis=1)
        df_clean = df[df['full_transcript'].str.len() > min_transcript_length].copy()
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        return df_clean 