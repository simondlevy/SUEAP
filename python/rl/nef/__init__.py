'''
A simple agent for reinforcement learning using the Neural Engineering Framework

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

class NefAgent:

    def __init__(self, n=10):

        # Encoder
        self.alpha = np.random.uniform(0, 100, n) # tuning parameter alpha
        self.b = np.random.uniform(-20,+20, n)    # tuning parameter b
        self.e = np.random.uniform(-1, +1, (4,n)) # encoder weights

        self.n = n

    def new_params(self):

       return np.random.uniform(-1, +1, (self.n,1)) # decoder weights

    def get_action(self, params, obs):

        a  = self._curve(obs)

        d = params

        return 1 if np.tanh(np.dot(a, d)) > 0 else 0

    def mutate_params(self, params, noise_std):

        d = params

        return d+noise_std*np.random.randn(*d.shape)

    def _curve(self, x):

        return NefAgent._G(self.alpha * np.dot(x, self.e) + self.b)

    @staticmethod
    def _G(v):

        v[v<=0] = np.finfo(float).eps

        g = 10 * np.log(np.abs(v))

        g[g<0] = 0

        return  g
