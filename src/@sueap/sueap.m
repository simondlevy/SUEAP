function sobj = sueap(args)
% superclass constructor for SuEAP objects; initializes random seed

sobj.seed = Inf;

sobj = class(sobj, 'sueap');

sobj.seed = getopts(sobj, args, {'seed'}, {Inf});

if sobj.seed ~= Inf
  seedrandom(sobj, sobj.seed)
end



