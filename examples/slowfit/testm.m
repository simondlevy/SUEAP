function testm(pobj)

SEED = 0;
POPSIZE = 100;
NGEN = 10;
PHI = 0.7;
MU = 0.001;

pop = newpop('slowfit', POPSIZE, 'seed', SEED);

tic

mobj = moop(PHI, MU);

if nargin > 0
  [allpops,allfits] = run(mobj, pop, NGEN, pobj);
else
  [allpops,allfits] = run(mobj, pop, NGEN);
end


toc