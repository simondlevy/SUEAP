function combos = exhaust(lims, mincmbs, filter)
% EXHAUST   Generate a grid of parameter combinations for exhaustive search.
%
%     COMBOS = EXHAUST(LIMS, MINCMBS) generates a minimum of MINCMBS
%     regularly spaced combinations of values constrained by LIMS.  LIMS
%     is an Nx2 matrix whose rows are the lower and upper limits for
%     exploring the N dimensions of the solution.
%
%     COMBOS = EXHAUST(LIMS, MINCMBS, FILTER) accepts a handle to a
%     function that filters out illegal combinations.

ndims = size(lims, 1);

% keep refining grid until we have enough legal solutions
for gridsize = 2:Inf
    
    % generate all possible values along each dimension
    vals = [];
    for j = 1:ndims
        vals(j,:) = linspace(lims(j, 1), lims(j, 2), gridsize);
    end    
    
    % pre-allocate empty solutions for efficiency
    maxsols = gridsize^ndims;
    combos = zeros(maxsols, ndims);
    okay = ones(maxsols, 1);
    
    % generate all possible solutions
    for i = 1:maxsols
                
        % convert single combination index into array of indices
        n = i-1;
        for j = 1:ndims
            indices(j) = mod(n, gridsize) + 1;
            n = fix(n/gridsize);
        end
        
        % generate possible solutions
        for j = 1:ndims
            combos(i, j) = vals(j,indices(j));
        end
                
    end
    
    % filter out impossible solutions if indicated
    if nargin > 2
        for i = 1:maxsols
            if filter(combos(i,:))
                okay(i) = 0;
            end
        end
    end
    
    % if we have enough possible solutions, we're done
    if sum(okay) >= mincmbs, break, end
        
end

% return only okay solutions
combos = combos(find(okay), :);