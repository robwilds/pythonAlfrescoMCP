#Info
This project was created using this as a guide: https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed

## note: instead of using uv as package manager, I used pip

# Getting started

There's an MCP.json file for use with copilot in vscode that uses an absolute path to the main.py file. You will have to modify this absolute path for your system unless your have my exact username syntax :)

Once you open coPilot, be sure to select Agent and the LLM you'd like to use. I used claude 3.5

You should see an option to restart as a new mcp server json is found.

If you are using Claude desktop, add the following to the claude config file (via the developer section under settings)

```
{
  "mcpServers": {
    "wildsalfmcp": {
      "command": "npx",
      "args": [
      "-y",
      "mcp-remote", "http://localhost:8000/sse"]
    }
  }
}
```

note: 1) npx needs to be installed and 2) You may have to check permissions on the npm folder: sudo chown -R 501:20 "/Users/<yourusername>/.npm"

There's a docker compose yml with environment variables set. be sure to change the BASE_URL to match your alfresco endpoint

# Tools you can use

1. audit information based on nodeid
2. comments for a node based on nodeid
3. the audit apps that are configured
