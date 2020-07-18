% this avoids excecution on non-Unix platforms
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License
if ~isempty(getenv('ARCH'))

  home = getenv('HOME');

  addpath(home)

  addpath([ home '/sueap/src'])

  addpath([home '/pecon/src'])

  addpath([home '/pecon/xml_toolbox-3.0a'])

  javaaddpath([home '/pecon/src/pecon.jar'])
  
end



