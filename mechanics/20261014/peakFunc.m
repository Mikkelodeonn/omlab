function [maxV, maxIout] = peakFunc(dx,spec, d)
    
% area = [720 721.5]
idx = find(dx>d(1) & dx<d(2));

% pf = polyfit(dx(idx), spec(idx)',2);

figure(1);clf; hold on

plot(dx, spec, 'b-')

plot(dx(idx), spec(idx), 'r-')
% plot(dx(idx), polyval(pf,dx(idx)), 'r-')

% specC = spec(idx)' - polyval(pf,dx(idx));
specC = spec(idx)';
figure(1);clf; hold on
plot(dx(idx), specC)

m11 = [d(1) d(2)];

idx11 = find(dx(idx)>m11(1) & dx(idx)<m11(2));

[maxV, maxI] = max(specC(idx11));

maxIout = dx(idx(1) + idx11(1) +  maxI - 2);
plot(maxIout, maxV, 'or')

