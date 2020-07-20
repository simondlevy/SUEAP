#!/usr/bin/env python3
'''
Use the Neural Engineering framework to solve CartPole via an elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np
import gym

from sueap.elitist import Elitist

class NefCartPole:

    def __init__(self, n=10):

        # Encoder
        self.alpha = np.random.uniform(0, 100, n) # tuning parameter alpha
        self.b = np.random.uniform(-20,+20, n)    # tuning parameter b
        self.e = np.random.uniform(-1, +1, (4,n)) # encoder weights

        self.n = n

    def new_params(self):

       return np.random.uniform(-1, +1, (self.n,1)) # decoder weights

    def eval_params(self, params, episodes=10):

        total_reward = 0
        total_steps = 0

        for _ in range(episodes):

            episode_reward, episode_steps = self._run_episode(params)

            total_reward += episode_reward
            total_steps += episode_steps

        return total_reward, total_steps


    def mutate_params(self, params, noise_std):

        d = params

        return d+noise_std*np.random.randn(*d.shape)

    def _run_episode(self, params, env='CartPole-v0', render=False):

        # Build env
        env = gym.make(env)
        obs = env.reset()

        episode_reward, episode_steps = 0,0

        # Simulation loop
        while True:

            action = self._get_action(params, obs)

            # Optional render of environment
            if render:
                env.render()

            # Do environment step
            obs, reward, done, _ = env.step(action)

            episode_reward += reward

            # Episode end
            if done:
                break

            episode_steps += 1

        # Cleanup
        env.close()

        return episode_reward, episode_steps

    def _get_action(self, params, obs):

        a  = self._curve(obs)

        d = params

        return 1 if np.tanh(np.dot(a, d)) > 0 else 0

    def _curve(self, x):

        return NefCartPole._G(self.alpha * np.dot(x, self.e) + self.b)

    @staticmethod
    def _G(v):

        v[v<=0] = np.finfo(float).eps

        g = 10 * np.log(np.abs(v))

        g[g<0] = 0

        return  g

if __name__ == '__main__':

    e = Elitist(NefCartPole())

    best = e.run(10, max_fitness=2000)

    print(best)
