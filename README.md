# Info

This project was created using this guide: https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed

```diff
- note: instead of using uv as package manager, I used pip
```

# Getting started

## Running locally

### be sure node and npm are installed. I used node 20.18.3 and npm 10.8.2

Running pip3 install -r requirements.txt will get the required modules installed.

use the .envtemplate file to create a .env file. The BASE_URL is the url to your Alfresco install. Make sure the credentials are correct as well

Now run with python3 main.py. You will see a confirmation that the MCP server is running.

If you are using Claude desktop, add the following to the claude config file (via the developer section under settings)

```
{
  "mcpServers": {
    "alfrescomcp": {
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

1. npx needs to be installed to run locally...and....
2. You may have to check permissions on the npm folder: sudo chown -R 501:20 "/Users/<yourusername>/.npm"
3. The url to the mcp server (http streaming) can be changed to match your IP or wherever the mcp service is running. Keep in mind: local chat clients like claude will require https to access the mcp server remotely (not on localhost). You will need to use https instead of http. There are self signed certificates created automatically

## Running via docker

1.  To run the container standalone, you can build a container locally (dockerfile is in the root of the project). This creates the container image in your local docker repository. There's a docker compose yml with environment variables set. be sure to change the BASE_URL and credentials to match your alfresco endpoint

If you would like to have a fully built yaml that includes alfresco community, use this link: https://github.com/robwilds/community25.x

Clone the entire aforementioned repo then run docker compose up -d

# Tools you can use

1. Audit information based on nodeid
2. Comments for a node based on nodeid
3. The audit apps that are configured
4. Fetch document info by name...this will return nodeid
5. Current alfresco version
6. Get tag information for a document based on nodeid
7. Add a tag to a node
8. Add comments to a node
