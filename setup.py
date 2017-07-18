#!/usr/bin/env python

""" 
marcx consists mainly of a `pymarc.Record` subclass called `marcx.Record`,
that implements a few extra methods, which should ease MARC library
metadata manipulations.

Documentation and examples can be found under: https://github.com/ubleipzig/marcx
"""

from setuptools import setup

from marcx import __version__

classifiers = """
Development Status :: 4 - Beta
Intended Audience :: Education
Intended Audience :: Developers
Intended Audience :: Information Technology
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Text Processing :: General
"""


setup(name='marcx',
      version=__version__,
      description='MARC record manipulation library based on pymarc',
      long_description=__doc__,
      classifiers=filter(None, classifiers.split('\n')),
      author='Martin Czygan',
      author_email='martin.czygan@gmail.com',
      url='https://github.com/ubleipzig/marcx',
      py_modules=['marcx'],
      install_requires=['pymarc>=2.0', 'jsonpath-rw==1.3.0', 'ply==3.4', 'future>=0.16'])
