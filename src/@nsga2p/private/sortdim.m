function I = sortdim(I, m)
% sort population members I by objective dimension m

L = length(I);
M = length(I{1}.fitness);

fits = zeros(L, M);

for i = 1:L
    fits(i,:) = I{i}.fitness;
end

[ignore,indices] = sort(fits(:,m));

I = I(indices);