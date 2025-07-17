# main.py
from server import mcp

# Import tools so they get registered via decorators
import tools.csv_tools
import tools.parquet_tools
import tools.alfrescoAPI

# Entry point to run the server
if __name__ == "__main__":
    
    mcp.run(transport="sse")
    #print('main server running');