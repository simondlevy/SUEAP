function [newpop, obj] = update(obj, pop, fits, gen, ngen)
% A harness for NSGA-II.  XXX Perhaps we should have SuEAP build fitnesses
% into population members, because it is so useful to have them together
% in this and other GA's.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% pre-process: put genomes and fitnesses into data structures
for i = 1:length(pop)
    Qt{i} = makemember(i, pop{i}, fits{i});
end

% Run NSGA-II, returning and storing fitness of next parent population.  
% Parent population is initially empty.
[obj.Pt{end+1}, Qt] = nsga_ii(obj, gen, ngen, obj.Pt{end}, Qt);

% post-process: extract next-pop genomes from data structures
newpop = extract_genomes(Qt);
