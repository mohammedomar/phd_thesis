function plot_bandstructure(x,y,x_special,label_str)
%%plot_bandstructure plots the data obtained from the GPAW. The labels
%%should be given as a cell string and e the same size as x_special.

plot(x,y)
hold on;
y_min = min(min(y));
y_max = max(max(y));

for i = 1:length(x_special)
    plot([x_special(i),x_special(i)],[y_min,y_max],'k-','LineWidth',1);
end

set(gca,'XTick',x_special,'XTickLabel',label_str)
axis tight;
ylabel('Energy (meV)');