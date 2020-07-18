function genomes = extract_genomes(pop)
% Returns genomes extracted from population-member data structures.  The
% latter are used internally by our NSGA-II implementation to combined
% genomes and their fitnesses, but the SuEAP API separates the genomes and 
% fitnesses for the user. 
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

for i = 1:length(pop)
    genomes{i} = pop{i}.genome;
end 




