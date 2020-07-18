function plotfronts(F, dims, lims, gen, ngen)
% Visualize sorted non-dominated fronts for NSGA-II.  Each front is labeled
% by its sorting rank, and given an arbitrary color.  The size of a label
% indicates the crowding distance associated with that member.  Members
% that do not make it into the next population are given a common
% arbitrary size and colored grey.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

COLORS = 'rkmbg';
PAUSE_SECONDS = 0; %0.5;
FONTSIZE_FOR_INFINITY = 24;
FONTSIZE_MAX = 18;
FONTSIZE_MIN = 6;
FONTSIZE_NODIST = 12;
COLOR_NODIST = [.5 .5 .5]; % grey

clf
hold on

if ~isempty(lims)
    axis(lims)
end

title(sprintf('Generation %d / %d', gen, ngen))

for i = 1:length(F)
    front = F{i};
    for j = 1:length(front)
        x = front{j}.fitness(dims(1));
        y = front{j}.fitness(dims(2));
        if isfield(front{j}, 'distance')
            color = COLORS(mod(i-1, length(COLORS)) + 1);
            fontsize = fix(FONTSIZE_MAX*front{j}.distance);
            fontsize = min(fontsize, FONTSIZE_FOR_INFINITY);
            fontsize = max(fontsize, FONTSIZE_MIN);
        else
            color = COLOR_NODIST;
            fontsize = FONTSIZE_NODIST;
        end
        text(x, y, num2str(i), 'Color',color, 'FontSize',fontsize)
        plot(x, y, 'w') % plot invsible dot to force auto axis resizing
    end
	pause(PAUSE_SECONDS)
end

drawnow

