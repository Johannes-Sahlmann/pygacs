"""
Tools to allow manipulating tables in GACS using authenticated and synchronous access.

Some example capabilities are:
- send a command to GACS
- upload a user table
- delete a user table
- query the progress of a job submitted to GACS
- retrieve the results of a job 
- set the flags of a user table
- retrieve the properties of GACS tables (public and user)


References
----------

Compiled on the basis of the 'Help' section of the GACS web pages,
see http://archives.esac.esa.int/gaia/


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, subprocess, time, sys
import xmltodict
import numpy as np
import pdb

__version__ = '0.2'

gacsurl = 'http://gea.esac.esa.int/'


def authenticatedGacsCommand(myUsername,myPsswd,commandString):
    """
    Send a command to GACS using Authenticated access
    
    Parameters
    ----------
    myUsername : string
        user name
    myPsswd : string
        password
    commandString : string
        string to be sent to GACS
    
    """    
    str_login = "curl -k -c cookies.txt -X POST -d username=%s -d password=%s -L \"%stap-server/login\" " % (myUsername,myPsswd,gacsurl)
    # print str_login
    str_logout = "curl -k -b cookies.txt -X POST -d -L \"%stap-server/logout\" " % (gacsurl)   

    os.system(str_login)
    os.system(commandString)
    os.system(str_logout)
        
def str_progress(jobid):
    """
    Return string to query progress of a job
    
    Parameters
    ----------
    jobid : string
        ID of the job

    """
    
    return "curl -k -b cookies.txt \"%stap-server/tap/async/%s\" "  % (gacsurl,jobid)
          
def str_retrieve(jobid,outFile):
    """
    Return string to retrieve result of a job in a file
    
    Parameters
    ----------
    jobid : string
        ID of the job
    outFile : string
        filename containing result

    """
    return "curl -k -b cookies.txt \"%stap-server/tap/async/%s/results/result\" > %s" % (gacsurl,jobid,outFile)
    
def authenticatedQuery(myUsername,myPsswd,queryString,outputFileName="out.vot", retrieve=False):        
    """
    Send a query to GACS using Authenticated access and check for progress
    
    Parameters
    ----------
    myUsername : string
        user name
    myPsswd : string
        password
    queryString : string
        string to be sent to GACS
    outputFileName : string, optional
        file to write results to
    retrieve : {True, False}
        flag to trigger result retrieval via file
    
    """
        
    str_login = "curl -k -c cookies.txt -X POST -d username=%s -d password=%s -L \"%stap-server/login\" " % (myUsername,myPsswd,gacsurl)                 
    str_query = "curl -k -b cookies.txt -i -X POST --data \"PHASE=run&LANG=ADQL&REQUEST=doQuery&QUERY=" + queryString + "\"  \"%stap-server/tap/async\" " % (gacsurl)                       
    str_logout = "curl -k -b cookies.txt -X POST -d -L \"%stap-server/logout\" " % (gacsurl)   
    
    os.system(str_login)
    resp = subprocess.check_output(str_query, shell=True)    
    if sys.version_info >= (3,): # tested on python 3.5
        jobid = str(resp).split('tap-server/tap/async/')[1].split('\\r')[0]
    else:    
        jobid = resp.split('tap-server/tap/async/')[1].split('\r')[0]
    
    
    # check for progress    
    while True:
        resp = subprocess.check_output(str_progress(jobid), shell=True)
        if sys.version_info >= (3,): # tested on python 3.5
            phase = str(resp).split('<uws:phase>')[1].split('</uws:phase>')[0];
        else:
            phase = resp.split('<uws:phase>')[1].split('</uws:phase>')[0]
        print("Status: " + phase);
        if phase == 'ERROR':
            print('error encountered');
            print(resp)
            break
        elif phase == 'COMPLETED':
            # retrieve result
            if retrieve:
                resp = subprocess.check_output(str_retrieve(jobid,outputFileName), shell=True)                
            break        
        time.sleep(1.0)
                    
    os.system(str_logout)

    

def str_deleteTable(tableName):
    """
    Return string used to delete table
    
    Parameters
    ----------
    tableName : string
        name of table to delete

    """
    return "curl -k -b cookies.txt -X POST -F TABLE_NAME=%s -F DELETE=TRUE -F FORCE_REMOVAL=TRUE \"%stap-server/Upload\"" % (tableName,gacsurl)

def str_uploadTable(tableFile,tableName):
    """
    Return string used to upload table
    
    Parameters
    ----------
    tableFile : string
        name of file to upload
    tableName : string
        name of table to upload

    """
    return  "curl -k -b cookies.txt -X POST -F FILE=@%s -F TABLE_NAME=%s \"%stap-server/Upload\"" % (tableFile,tableName,gacsurl)

def str_setTableFlags(tableName, myUsername,  ra_column_name, dec_column_name ):
    """
    Return string used to set table flags
    
    Parameters
    ----------
    tableName : string
        name of table
    myUsername : string
        user name in GACS
    ra_column_name : string
        name of RA column in the table
    dec_column_name : string
        name of Dec column in the table
    
    """
    return "curl -k -b cookies.txt -X POST \"%stap-server/TableTool?ACTION=radec&TABLE_NAME=user_%s.%s&RA=%s&DEC=%s\"" % ( gacsurl, myUsername, tableName, ra_column_name,dec_column_name)
            
    
                
    
class GacsTableProperties:    
    """
    A class to query properties of tables in GACS

    Attributes
    ----------
    myUsername : string
        user name
    myPsswd : string
        password
    xmlFileName : string
        filename used to write file on disk

    Methods
    -------
    printSchemaNames()
        prints names of availabe schemas
    getTableNames(schemaName,verbose=0):
        return table names of a certain schema
    """

    
    def __init__(self, myUsername, myPsswd, xmlFileName): 
        self.myUsername = myUsername;
        self.myPsswd = myPsswd;
        self.xmlFileName = xmlFileName;

        comstr = "curl -k -b cookies.txt -X POST -L \"%stap-server/tap/tables\" > %s" % (gacsurl,xmlFileName)
        authenticatedGacsCommand(myUsername,myPsswd, comstr )
        with open(xmlFileName) as fd:
            d = xmltodict.parse(fd.read())

        # dictionary containing the table properties
        self.d = d    
        self.Nschema = len(self.d['vod:tableset']['schema']);
        self.schemaNames = np.array([np.str(self.d['vod:tableset']['schema'][i]['name']) for i in range(self.Nschema)])

            
    def printSchemaNames(self):
        """
        Print the GACS schema names to stdout
    
        """

        print('Available schemas:')
        for nam in self.schemaNames:
            print(nam);

                  
    def getTableNames(self,schemaName,verbose=0):
        """
        Return the table names corresponding to a certain schema
    
        Parameters
        ----------
        schemaName : string
           name of schema to query
        verbose : int {0 ,1}
           flag to trigger printing of table names
        
        Returns
        -------
        tableNames : string array
           empty if schema does not have any table
           
        """
             
        schemaIndex = np.where(self.schemaNames == schemaName)[0][0]
        try:
            Ntables = len(self.d['vod:tableset']['schema'][schemaIndex]['table'])        
            tableNames = np.array([ self.d['vod:tableset']['schema'][schemaIndex]['table'][i]['name'] for i in range(Ntables)])
            if verbose:
                print('Available tables in schema %s:' % schemaName);
                for nam in tableNames:
                    print(nam);
        except KeyError:
            print('Schema %s does not contain any table' % schemaName);
            tableNames = np.array(['']);
                        
        return tableNames
