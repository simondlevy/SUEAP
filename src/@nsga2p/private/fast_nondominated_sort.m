function F = fast_nondominated_sort(P)
% From same-named algorithm of Deb et al. (2002).
% Returns a set of non-dominated fronts F of population P,
% sorted by non-domination ranks.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% i is the front-counter and is initialized to one
i = 1;

F = {};

while ~isempty(P)
    
    % start with nobody on front
    Fi = {};
    
    % look at each fitness in the population
    for i = 1:length(P)
        
        % assume undominateded
        dominated = false;
        
        % compare it with everyone (including itself, costs less time)
        for j = 1:length(P)
            
            % if it's dominated by anyone, mark it as such and stop looking
            if dominates(P{j}, P{i})
                dominated = true;
                break
            end
            
        end
        
        % add to front if not dominated
        if ~dominated
            Fi{end+1} = P{i};
        end
        
    end

    % remove the non-dominated solutions from P
    P = remove(P, Fi);
    
    % increment the front-counter
    i = i + 1;
    
    F{end+1} = Fi;
end

