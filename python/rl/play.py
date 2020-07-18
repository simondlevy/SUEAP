#!/usr/bin/env python3
'''
Playback of evolved agent

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import collections
import time
import numpy as np
import os

import pickle

from lib import make_parser, run_episode

def parse_args():
    parser = make_parser()
    parser.add_argument('-m', '--model', required=True, help='Model to load')
    args = parser.parse_args()
    return args

def main():

    # Get command-line arguments
    args = parse_args()

    # Load solver
    agent, params = pickle.load(open(args.model, 'rb'))

    # Run episode and report results
    print('Reward = %.3f  Steps = %d' % run_episode(agent, params, args.env, render=True))

if __name__ == '__main__':
    main()
