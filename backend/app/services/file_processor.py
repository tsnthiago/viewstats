import pandas as pd
import io


def process_csv_file(file_bytes: bytes):
    try:
        df = pd.read_csv(io.StringIO(file_bytes.decode('utf-8')))
        return {
            "rows": len(df),
            "columns": list(df.columns)
        }
    except Exception as e:
        raise ValueError(f"Error processing CSV: {str(e)}")