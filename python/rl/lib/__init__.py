'''
Common code for sueap/python/rl

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import argparse
import gym

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--env', default='CartPole-v0', help=('Environment id, default=CartPole-v0'))
    return parser


def run_episode(agent, params, env, render=False):

    # Build env
    env = gym.make(env)
    obs = env.reset()

    episode_reward, episode_steps = 0,0

    # Simulation loop
    while True:

        action = agent.get_action(params, obs)

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



