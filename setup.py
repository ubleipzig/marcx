#!/usr/bin/env python

from distutils.core import setup
from marcx import __version__ as version

setup(name='marcx',
      version=version,
      description='Marc Record Utility',
      author='Martin Czygan',
      author_email='martin.czygan@gmail.com',
      url='https://github.com/miku/marcx',
      py_modules=['marcx'],
      install_requires=['pymarc>=2.0', 'pyisbn>=0.6'])