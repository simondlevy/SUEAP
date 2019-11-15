function varargout = getopts(s, varargs, names, defaults)
% get name/attribute options for SUEAP constructors

for j = 1:length(defaults)
  varargout{j} = defaults{j};
end


for i = 1:length(varargs)
  vararg = varargs{i};
  if ischar(vararg)    
    for j = 1:length(names)
      if strcmp(vararg, names{j})
        argval = varargs{i+1};
        varargout{j} = argval;
        i = i + 1;
      end
    end
  end
end
