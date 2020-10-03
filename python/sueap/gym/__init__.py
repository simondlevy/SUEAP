'''
A superclass for working with OpenAI Gym environments in SUEAP

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import gym
import numpy as np

class _Problem:

    def __init__(self, env_name, ndims, seed=None):

        # Seed random-number generator if indicated
        if seed is not None:
            np.random.seed(seed)

        # Get observation space and action space sizes from environment
        env = gym.make(env_name)
        self.obs_size = env.observation_space.shape[0]
        self.act_size = env.action_space.shape[0] if hasattr(env.action_space, 'high') else 1

        self.seed = seed
        self.env_name = env_name

class MultiobjectiveProblem(_Problem):

    def __init__(self, env_name, ndims, seed=None):

        _Problem.__init__(self, env_name, seed)

        self.ndims = ndims

    def eval_params(self, params, episodes=10):
        '''
        Evaluates parameters for a given number of episodes
        Inputs:
            params   paramters to evaluate
            episodes number of episodes to run
        Returns: total rewards and total number of steps taken
        '''

        total_reward = np.zeros(self.ndims)
        total_steps = 0

        for _ in range(episodes):

            episode_reward, episode_steps = self.run_episode(params)

            total_reward += episode_reward
            total_steps += episode_steps

        return total_reward, total_steps

    def run_episode(self, params, render=False):

        # Build env
        env = gym.make(self.env_name)

        if self.seed is not None:
            env.seed(self.seed)

        obs = env.reset()

        episode_reward, episode_steps = self.ndims,0

        # Simulation loop
        while True:

            action = self.get_action(params, obs)

            # Optional render of environment
            if render:
                env.render()

            # Do environment step
            obs, reward, done, _ = env.step_mo(action)

            episode_reward += reward
            episode_steps += 1

            # Episode end
            if done:
                break

        # Cleanup
        env.close()

        return episode_reward, episode_steps

class Problem(_Problem):

    def __init__(self, env_name, seed=None):

        _Problem.__init__(self, env_name, seed)

    def eval_params(self, params, episodes=10):
        '''
        Evaluates parameters for a given number of episodes
        Inputs:
            params   paramters to evaluate
            episodes number of episodes to run
        Returns: total rewards and total number of steps taken
        '''

        total_reward = 0
        total_steps = 0

        for _ in range(episodes):

            episode_reward, episode_steps = self.run_episode(params)

            total_reward += episode_reward
            total_steps += episode_steps

        return total_reward, total_steps
    
    def run_episode(self, params, render=False):

        # Build env
        env = gym.make(self.env_name)

        if self.seed is not None:
            env.seed(self.seed)

        obs = env.reset()

        episode_reward, episode_steps = 0,0

        # Simulation loop
        while True:

            action = self.get_action(params, obs)

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


