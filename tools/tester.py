from dotenv import load_dotenv
import requests,os

load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")
user=os.getenv("user")


def getTags(nodeid):
    """
    Get tags for a node in Alfresco.
    Args:
        nodeid: The ID of the node to retrieve tags for.
    Returns:
        A JSON string containing the tags for the specified node. Multiple tags may be returned in a json array.
    """

    print('inside of gettags')

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/tags"
    #print('this is the url: '+url); 
    temp3 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp3)
    return temp3

def addTagtoNode(nodeid:str,tag:str):
    """
    with the current nodeid, add a tag.  Tags are added one at a time
    Args:
        nodeid,tag
    Returns:'
        confirmation that tag has been added.  a simple yes or no
    """

    url = os.getenv("BASE_URL") + f"""/alfresco/api/-default-/public/alfresco/versions/1/nodes/{nodeid}/tags"""
    
    body = f"""{{
  "tag": "{tag}"
}}"""
    
    print("attempt to run addtag with url->"+url+"and body->"+body)
    temp = requests.post(url,data=body,auth = (os.getenv("user"), os.getenv("pass"))).text
    return temp

if __name__ == "__main__":
  addTagtoNode("1a0b110f-1e09-4ca2-b367-fe25e4964a4e","yes")