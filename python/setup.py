#!/usr/bin/env python3

'''
Python distutils setup file for sueap module.

Copyright (C) 2020 Simon D. Levy

MIT License
'''

#from distutils.core import setup
from setuptools import setup

setup (name = 'sueap',
    version = '0.1',
    install_requires = ['numpy'],
    description = 'Suite of Evolutionary Algorithms in Parallel',
    packages = ['sueap', 'sueap.algorithms', 'sueap.algorithms.nsga2', 'sueap.algorithms.elitist', 'sueap.gym'],
    author='Simon D. Levy',
    author_email='simon.d.levy@gmail.com',
    url='https://github.com/simondlevy/sueap',
    license='MIT',
    platforms='Linux; Windows; OS X'
    )
