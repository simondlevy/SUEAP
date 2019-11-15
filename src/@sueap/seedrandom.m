function seedrandom(sobj, seed)
% seed the random-number generators

rand('state', seed)
randn('state', seed)