"""
Tools to query GACS using non-authenticated and synchronous access.

Some example capabilities are:
- send a query to GACS and retrieve the resulting table

References
----------

Compiled on the basis of the 'Help' section of the GACS web pages,
located at http://archives.esac.esa.int/gaia/ 


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

############################################################    
# Non authenticated access
############################################################    
    
import httplib
import urllib
import time, sys
from xml.dom.minidom import parseString
# import pdb

__version__ = '0.2'


def retrieveQueryResult(queryString,outputFileName):
    #ASYNCHRONOUS REQUEST
    
    host = "gea.esac.esa.int"
    pathinfo = "/tap-server/tap/async"
    port = 80
    
    #-------------------------------------
    #Create job

    params = urllib.urlencode({\
        "REQUEST": "doQuery", \
        "LANG":    "ADQL", \
        "FORMAT":  "votable", \
        "PHASE":   "RUN", \
        "QUERY":   queryString
        })
    
    headers = {\
        "Content-type": "application/x-www-form-urlencoded", \
        "Accept":       "text/plain" \
        }

    connection = httplib.HTTPConnection(host, port)
    connection.request("POST",pathinfo,params,headers)

    #Status
    response = connection.getresponse()
    print("Status: " +str(response.status), "Reason: " + str(response.reason));

    #Server job location (URL)
    location = response.getheader("location")
    print("Location: " + location)

    #Jobid
    jobid = location[location.rfind('/')+1:]
    print("Job id: " + jobid);

    connection.close()

    #-------------------------------------
    #Check job status, wait until finished

    while True:
        connection = httplib.HTTPConnection(host, port)
        connection.request("GET",pathinfo+"/"+jobid)
        response = connection.getresponse()
        data = response.read()
        #XML response: parse it to obtain the current status
        dom = parseString(data)
        phaseElement = dom.getElementsByTagName('uws:phase')[0]
        phaseValueElement = phaseElement.firstChild
        phase = phaseValueElement.toxml()
        print("Status: " + phase);
        #Check finished
        if phase == 'COMPLETED': break
        if phase == 'ERROR':            
            # query = dom.getElementsByTagName('uws:parameter')[2].firstChild.toxml()
            message = dom.getElementsByTagName('uws:message')[0].firstChild.toxml()
            # print phaseElement
            # pdb.set_trace()
            break

        #wait and repeat
        time.sleep(1.0)


    connection.close()

    if phase == 'ERROR':
        print('ERROR');
        print(message);
        sys.exit(1)
    
    #-------------------------------------
    #Get results
    connection = httplib.HTTPConnection(host, port)
    connection.request("GET",pathinfo+"/"+jobid+"/results/result")
    response = connection.getresponse()
    data = response.read()
    if sys.version_info >= (3,):
        outputFile = open(outputFileName, 'wb')
    else:
        outputFile = open(outputFileName, 'w')
    outputFile.write(data)
    outputFile.close()
    connection.close()
    print("Data saved in: " + outputFileName)
            