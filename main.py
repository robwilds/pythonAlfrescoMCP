from server import mcp

# Import tools so they get registered via decorators
import tools.alfrescoAPI
#import tools.tylerConn

mcp.run(transport="http")
# Entry point to run the server
