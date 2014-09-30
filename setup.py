# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import gvldash
version = gvldash.__version__

setup(
    name='gvldash',
    version=version,
    author='',
    author_email='nuwan.goonasekera@unimelb.edu.au',
    packages=[
        'gvldash',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['gvldash/manage.py'],
)