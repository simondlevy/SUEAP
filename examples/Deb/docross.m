function c = docross(p1, p2)

xpt = fix(rand * length(p1)) + 1;

c = [p1(1:xpt) p2(xpt+1:end)];
