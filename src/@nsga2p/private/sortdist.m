function I = sortdist(I)
% sort front elements in descending order of crowding distance

for i = 1:length(I)
    distances(i) = I{i}.distance;
end

[ignore, indices] = sort(distances, 'descend');

I = I(indices);
