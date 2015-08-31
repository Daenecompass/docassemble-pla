#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(name='docassemble.pla_forms',
      version='0.1',
      description=('A docassemble extension.'),
      author='Jonathan Pyle',
      author_email='jhpyle@gmail.com',
      license='MIT',
      url='http://docassemble.org',
      packages=find_packages(),
      namespace_packages = ['docassemble'],
      zip_safe = False,
      package_data={'docassemble.pla_forms': ['data/templates/*', 'data/questions/*', 'data/static/*']},
     )

