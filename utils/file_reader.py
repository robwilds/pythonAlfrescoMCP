# utils/file_reader.py

import pandas as pd
from pathlib import Path
# Base directory where our data lives
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
def read_csv_summary(filename: str) -> str:
    """
    Read a CSV file and return a simple summary.
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)
    return f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns."
def read_parquet_summary(filename: str) -> str:
    """
    Read a Parquet file and return a detailed summary including column information.
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
    Returns:
        A string describing the file's contents including column names and types.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    columns_info = [f"\n- {col} ({df[col].dtype})" for col in df.columns]
    return f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns:{' '.join(columns_info)}"