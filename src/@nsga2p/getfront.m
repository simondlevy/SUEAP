function pop = getfront(nobj)
% GETFRONT  Get elite population members, sorted by non-dominance.
%
%     POP = GETFRONT(NOBJ) returns current parent population from NSGA2P
%     object NOBJ.  This population is sorted by non-dominance fronts, 
%     with the best (non-dominated) members first.  Because of the 
%     elitism in the NSGA-II algorithm, this population is guaranteed to
%     contain members not dominated by members from any previous 
%     generation.

% Our NSGA-II implementation combines each population member's genome with
% its fitness.  So in order to return just the genomes to the user, we need
% to extract them from the combined representation.

pop = extract_genomes(nobj.Pt);