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

if __name__ == "__main__":
  getTags("1a0b110f-1e09-4ca2-b367-fe25e4964a4e")