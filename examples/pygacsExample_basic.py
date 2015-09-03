"""
This script provides a basic example of how to use pygacs for authenticated access to GACS.
It will read an example catalogue (starlist.vot), upload it to the private area of GACS, and crossmatch it with the IGSL catalogue.
The resulting table is downloaded.

For the relative paths to work, please run this script in the "examples/" directory.

IMPORTANT:
Save your GACS access credentials in a simple text file named
pygacs.config and located in the 'configPath'.See pygacs.config.template for format. It is simple text.
This separate configuration file is required to avoid uploading user credentials to github.


"""



import sys,os
import numpy as np
from astropy.table import Table


sys.path.append("../")


# for development only
if 0 == 1:
    if ('pygacs' in sys.modules):
        import pygacs.authen.manip
        reload(pygacs.authen.manip);

# import pygacs manip        
import pygacs.authen.manip as pga        


# read in username and password stored in configuration file
configPath = '../../'
configData = Table.read(configPath + 'pygacs.config', format='ascii.basic',data_start=0)
myUsername = configData[0][0]
myPsswd = configData[1][0]


print "*********************"    

showPlots = 1;

# read in a list of stars
mystarFile = 'starlist.vot'
T = Table.read(mystarFile,format='votable')

# display positions and proper motions
if showPlots==1:
    import pylab as pl
    pl.close('all');
    
    pl.figure(figsize=(8, 3),facecolor='w', edgecolor='k'); pl.clf();
    pl.subplot(1,2,1)
    pl.plot(T['RA_ICRS_'],T['DE_ICRS_'],'bo',ms=5)
    pl.xlabel('RA (deg)')
    pl.ylabel('Dec (deg)')
    pl.axis('equal')
    pl.subplot(1,2,2)
    pl.plot(T['pmRA'],T['pmDE'],'ro',ms=5)
    pl.xlabel('PM in RA (mas/yr)')
    pl.ylabel('PM in Dec (mas/yr)')
    pl.axis('equal')
    pl.tight_layout()
    pl.title('Input catalogue')
    pl.show()
    
############################################################    
# Crossmatch with Authenticated access
############################################################    
       
tableFile = mystarFile; # the user-provided table to be uploaded 

tableName = 'starlist'; # user-given name of this table in GACS

gacsTableForXmatch = 'igsl_source'; # name of GACS table for crossmatch

xmatchTableName = 'xmatch'; # user-given name of xmatch table in GACS
                    
# get properties of all GACS tables
# (this will write a xml file into your working directory)
xmlFileName = 'gacsTableProperties.xml'        

tableProps = pga.GacsTableProperties( myUsername, myPsswd, xmlFileName )
tableProps.printSchemaNames()

# get and print available table in a specific schema
publicTableNames = tableProps.getTableNames('public',verbose=0)

# the user's schema name
userSchemaName = 'user_%s' % myUsername

# check whether user table or xmatch table already exist in GACS. if yes delete them
if userSchemaName in tableProps.schemaNames:
    userTableNames = tableProps.getTableNames(userSchemaName,verbose=1)
    
    if tableName in userTableNames:
        print "*********************  Deleting Table"    
        pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_deleteTable(tableName) )
    
    if xmatchTableName in userTableNames:
        print "*********************  Deleting Table"    
        pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_deleteTable(xmatchTableName) )
     
# upload user table
print "*********************  Uploading Table"    
pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_uploadTable(tableFile,tableName) )
                
        
# set RA and Dec flags in user-provided table to prepare for crossmatch
# Has to be tuned to match the names of RA and Dec columns in input table T
print "*********************  Setting Table flags"    
pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_setTableFlags( tableName, myUsername, T.colnames[1].lower(), T.colnames[2].lower() ))

# command the crossmatch

crossMatchRadius_arcsec = 2.0;
queryString = "SELECT crossmatch_positional('user_%s','%s','public','%s','%3.2f','%s') FROM dual" % (myUsername,tableName,gacsTableForXmatch,crossMatchRadius_arcsec,xmatchTableName)
print "*********************  Table crossmatch"     
pga.authenticatedQuery(myUsername,myPsswd,queryString)  


# retrieve the xmatch data (all table fields)
# a stands for the user-provided table, b stands for the GACS reference table, c stands for the crossmatch table
queryString = 'SELECT * FROM user_%s.%s AS a, public.%s AS b, user_%s.%s AS c WHERE (c.%s_%s_oid = a.%s_oid AND c.%s_source_id = b.source_id)' % (myUsername,tableName,gacsTableForXmatch,myUsername,xmatchTableName,tableName,tableName,tableName,gacsTableForXmatch);
outputFileName = '%s.vot' % xmatchTableName;
print "*********************  Retrieve crossmatch results"      
pga.authenticatedQuery(myUsername,myPsswd,queryString,outputFileName,retrieve=True)

# read crossmatched table
T4 = Table.read(outputFileName,format='votable')

# as an example, print the Hipparcos identifiers and the corresponding Gaia source_id for the stars in this example
print T4['hip','source_id']

# print all available columns
# print T4.colnames

# display positions and proper motions
if showPlots==1:
    pl.figure(figsize=(8, 3),facecolor='w', edgecolor='k'); pl.clf();
    pl.subplot(1,2,1)
    pl.plot(T4['alpha'],T4['delta'],'bo',ms=5)
    pl.xlabel('RA (deg)')
    pl.ylabel('Dec (deg)')
    pl.axis('equal')
    pl.subplot(1,2,2)
    pl.plot(T4['mu_alpha'],T4['mu_delta'],'ro',ms=5)
    pl.xlabel('PM in RA (mas/yr)')
    pl.ylabel('PM in Dec (mas/yr)')
    pl.axis('equal')
    pl.tight_layout()
    pl.title('GACS catalogue (%s)' % gacsTableForXmatch)
    pl.show()
    
    
    
    
    
sys.exit(0)




