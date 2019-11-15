function plotfronts(fits, front, notfront, dims, lims, gen, ngen)
% visualize frontier and non-frontier fitnesses for MOOP

PAUSE_SECONDS = 1.0;
STYLE_FRONT = 'r+';
STYLE_NOTFRONT = 'bo';

clf
hold on
axis equal

if ~isempty(lims)
    axis(lims)
end

title(sprintf('Generation %d / %d', gen, ngen))

plotfits(fits, front, STYLE_FRONT, dims)
plotfits(fits, notfront, STYLE_NOTFRONT, dims)

pause(PAUSE_SECONDS)

function plotfits(fits, indices, style, dims)

for i = 1:length(indices)
    fit = fits{indices(i)};
    x = fit(dims(1));
    y = fit(dims(2));
    plot(x, y, style)
end

drawnow

