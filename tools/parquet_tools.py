# tools/parquet_tools.py

from server import mcp
from utils.file_reader import read_parquet_summary
@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows and columns, along with column names and types.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's dimensions and column information.
    """
    return read_parquet_summary(filename)