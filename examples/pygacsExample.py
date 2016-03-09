#!/usr/bin/env python

# for compatibility with python 2.7 and 3.x
from __future__ import print_function


import sys, os, argparse
print('Python version is %s' % sys.version);
import numpy as np
from astropy.table import Table
import pygacs.authen.manip as pga        



def main(argv):

    parser = argparse.ArgumentParser(description="This script provides a basic example of how to use pygacs for authenticated access to GACS. It will read an example catalogue (starlist.vot), upload it to the private area of GACS, and crossmatch it with the IGSL catalogue. The resulting table is downloaded.")

    parser.add_argument('--dataDir',  type=str, default='', help='path to directory containing starlist.vot')
    parser.add_argument('--saveFigure', type=bool, default=False, help='save figure to file')
    parser.add_argument('-t', '--tableName', type=str, default='starlist', help='user-given name in GACS of the uploaded table')
    parser.add_argument('-gt', '--gacsTableForXmatch',  type=str, default='igsl_source', help='name of GACS table for crossmatch')
    parser.add_argument('-xt', '--xmatchTableName',  type=str, default='xmatch', help='user-given name of xmatch table in GACS')
    parser.add_argument('username', type=str, help='GACS username')
    parser.add_argument('password', type=str, help='GACS password')

    args = parser.parse_args(sys.argv[1:])

    myUsername = args.username
    myPsswd = args.password

    tableName = args.tableName
    gacsTableForXmatch = args.gacsTableForXmatch
    xmatchTableName = args.xmatchTableName


    # working directory
    wDir = args.dataDir

    # read in a list of stars
    mystarFile = 'starlist.vot'
    T = Table.read(os.path.join(wDir,mystarFile),format='votable')

    ############################################################    
    # Crossmatch with Authenticated access
    ############################################################    

    tableFile = mystarFile; # the user-provided table to be uploaded 

    # get properties of all GACS tables
    # (this will write a xml file into your working directory)
    xmlFileName = os.path.join(wDir,'gacsTableProperties.xml')        

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
            print("*********************  Deleting Table")    
            pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_deleteTable(tableName) )

        if xmatchTableName in userTableNames:
            print("*********************  Deleting Table")    
            pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_deleteTable(xmatchTableName) )

    # upload user table
    print("*********************  Uploading Table")    
    pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_uploadTable(tableFile,tableName) )


    # set RA and Dec flags in user-provided table to prepare for crossmatch
    # Has to be tuned to match the names of RA and Dec columns in input table T
    print("*********************  Setting Table flags")    
    pga.authenticatedGacsCommand(myUsername,myPsswd, pga.str_setTableFlags( tableName, myUsername, T.colnames[1].lower(), T.colnames[2].lower() ))

    # command the crossmatch

    crossMatchRadius_arcsec = 1.5;
    queryString = "SELECT crossmatch_positional('user_%s','%s','public','%s','%3.2f','%s') FROM dual" % (myUsername,tableName,gacsTableForXmatch,crossMatchRadius_arcsec,xmatchTableName)
    print("*********************  Table crossmatch")     
    pga.authenticatedQuery(myUsername,myPsswd,queryString)  


    # retrieve the xmatch data (all table fields)
    # a stands for the user-provided table, b stands for the GACS reference table, c stands for the crossmatch table
    queryString = 'SELECT * FROM user_%s.%s AS a, public.%s AS b, user_%s.%s AS c WHERE (c.%s_%s_oid = a.%s_oid AND c.%s_source_id = b.source_id)' % (myUsername,tableName,gacsTableForXmatch,myUsername,xmatchTableName,tableName,tableName,tableName,gacsTableForXmatch);
    outputFileName = '%s.vot' % os.path.join(wDir,xmatchTableName);
    print("*********************  Retrieve crossmatch results")      
    pga.authenticatedQuery(myUsername,myPsswd,queryString,outputFileName,retrieve=True)

    # read crossmatched table
    T4 = Table.read( os.path.join(wDir,outputFileName) ,format='votable')

    # as an example, print the Hipparcos identifiers and the corresponding Gaia source_id for the stars in this example
    print(T4['hip','source_id'])



    # display positions and proper motions and save to file
    if args.saveFigure == 1:
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
        # pl.show(block=False)
        figName = os.path.join(wDir,'PM_input.pdf')
        pl.savefig(figName,transparent=True,bbox_inches='tight',pad_inches=0.05);


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

        figName = os.path.join(wDir,'PM_xmatch.pdf')
        pl.savefig(figName,transparent=True,bbox_inches='tight',pad_inches=0.05);

    
    
if __name__ == '__main__':
    main(sys.argv[1:])    
    
sys.exit(0)




