function P1 = find_nondominated_front(P)
% From same-named algorithm of Deb et al. (2002).  Our implementation 
% differs in detail from Deb's, but does the same O(N^2) comparisons of 
% every member of the population with every other.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License


% start with nobody on front
P1 = {};

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
        P1{end+1} = P{i};
    end
    
end
