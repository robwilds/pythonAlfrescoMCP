from server import mcp

# Import tools so they get registered via decorators
import tools.alfrescoAPI

mcp.run(transport="sse")
# Entry point to run the server
