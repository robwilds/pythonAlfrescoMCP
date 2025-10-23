import pandas as pd, json
import os
from dotenv import load_dotenv
import requests,json
from server import mcp
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from utils.queryAlfAPI import runQuery
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

BASE_URL= os.getenv("BASE_URL")
auth = os.getenv("auth")
user=os.getenv("user")
passwd=os.getenv("pass")

nodeID = []
appEntryID = []
appEntryDetails = []
appEntryDate = []
appEntryUser = []

cols = {0: 'nodeID',1:'auditEntryID',2:'entryDate',3:'details',4:'user'}

# @mcp.tool()
# def startWorkflow(type:str,assignee:str)->str:
#     """
#     This tool will start a review workflow within Alfresco.  The workflow type is the description of the request
#     for the workflow.  The assignee is who will receive the workflow.  If no assignee provided, the default is user: demo

#     Args:
#         type as string
#         assignee as string (optional)
#     Returns:
#         returns confirmation that the workflow has been started
#     """
#     return "nothing"

@mcp.tool()
def get_current_datetime():
    """
    return the date and time
    """
    current_date_time = get_current_datetime()

    print(f"The current date and time are: {current_date_time}")
    return datetime.now()


@mcp.tool()
def lockNode(nodeid:str)-> str:
    """
    use the provided id to lock a file.  The files will be locked for a maximum of 5 minutes
    Args:
        nodeid as string
    Returns:
        confirmation that the node has been locked as json response
    """
    url = os.getenv("BASE_URL") + f"""/alfresco/api/-default-/public/alfresco/versions/1/nodes/{nodeid}/lock"""
    
    body = """{
   "timeToExpire": "300",
  "type": "ALLOW_OWNER_CHANGES",
  "lifetime": "PERSISTENT"
}"""
    
    temp = requests.post(url,data=body,auth = (os.getenv("user"), os.getenv("pass"))).text
    return temp


def addTagtoNode(nodeid:str,tag:str) -> str:
    """
    use the provided id and tag to add a tag to a ndoe in Alfresco.  Tags are added one at a time
    Args:
        nodeid as string and tag as string
    Returns:
        confirmation that tag has been added as json
    """

    url = os.getenv("BASE_URL") + f"""/alfresco/api/-default-/public/alfresco/versions/1/nodes/{nodeid}/tags"""
    
    body = f"""{{
  "tag": "{tag}"
}}"""
    
    print("attempt to run addtag with url->"+url+"and body->"+body)
    temp = requests.post(url,data=body,auth = (os.getenv("user"), os.getenv("pass"))).text
    return temp

@mcp.tool()
def getAlfrescoVersion():
    """
    retrieve the current version of Alfresco Server.
    Args:
        none
    Returns:
        json containing the version of Alfresco Server.
    """
    url = os.getenv("BASE_URL") + "/alfresco/service/api/server"
    response = runQuery('get', url, '', os.getenv("user"), os.getenv("pass"))

    print("\nAlfresco System Information:")
    print(json.dumps(response, indent=2))
    return json.dumps(response, indent=2)

@mcp.tool()
def getFiles(filename: str) -> str:
    """
    Get files from Alfresco.
    Args:
        filename: The name of the file to retrieve. wildscards can be passed.
    Returns:
        A JSON string containing the file details.
    """

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/search/versions/1/search"
    #print('this is the url: '+url); 
    data = f"""{{"query": 
{{"query": "{filename}",
 "language": "afts"}}}}"""
    
    print ('the query for getFiles is: '+data)
    temp = requests.post(url,data=data,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp)
    return temp

@mcp.tool()
def getTags(nodeid: str):
    """
    Get tags for a node in Alfresco.
    Args:
        nodeid: The ID of the node to retrieve tags for.
    Returns:
        A JSON string containing the tags for the specified node. Multiple tags may be returned in a json array.  the tag field container the english value of the tag.
    """

    print('inside of gettags')

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/tags"
    #print('this is the url: '+url); 
    temp3 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp3)
    return temp3

@mcp.tool()
def getComments(nodeid: str) -> str:
    """
    Get comments for a node in Alfresco.
    Args:
        nodeid: The ID of the node to retrieve comments for.
    Returns:
        A JSON string containing the comments for the specified node. Multiple files may be returned in a json array.
    """

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/alfresco/versions/1/nodes/"+nodeid+"/comments"
    print('this is the url: '+url); 
    temp4 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp4)
    return temp4

@mcp.tool()
def getAuditApps() -> str:
    """
    Get audit apps enabled for Alfresco.
    Args:
        none
    Returns:
        A JSON string containing the audit apps with enabled status.
    """

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/alfresco/versions/1/audit-applications"
    print('this is the url: '+url); 
    temp4 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp4)
    return temp4



    date_format = "%Y-%m-%dT%H:%M:%S.%f+0000"
    local_tz = ZoneInfo("America/New_York")
    
    newDate = datetime.strptime(date,date_format)
    #print ('inside dateprocessor: '+str(newDate)) #debug

    print('local time zone '+ str(newDate.astimezone(local_tz)))

    return str(newDate.astimezone(local_tz))

@mcp.tool()
def auditForNode(nodeid):
    """
    Get audit entries for a specific node in Alfresco.
    Args:
        nodeid: The ID of the node to retrieve audit entries for.
    Returns:
        Markdown containing the audit entries for the specified node.
    """
    #now clear the temp arrays now!
    nodeID = []
    appEntryID = []
    appEntryDate = []
    appEntryDetails = []
    appEntryUser = []
    auditentryfornodeDF = pd.DataFrame(None)

    #print("node id is: "+nodeid) #debugging

    for entry in pullAuditEntryForNode(nodeid)['list']['entries']:
        #print(nodeid + '-' + str(entry['entry']['id'])) #debug

        #set the entry details and user now so there's one call
        entryDetails = pullAuditEntryDetailsForNode(entry['entry']['id'])[0]
        entryUser = pullAuditEntryDetailsForNode(entry['entry']['id'])[1]

        nodeID.append(nodeid) #this will be the same nodeid for each audit entry id
        appEntryID.append(entry['entry']['id'])
        appEntryDate.append(dateProcessor(entry['entry']['createdAt']))
        appEntryDetails.append(entryDetails) #this is coming from the pullauditdetailsentryfornode
        appEntryUser.append(entryUser) #this is coming from the pullauditdetailsentryfornode
    
    #print ("size of user array is: " + str(len(appEntryUser))) #debugging
    auditentryfornodeDF = pd.DataFrame([nodeID,appEntryID,appEntryDate,appEntryDetails,appEntryUser]).T
    auditentryfornodeDF.rename(columns=cols,inplace=True)

    print (auditentryfornodeDF)
    #auditentryfornodeDF.to_excel('auditentryfornode.xlsx')

    return auditentryfornodeDF.to_markdown()

@mcp.tool()
def auditInfo(auditApp:str):
    """
    Get all audit info based on the audit application id
    Args:
        auditApp: The ID of the audit application to retrieve audit information for.  Alfresco-access is the most common audit app id
    Returns:
        A JSON string containing the audit information for the specific audit app
    """

    url = os.getenv("BASE_URL") + f"/alfresco/api/-default-/public/alfresco/versions/1/audit-applications/{auditApp}/audit-entries?skipCount=0&omitTotalItems=false&orderBy=createdAt%20desc&maxItems=20&include=values"
    print('this is the url: '+url); 
    temp4 = requests.get(url,auth = (os.getenv("user"), os.getenv("pass"))).text
    return temp4

def pullAuditEntryForNode(nodeid):

    auditEntryforNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/nodes/'+nodeid+'/audit-entries'

    #print ('query url is: ' + auditEntryforNodeQuery) #debug
    data=runQuery('get',auditEntryforNodeQuery,'',user,passwd)
    #print ("data from nodequery returned is: " + json.dumps(data)) #debug
    return data

def pullAuditEntryDetailsForNode(auditentryid):

    auditEntryDetailsForNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/audit-applications/alfresco-access/audit-entries/'+str(auditentryid)+''

    data=runQuery('get',auditEntryDetailsForNodeQuery,'',user,passwd)

    print('data from entry detailsfornode: '+ json.dumps(data))

    #See if the actual action data can be returned
    actionDetailsForNode = data['entry']['values']['/alfresco-access/transaction/action'] #
    #actionDetailsForNode = data['entry']['values']['/alfresco-access/transaction/sub-actions']
    actionUserForNode = data['entry']['values']['/alfresco-access/transaction/user']

    return [actionDetailsForNode,actionUserForNode]

def dateProcessor(date):
    date_format = "%Y-%m-%dT%H:%M:%S.%f+0000"
    local_tz = ZoneInfo("America/New_York")
    
    newDate = datetime.strptime(date,date_format)
    #print ('inside dateprocessor: '+str(newDate)) #debug

    print('local time zone '+ str(newDate.astimezone(local_tz)))

    return str(newDate.astimezone(local_tz))