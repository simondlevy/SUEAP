#!/usr/bin/env python3
'''
Use the Neural Engineering framework to solve Pendulum via an elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np
import gym

from sueap.elitist import Elitist

class NefPendulum:

    def __init__(self, neurons=20):

        # Encoder
        self.alpha = np.random.uniform(0, 100, neurons) # tuning parameter alpha
        self.b = np.random.uniform(-20,+20, neurons)    # tuning parameter b
        self.e = np.random.uniform(-1, +1, (3,neurons)) # encoder weights

        self.neurons = neurons

    def new_params(self):

       return np.random.uniform(-1, +1, (self.neurons,1)) # decoder weights

    def eval_params(self, params, episodes=10):

        total_reward = 0
        total_steps = 0

        for _ in range(episodes):

            episode_reward, episode_steps = self.run_episode(params)

            total_reward += episode_reward
            total_steps += episode_steps

        return total_reward, total_steps


    def mutate_params(self, params, noise_std):

        d = params

        return d+noise_std*np.random.randn(*d.shape)

    def run_episode(self, params, env='Pendulum-v0', render=False):

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
            episode_steps += 1

            # Episode end
            if done:
                break

        # Cleanup
        env.close()

        return episode_reward, episode_steps

    def _get_action(self, params, obs):

        a  = self._curve(obs)

        d = params

        return np.clip(np.dot(a, d), -2, +2)

    def _curve(self, x):

        return NefPendulum._G(self.alpha * np.dot(x, self.e) + self.b)

    @staticmethod
    def _G(v):

        v[v<=0] = np.finfo(float).eps

        g = 10 * np.log(np.abs(v))

        g[g<0] = 0

        return  g

if __name__ == '__main__':

    problem = NefPendulum()

    ga = Elitist(problem, 2000)

    best = ga.run(80, max_fitness=2000)

    print('Got reward %.3f in %d steps' % problem.run_episode(best, render=True))

