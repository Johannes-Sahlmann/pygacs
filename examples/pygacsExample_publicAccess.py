#!/usr/bin/env python

# for compatibility with python 2.7 and 3.x
from __future__ import print_function

import sys, os, argparse
print('Python version is %s' % sys.version);
from astropy.table import Table

import pygacs.public.publicAccessTools as pgp 

def main(argv):

    parser = argparse.ArgumentParser(description="This script provides a basic example of how to use pygacs for public access to GACS. It executes a custom or default ADQL query on a GACS public table and downloads the resulting table.")
    parser.add_argument('--query',  type=str, default='''SELECT * FROM gaiadr1.gaia_source WHERE parallax > 200; ''' , help='ADQL query string')
    parser.add_argument('--dataDir',  type=str, default='', help='path to directory for table saving')
    parser.add_argument('--output_file',  type=str, default=None, help='file for saving the query result. Format is VOTable.')
    args = parser.parse_args(argv)

    queryString = args.query
    dataDir = args.dataDir
    output_file = args.output_file

    if output_file is not None:
        outputFileName = output_file
    else:
        outputFileName = dataDir + 'ADQL_query_result.vot'
    pgp.retrieveQueryResult(queryString,outputFileName)
    T = Table.read(outputFileName,format='votable')
    print('Result table has %d rows' % len(T))
    T.pprint()
    # print(T['source_id', 'ra', 'dec'])
    
if __name__ == '__main__':
    main(sys.argv[1:])    
    
sys.exit(0)




