function I = crowding_distance_assignment(I)
% From same-named algorithm of Deb et al. (2002).
% Attaches crowding distances to population members in I.

% number of solutions in I
L = length(I);

% initialize distance
for i = 1:L
    I{i}.distance = 0;
end

% number of objectives, taken arbitrarily from first member
M = length(I{1}.fitness);

% for each objective m
for m = 1:M
    
    % sort using each objective value
    I = sortdim(I, m);
    
    % so that boundary points are always selected
    I{1}.distance = Inf;
    I{L}.distance = Inf;
    
    % for all other points, assign distance equal to absolute difference
    % in function values of two adjacent solutions
    for i = 2:L-1
        I{i}.distance = I{i}.distance + (I{i+1}.fitness(m) - I{i-1}.fitness(m));
    end
    
end



