#!/usr/bin/env python3

'''
Python distutils setup file for nsga2 module.

Copyright (C) 2020 Simon D. Levy

MIT License
'''

#from distutils.core import setup
from setuptools import setup

setup (name = 'sueap',
    version = '0.1',
    install_requires = ['numpy'],
    description = 'Suite of Evolutionary Algorithms in Parallel',
    packages = ['sueap', 'sueap.nsga2'],
    author='Simon D. Levy',
    author_email='simon.d.levy@gmail.com',
    url='https://github.com/simondlevy/sueap',
    license='MIT',
    platforms='Linux; Windows; OS X'
    )
