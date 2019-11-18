<img src="movie.gif" width=500>

This repository contains a Matlab class library and example code for a few kinds of evolutionary (genetic) 
algorithm:

1. The [Standard Genetic Algorithm](https://mitpress.mit.edu/books/introduction-genetic-algorithms)

2. The [NSGA-II](http://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf) algorithm for multi-objective optimization

3. [Random-Mutation Hill-Climbing](http://www.cleveralgorithms.com/nature-inspired/stochastic/hill_climbing_search.html), to use as a baseline for comparsion

4. A &ldquo;homebrew&rdquo; Multi-Objective Optimization algorithm that I devloped before learning about
NSGA-II

The library supports parallel fitness evaluation (on multi-core or cluster machines).

## Quickstart

1. Add SUEAP to your Matlab path (<b>Home / Set Path / Add with Subfolders ...</b>).

2. In the Matlab interpreter, run ```fon(@nsga2p, 100, 30, .7, .01)```.  This should produce a sequence of figures as
in the animation above, based on the fitness function from
[Fonseca and Fleming (1993)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.48.9077&rep=rep1&type=pdf).

## Parallel fitness evaluation

To try out parallel fitness evaluation, you should first download, install, and test the
[PECON](https://github.com/simondlevy/PECON) repository.  Then take a look at the 
[testm](https://raw.githubusercontent.com/simondlevy/SUEAP/master/examples/slowfit/testm.m) script to see 
how to run fitness evaluation in parallel.
