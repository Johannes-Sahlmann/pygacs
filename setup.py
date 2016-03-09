#/usr/bin/env python3.5
#!/usr/bin/env python

import os
import sys
import re


# from distribute_setup import use_setuptools
# use_setuptools()

try:
    import setuptools
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()


from setuptools import find_packages

try:
  from setuptools import setup
  setup
except ImportError:
  from distutils.core import setup
  setup

# extra = {}  
# if sys.version_info >= (3,):
#     extra['use_2to3'] = True

# vre = re.compile("__version__ = \"(.*?)\"")
# m = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pygacs", "__init__.py")).read()
# pygaiaVersion = vre.findall(m)[0]

pygacsVersion = '0.2.3'

setup(
    name="pygacs",
    description="Toolkit to access and manipulate Gaia catalogue tables hosted at ESA's Gaia Archive Core Systems (GACS)",
    version=pygacsVersion,
    author="Johannes Sahlmann",
    author_email="Johannes.Sahlmann@esa.int",
    url="https://github.com/Johannes-Sahlmann/pygacs",
    license="LGPLv3+",
    long_description="\n"+open("README.rst").read() + "\n\n"    + "Changelog\n"    + "---------\n\n"    + open("HISTORY.rst").read(),
    packages = find_packages(),
    use_2to3 = True,
    # packages=['pygacs', 'pygacs.authen'],
    scripts=['examples/pygacsExample.py', 'examples/pygacsExample_publicAccess'],  # this will be installed to a bin/ directory
    package_data={'': ['LICENSE', 'AUTHORS.rst', 'HISTORY.rst', 'INSTALL', 'MANIFEST.in'],'pygacs': ['examples/*']},
    include_package_data=True,
    install_requires=["numpy","astropy","xmltodict"],
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Developers",
      "Intended Audience :: Science/Research",
      "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Topic :: Scientific/Engineering :: Astronomy",
      ],
    )
