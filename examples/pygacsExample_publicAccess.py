#!/usr/bin/env python

# for compatibility with python 2.7 and 3.x
from __future__ import print_function

import sys, os, argparse
print('Python version is %s' % sys.version);
import numpy as np
from astropy.table import Table

import pygacs.public.publicAccessTools as pgp 

def main(argv):

    parser = argparse.ArgumentParser(description="This script provides a basic example of how to use pygacs for public access to GACS. It executes a custom or default ADQL query on a GACS public table and downloads the resulting table.")
    parser.add_argument('--query',  type=str, default='''SELECT * FROM public.hipparcos WHERE plx > 300; ''' , help='ADQL query string')
    parser.add_argument('--dataDir',  type=str, default='', help='path to directory for table saving')
    args = parser.parse_args(sys.argv[1:]);

    queryString = args.query;
    dataDir = args.dataDir;
    
    outputFileName = dataDir + 'ADQL_query_result.vot';
    pgp.retrieveQueryResult(queryString,outputFileName);
    T = Table.read(outputFileName,format='votable')
    print('Result table has %d rows' % len(T))
    print(T['hip','vmag','plx'])
    
if __name__ == '__main__':
    main(sys.argv[1:])    
    
sys.exit(0)




