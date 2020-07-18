function [front,notfront] = getfront(mobj, fits)
% GETFRONT Get Pareto front from population fitnesses
%
% FRONT =  GETFRONT(MOBJ, FITS) goes through all fitsnesses in FITS.
% It returns FRONT, an array of the indices on the frontier based
% on the weights W of each of the fitnesses in FITS.  
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

p = length(fits);
n = length(fits{1});

front = [];

% XXX noise is additive inverse of bias
%noiz = (1-mobj.bias) .* randn(1,n);
noiz = zeros(1,n);
    
for i = 1:p

  unbeaten = true;
  
  for j = 1:p

    if ~unbeaten
       break
    end
    
    % if this guy is less than some other on all dims, he's toast!
    if prod(double((fits{i} < (fits{j} + noiz))))
      unbeaten = false; 
    end

  end

  if (unbeaten == true)
    front(end+1) = i;
  end

end

notfront = setdiff([1:size(fits,2)], front);
