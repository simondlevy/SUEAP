function e = fpselect(pop, wheel)
% select element of population member using fitness-proportional roulette wheel

e = pop(pickrand(wheel));
