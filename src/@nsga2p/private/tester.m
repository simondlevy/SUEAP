function tester(n, doplot)

colors = 'rkmbg';

for i = 1:n
    g = rand(1,2);
    f = g;
    P{i} = makemember(i, g, f);
end

F = fast_nondominated_sort(P);

if doplot
    clf
    hold on
    axis equal
    axis([0 1 0 1])
end

for i = 1:length(F)
    front = crowding_distance_assignment(F{i});
    if ~doplot, continue, end
    for j = 1:length(front)
        xy = front{j}.fitness;
        color = colors(mod(i-1, length(colors)) + 1);
        charsize = fix(24*front{j}.distance);
        charsize = max(min(charsize, 18), 1);
        text(xy(1), xy(2), num2str(i), 'Color',color, 'FontSize',charsize)
    end
	pause(1)
end

