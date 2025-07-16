#from queryAlf import runQuery
import pandas as pd, json
import os
from dotenv import load_dotenv
import requests,json
from server import mcp

@mcp.tool()
def getComments(nodeid: str) -> str:
    load_dotenv()
    """
    Get comments for a node in Alfresco.
    Args:
        nodeid: The ID of the node to retrieve comments for.
    Returns:
        A JSON string containing the comments for the specified node.
    """

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/comments"
    print('this is the url: '+url); 
    temp4 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp4)
    return temp4

if __name__ == '__main__':
    
    getComments("1a0b110f-1e09-4ca2-b367-fe25e4964a4e")