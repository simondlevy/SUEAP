#!/usr/bin/env python3
'''
Reinforcement learning using a genetic algorithm

'Adapted from https://github.com/PacktPublishing/Deep-Reinforcement-Learning-Hands-On-Second-Edition/blob/master/Chapter20/03_cartpole_ga.py

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import collections
import time
import numpy as np
import os

import multiprocessing as mp

import pickle

from lib import make_parser, run_episode

from nef import NefAgent as Agent

# Workers use named tuple to send results back to main
WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'reward', 'steps'])

# =====================================================================================================================

# Worker code

def evaluate(agent, params, env, episodes):

    total_reward = 0
    total_steps = 0

    for _ in range(episodes):

        episode_reward, episode_steps = run_episode(agent, params, env)

        total_reward += episode_reward
        total_steps += episode_steps

    return total_reward, total_steps


def worker_func(worker_id, cmdargs, main_to_worker_queue, worker_to_main_queue):

    # Loop over generations, getting parent param dictionaries from main process and mutating to get new population
    for _ in range(cmdargs.max_gen):
        parents = main_to_worker_queue.get()
        if len(parents) == 0:
            break
        for solver in parents:
            agent, params = solver
            reward, steps = evaluate(agent, params, cmdargs.env, cmdargs.max_evals)
            worker_to_main_queue.put(WorkerToMainItem(params=params, reward=reward, steps=steps))

# =====================================================================================================================

def report(population, parents_count, gen_idx, batch_steps, t_start):

    rewards = [p[1] for p in population[:parents_count]]
    speed = batch_steps / (time.time() - t_start)
    print('%04d: reward_mean=%+6.2f\treward_max=%+6.2f\treward_std=%6.2f\tspeed=%d f/s' % (
        gen_idx, np.mean(rewards), np.max(rewards), np.std(rewards), int(speed)))


def get_new_population(worker_to_main_queue, parents_per_worker, workers_count):

    batch_steps = 0
    population = []
    pop_size = parents_per_worker * workers_count
    while len(population) < pop_size:
        out_item = worker_to_main_queue.get()
        population.append((out_item.params, out_item.reward))
        batch_steps += out_item.steps
    return population, batch_steps


def setup_workers(cmdargs, agent, workers_count, parents_per_worker):

    main_to_worker_queues = []
    worker_to_main_queue = mp.Queue(workers_count)
    workers = []
    for k in range(workers_count):
        main_to_worker_queue = mp.Queue()
        main_to_worker_queues.append(main_to_worker_queue)
        w = mp.Process(target=worker_func, args=(k, cmdargs, main_to_worker_queue, worker_to_main_queue))
        workers.append(w)
        w.start()
        main_to_worker_queue.put([(agent, agent.new_params()) for _ in range(parents_per_worker)])

    return main_to_worker_queues, worker_to_main_queue, workers

def update_workers(population, main_to_worker_queues, parents_per_worker, parents_count):

    for main_to_worker_queue in main_to_worker_queues:

        # Select the fittest parents
        parents = [population[np.random.randint(parents_count)] for _ in range(parents_per_worker)]

        # Send them to workers
        main_to_worker_queue.put(parents)

def halt_workers(main_to_worker_queues):

    for main_to_worker_queue in main_to_worker_queues:

        main_to_worker_queue.put([])

def make_save_path(name):

    save_path  = None
    if name is not None:
        save_path = os.path.join('saves', '%s' % name)
        os.makedirs(save_path, exist_ok=True)
    return save_path

def parse_args():

    parser = make_parser()

    parser.add_argument('--name', required=True, help='Name of the run for saving')
    parser.add_argument('--noise-std', type=float, default=0.01)
    parser.add_argument('--pop-size', type=int, default=2000)
    parser.add_argument('--parents-count', type=int, default=10)
    parser.add_argument('--max-gen', default=None, type=int, help='Maximum number of generations, default=inf')
    parser.add_argument('--max-evals', default=10, type=int, help='Maximum number of evaluations, default=10')
    parser.add_argument('--max-reward', default=None, type=float, help='Maximum reward before halting, default=None')

    args = parser.parse_args()

    # Get command-line args
    # Default to infinite generations
    if args.max_gen is None:
        args.max_gen = np.iinfo(np.uint32).max

    return args

def save_best(save_path, params, reward, best_reward, agent):
    if best_reward is None or reward > best_reward:
        name = 'best_%+.3f.dat' % reward
        fname = os.path.join(save_path, name)
        pickle.dump((agent,params), open(fname, 'wb'))
        print('Saved '  + fname)
    return reward # Reward never goes down

def main():

    # Get command-line arguments
    args = parse_args()

    # Make save directory if indicated
    save_path = make_save_path(args.name)

    # A single agent will be used to evaluate new parameters
    agent = Agent()

    main_to_worker_queues = []
    # Use all available CPUs, distributing the population equally among them
    workers_count = mp.cpu_count()
    parents_per_worker = args.pop_size // workers_count

    # Set up communication with workers
    main_to_worker_queues, worker_to_main_queue, workers = setup_workers(args, agent, workers_count, parents_per_worker)

    # This will store the fittest individual in the population and its reward
    best = None
    best_reward = None

    # Loop for specified number of generations (default = inf)
    for gen_idx in range(args.max_gen):

        # Start timer for performance tracking
        t_start = time.time()

        # Get results from workers
        population, batch_steps = get_new_population(worker_to_main_queue, parents_per_worker, workers_count)

        # Keep the current best in the population
        if best is not None:
            population.append(best)

        # Sort population by reward (fitness)
        population.sort(key=lambda p: p[1], reverse=True)

        # Report and store current state
        report(population, args.parents_count, gen_idx, batch_steps, t_start)

        # Get new best
        best = population[0]

        # Save best if it's better than previous
        if save_path is not None:
            best_reward = save_best(save_path, best[0], best[1], best_reward, agent)

        # Mutate the learnable parameters for each individual in the population
        population = [(agent, agent.mutate_params(p[0], args.noise_std)) for p in population]

        # Quit if maximum reward reached
        if args.max_reward is not None and best_reward >= args.max_reward:
            halt_workers(main_to_worker_queues)
            break

        # Send new population to wokers
        update_workers(population, main_to_worker_queues, parents_per_worker, args.parents_count)

    # Shut down workers after waiting a little for them to finish
    time.sleep(0.25)
    for w in workers:
        w.join()

if __name__ == '__main__':
    main()
