import asyncio
from server import mcp

# Import tools so they get registered via decorators
import tools.alfrescoAPI
#import tools.tylerConn

async def main():
	await mcp.run_async(transport="streamable-http", stateless_http=True)

# Entry point to run the server
if __name__ == "__main__":
	asyncio.run(main())
