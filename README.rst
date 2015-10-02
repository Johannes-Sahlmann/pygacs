pygacs
======

**Python toolkit to manipulate Gaia catalogue tables hosted at ESA's Gaia Archive Core Systems (GACS)**

pygacs provides python modules for the access and manipulation (e.g. crossmatch) of
tables in GACS. It employs the TAP command line access tools described
in the 'Help' section of the GACS web pages (`<https://geadev.esac.esa.int/gacs-dev/index.html>`_). 

So far, only synchronous and authenticated access has been
implemented. To fully use pygacs, in particular to upload a table for
crossmatch operations, you will need to be a registered user of GACS
and call the example script with your access credentials.



Documentation
-------------

All classes and methods/functions include basic documentation. 


Installation notes
------------------

This package was developed in a python 2.7 environment.

The following python packages are required:

* `numpy <http://www.numpy.org/>`_
* `astropy <http://www.astropy.org/>`_
* `xmltodict <https://pypi.python.org/pypi/xmltodict/>`_

Optional (for plotting in the example script):

* `matplotlib <http://matplotlib.org/>`_
* `pylab <http://matplotlib.org/pylab/>`_


How to run the example script
-----------

Get the source files, e.g. 
|> git clone https://github.com/johannes-sahlmann/pygacs
|
|install pygacs
|> cd pygacs

> python setup.py install --user


To run the example script

> cd examples/

> ./pygacsExample.py --help

> ./pygacsExample.py yourGacsUserName yourGacsPassword


You may also use pip for installation:

> pip install pygacs




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
