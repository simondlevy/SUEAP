<img src="movie.gif" width=500>

This repository contains Matlab class libraries and example code for three kinds of evolutionary (genetic) 
algorithm:

1. The [Standard Genetic Algorithm](https://mitpress.mit.edu/books/introduction-genetic-algorithms)

2. The [NSGA-II](http://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf) algorithm for multi-objective optimization

3. [Random-Mutation Hill-Climbing](http://www.cleveralgorithms.com/nature-inspired/stochastic/hill_climbing_search.html), to use as a basic
for comparsion.



## Quickstart

1. Add SUEAP to your Matlab path (<b>Home / Set Path / Add with Subfolders ...</b>).

2. In the Matlab interpreter, run ```fon(@nsga2p, 100, 30, .7, .01)```.  This should produce a sequence of figures as
in the animation above, based on the fitness function from
[Fonseca and Fleming (1993)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.48.9077&rep=rep1&type=pdf).
