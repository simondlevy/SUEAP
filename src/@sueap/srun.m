function [allpops,allfits,sobj] = srun(sobj, pop, ngen, varargin)
% SRUN should be called by your implementing class (MOOP, SGAP, ...).  SRUN
% takes care of the parallel fitness evaluation and then calls the UPDATE
% function of the implementing class.

% grab defaults
[pobj,init,haltfun,savegen,savename]  = getopts(sobj, varargin, ...
    {'pobj', 'init', 'haltfun', 'savegen', 'savename'}, ...
    {[], [], [], Inf, 'sueap.mat'});

% set up initial data for parallelization, if indicated
if ~isempty(pobj) & ~isempty(init)
    save SUEAP_DATA init
end

% loop over generations
for g = 1:ngen

    % serial fitness evaluation
    if isempty(pobj)

        for i = 1:length(pop)
            if isempty(init)
                fits{i} = fitness(pop{i});
            else
                fits{i} = fitness(pop{i}, init);
            end
        end

        % parallel evaluation, init data specified
    elseif ~isempty(init)

        fits = feval(pobj, 'sueap_fitness', pop);

        % parallel, no init data
    else
        fits = feval(pobj, 'fitness', pop);
    end

    % record current population and its fitnesses
    allpops{g} = pop;
    allfits{g} = fits;
    
    % update function is written separately for each implementing class
    [pop,sobj] = update(sobj, pop, fits, g, ngen);

    % report progress
    fprintf('Gen: %5d / %-5d\n', g, ngen)

end

