function F = fast_nondominated_sort(P)
% From same-named algorithm of Deb et al. (2002).
% Returns a set of non-dominated fronts F of population P,
% sorted by non-domination ranks. 

% i is the front-counter and is initialized to one
i = 1;

while ~isempty(P)
    
    % find the non-dominated front
    F{i} = find_nondominated_front(P);
    
    % remove the non-dominated solutions from P
    P = remove(P, F{i});
    
    % increment the front-counter
    i = i + 1;
end

