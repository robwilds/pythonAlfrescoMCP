# Info

This project was created using this guide: https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed

```diff
- note: instead of using uv as package manager, I used pip
```

# Getting started

## Running locally

### be sure node and npm are installed. I used node 20.18.3 and npm 10.8.2

Running pip3 install -r requirements.txt will get the required sister modules installed.

use the .envtemplate file to create a .env file. The BASE_URL is the url to your Alfresco install.

Now run with python3 main.py. You will see a confirmation that the MCP server is running.

There's an MCP.json file for use with copilot in vscode that uses an absolute path to the main.py file. You will have to modify the absolute path for your system unless your have my exact username syntax :)

Once you open CoPilot, be sure to select Agent and the LLM you'd like to use. I used claude 3.5

You should see an option to restart as a new mcp server json is found.

If you are using Claude desktop, add the following to the claude config file (via the developer section under settings)

```
{
  "mcpServers": {
    "wildsalfmcp": {
      "command": "npx",
      "args": [
      "-y",
      "mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```

Once your chat interface is setup you can ask away

### note

1. npx needs to be installed and
2. You may have to check permissions on the npm folder: sudo chown -R 501:20 "/Users/<yourusername>/.npm"
3. The url to the mcp server (mcp-remote) can be changed to match your IP or wherever the mcp service is running

## Running via docker

There's a docker compose yml with environment variables set. be sure to change the BASE_URL to match your alfresco endpoint

If you would like to have a fully built yaml that includes alfresco community, use this link: https://github.com/robwilds/community25.x

Clone the entire repo then run docker compose up -d

# Tools you can use

1. audit information based on nodeid
2. comments for a node based on nodeid
3. the audit apps that are configured
4. fetch document info by name...this will return nodeid
5. current alfresco version
6. get tag information for a document based on nodeid
