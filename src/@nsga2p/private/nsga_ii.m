function [Pt1, Qt1] = nsga_ii(obj, gen, ngen, Pt, Qt)
% Implements the NSGA-II algorithm of Deb et al. (2002).  Accepts
% current parent population Pt (initially empty) and child population Qt 
% and returns next-generation parent and child populations Pt1, Qt1.  Each 
% member of a population contains its genotype, fitness, and a unique
% index. We also pass in a SuEAP object and the count of current and
% total generations, in order to take advantage of SuEAP methods and do
% additional compuations.

% our goal is to get N members into Pt1
N = length(Qt);

% combine parent and child populations
Rt = popunion(Pt, Qt);

% F = (F_1, F_2, ...), all non-dominated fronts of Rt
F = fast_nondominated_sort(Rt);

% next parent population initially empty
Pt1 = {};

% till next parent population is filled
for i = 1:length(F)
    
    % calcuate crowding distance in F_i
    F{i} = crowding_distance_assignment(F{i});
  
    % XXX: include each member's rank along with its genome and fitness
    F{i} = add_ranks(F{i}, i);
    
    % stop when parent population is filled
    if length(Pt1) + length(F{i}) > N, break, end    
        
    % include i-th non-dominated front in the parent pop
    Pt1 = popunion(Pt1, F{i});
    
end

% sort in descending order using <_n (crowding distance metric)
F{i} = sortdist(F{i});

% choose the first (N - |P_{t+1}|) elements of F_i
Pt1 = popunion(Pt1, {F{i}{1:N-length(Pt1)}});

% use selection, crossover, and mutation to create a new population Q_{t+1}
Qt1 = make_new_pop(obj, Pt1, gen, ngen);

% bonus: visualize sorted fronts if indicated
if ~isempty(obj.visdims)
    plotfronts(F, obj.visdims, obj.vislims, gen, ngen);
end

