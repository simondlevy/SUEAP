This directory contains multi-objective optimization problems from 
[Deb et al. (2002)](https://pdfs.semanticscholar.org/dc4e/c99d4201affa93f404c6b4e4f8538d07aeb5.pdf).

Each example can be used with the SGAP, MOOP, and NSGA2P algorithms.  For
example, to run the NSGA2P on the FON problem, you would type

```
  >> fon(@nsga2p, 100, 30, .7, .01)
```

where 100 = population size, 30 = number of generations, .7 = probability
of crossover, .01 = mutation rate.  When running MOOP, the .7 would be the
frontier-selection-bias parameter PHI.  

We might get better results with MOOP by also specifying its (optional) crossover 
probability, but a truly fair comparison of any algorithm against NSGA-II should
allow the specification of only two parameters.
