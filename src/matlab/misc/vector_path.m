function r = vector_path(r_start,r_end,n)
%VECTOR_PATH returns the points across a path
% r = vector_path(r_start,r_end,npts) returns n points across the vector
% from r_start to r_end. The points are converted to row vectors making the
% different dimensions at different columns and stacking them in in rows.

x_start = reshape(r_start,length(r_start),1); %Convert to row vector
x_end= reshape(r_end,length(r_end),1); %Convert to row vector
dr = (r_end-r_start); % Difference vector
r = zeros(n,length(dr)); %Stacking the vector points in different rows.
path_scale = linspace(0,1,n); %Normalized distance

for i = 1:n
    r(i,:) = r_start + (path_scale(i).*dr);
end
