# server.py

from fastmcp import FastMCP
import asyncio
# This is the shared MCP server instance

mcp = FastMCP("Alfresco MCP Server by RobW",host="0.0.0.0",log_level="DEBUG",stateless_http=True,)