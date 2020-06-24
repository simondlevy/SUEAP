function F = fast_nondominated_sort(P)
% From same-named algorithm of Deb et al. (2002).
% Returns a set of non-dominated fronts F of population P,
% sorted by non-domination ranks.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% empty fronts lists to start
F = {};

while ~isempty(P)
    
    % start with nobody on front
    Fi = {};
    
    % look at each fitness in the population
    for i = 1:length(P)
        
        p = P{i};
        
        % assume undominateded
        dominated = false;
        
        % compare it with everyone (including itself, costs less time)
        for j = 1:length(P)
            
            q = P{j};
            
            % if it's dominated by anyone, mark it as such and stop looking
            if dominates(q, p)
                dominated = true;
                break
            end
            
        end
        
        % add to front if not dominated
        if ~dominated
            Fi{end+1} = p;
        end
        
    end

    % remove the non-dominated solutions from P
    P = remove(P, Fi);
    
    F{end+1} = Fi;
end

