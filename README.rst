pygacs
======

**Python toolkit to manipulate Gaia catalogue tables hosted at ESA's Gaia Archive Core Systems (GACS)**

pygacs provides python modules for the access and manipulation of
tables in GACS, e.g. basic query on a single table or crossmatch between two tables. It employs the TAP command line access tools described
in the 'Help' section of the GACS web pages (`<http://gaia.esac.esa.int/archive/>`_). 

Both public and authenticated access have been
implemented.

Please see pygacsExample_publicAccess.py for a demo on how public tables can easily be queried using ADQL.

To fully use pygacs, in particular to upload a table for
crossmatch operations, you will need to be a registered user of GACS
and call the example script pygacsExample.py with your access credentials.



Documentation
-------------

All classes and methods/functions include basic documentation. 


Installation notes
------------------

This package was developed in a python 2.7 environment, but was also
successfully tested using python 3.5.

The following python packages are required:

* `numpy <http://www.numpy.org/>`_
* `astropy <http://www.astropy.org/>`_
* `xmltodict <https://pypi.python.org/pypi/xmltodict/>`_

Optional (for plotting in the example script):

* `matplotlib <http://matplotlib.org/>`_
* `pylab <http://matplotlib.org/pylab/>`_


How to run the example script
-----------

You may use pip for installation:

> pip install pygacs

Or get the source files, e.g.: 

> git clone https://github.com/johannes-sahlmann/pygacs

Install pygacs:

> cd pygacs

> python setup.py install --user

To run the example script, do:

> cd examples/

For public access:

> ./pygacsExample_publicAccess.py

For authenticated access:

> ./pygacsExample.py --help

> ./pygacsExample.py yourGacsUserName yourGacsPassword





Attribution
-----------

Please acknowledge the ESA Science Archives Team and the Gaia Data
Processing and Analysis Consortium (DPAC) if you used this code in your
research.

License
-------

Copyright (c) 2015 Johannes Sahlmann, Gaia Data Processing and Analysis Consortium

pygacs is open source and free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see `<http://www.gnu.org/licenses/>`_.
