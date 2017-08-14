function [x,y,c_level] = read_contourMatrix(C)
%READ_CONTOURMATRIX reads the data of contour matrix and returning the path
%of the contour.
% [x,y,c_level] = read_contourMatrix(C) returns the x and y paths of each 
% level in the contour matrix C. Each path is returned as a an element in 
% the cell arrays x and y, and the level added to the vector c_level

C_size = size(C);

idx_c=1; %Column index
n = 0; %No. of levels counter
while idx_c < C_size(2) %Go through the columns
    n = n+1; %Levels counter
    c_level(n) = C(1,idx_c);%Level value
    n_pairs =  C(2,idx_c); %Number of pairs
    %Parse the elements
    x{n} = C(1,idx_c+1:idx_c+n_pairs);
    y{n} = C(2,idx_c+1:idx_c+n_pairs);
    
    %Go to next place
    idx_c = idx_c + n_pairs +1;
end