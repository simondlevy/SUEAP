function plotfits(fits, dims, lims, gen, ngen)
% visualize fitnesses for SGAP

PAUSE_SECONDS = 1.0;
STYLE = 'b+';

clf
hold on
axis equal

if ~isempty(lims)
    axis(lims)
end

title(sprintf('Generation %d / %d', gen, ngen))

for i = 1:length(fits)
    fit = fits{i};
    x = fit(dims(1));
    y = fit(dims(2));
    plot(x, y, STYLE)
end


pause(PAUSE_SECONDS)

drawnow
