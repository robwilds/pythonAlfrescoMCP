import pandas as pd, json
import os
from dotenv import load_dotenv
import requests,json
from server import mcp
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from utils.queryAlfAPI import runQuery

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

@mcp.tool()
def getFiles(filename: str) -> str:
    """
    Get files from Alfresco.
    Args:
        filename: The name of the file to retrieve.
    Returns:
        A JSON string containing the file details.
    """

    url = os.getenv("BASE_URL") + "/alfresco/api/-default-/public/search/versions/1/search"
    #print('this is the url: '+url); 
    data = f"""{{"query": 
{{"query": "{filename}",
 "language": "afts"}}}}"""
    temp = requests.post(url,data=data,auth = (os.getenv("user"), os.getenv("pass"))).text
    print(temp)
    return temp


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

def pullAuditEntryForNode(nodeid):

    auditEntryforNodeQuery = BASE_URL + '/alfresco/api/-default-/public/alfresco/versions/1/nodes/'+nodeid+'/audit-entries'

    #print ('query url is: ' + auditEntryforNodeQuery + ' with userpass: '+ user+passwd) #debug
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