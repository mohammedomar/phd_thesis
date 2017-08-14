clear all;
close all;
clc;

Npts_cut = 500;
Npts_k = 2000;
a = 0.142; %C-C spacinging in nm
kx = linspace(-2*pi./a,2*pi./a,Npts_k).*0.5;
ky = linspace(-2*pi./a,2*pi./a,Npts_k).*0.5;

% High symmetry points
G_point = [0,0]; %Gamma
M_point = (2.*pi./(3.*a)).*[1,0]; %M
K_point = (2.*pi./(3.*a)).*[1,1./sqrt(3)]; %K
K_p_point = (2.*pi./(3.*a)).*[1,-1./sqrt(3)]; %K'

BZ_kx = [K_p_point(1),K_point(1),0           ,-K_p_point(1),-K_point(1),0];
BZ_ky = [K_p_point(2),K_point(2),norm(K_point),-K_p_point(2),-K_point(2),-norm(K_point)];

%Offset version
% BZ_kx = BZ_kx+K_point(1); 
% BZ_ky = BZ_ky + K_point(2);

%% Tight binding calculations
t = 2.7; %Tight binding hamiltonian hopping energy
t_prime = -0.2.*t.*0; %Tight binding fitting parameter
[Kx,Ky] = meshgrid(kx,ky);
idx_bz = inpolygon(Kx,Ky,BZ_kx,BZ_ky);

f =  @(x,y) ((2.*cos(sqrt(3).*y.*a))+(4.*cos(0.5.*sqrt(3).*y.*a).*cos(1.5.*x.*a)));
E_c_full = (-t_prime.*f(Kx,Ky))+(t.*sqrt(3+f(Kx,Ky)));
E_v_full = (-t_prime.*f(Kx,Ky))-(t.*sqrt(3+f(Kx,Ky)));


E_c_bz = nan(size(E_c_full));
E_c_bz(idx_bz) = E_c_full(idx_bz);
E_v_bz = nan(size(E_v_full));
E_v_bz(idx_bz) = E_v_full(idx_bz);
Kx_bz = nan(size(Kx));
Ky_bz = nan(size(Ky));
Kx_bz(idx_bz) = Kx(idx_bz);
Ky_bz(idx_bz) = Ky(idx_bz);



figure;
contourf(Kx./(2*pi./a),Ky./(2*pi./a),E_c_full);
xlabel('k_x (2\pi/a_o)');
ylabel('k_y (2\pi/a_o)');
colorbar;

figure;
contourf(Kx_bz./(2*pi./a),Ky_bz./(2*pi./a),E_c_bz);
xlabel('k_x (2\pi/a_o)');
ylabel('k_y (2\pi/a_o)');
colorbar;
axis equal;

figure;
surf(Kx./(2*pi./a),Ky./(2*pi./a),E_c_full);
hold on;
surf(Kx./(2*pi./a),Ky./(2*pi./a),E_v_full);
shading interp;
view(45,8)
xlabel('k_x (2\pi/a_o)');
ylabel('k_y (2\pi/a_o)');
zlabel('Energy (eV)');

figure;
surf(Kx./(2*pi./a),Ky./(2*pi./a),E_c_bz);
hold on;
surf(Kx./(2*pi./a),Ky./(2*pi./a),E_v_bz);
shading interp;
view(45,8)
xlabel('k_x (2\pi/a_o)');
ylabel('k_y (2\pi/a_o)');
zlabel('Energy (eV)');

%% Cut path

r_gm = vector_path(G_point,M_point,Npts_cut); %Gamma -> M
r_mk = vector_path(M_point,K_point,Npts_cut); %M -> K
r_kg = vector_path(K_point,G_point,Npts_cut); %K -> G

path_x = [r_gm(:,1);r_mk(:,1),;r_kg(:,1)];
path_y = [r_gm(:,2);r_mk(:,2),;r_kg(:,2)];

E_c_path = interp2(Kx,Ky,E_c_full,path_x,path_y);
E_v_path = interp2(Kx,Ky,E_v_full,path_x,path_y);

figure;
hold on;
plot(E_c_path);
plot(E_v_path);
xlabel('Wave vector');
ylabel('Energy (eV)');

%X-Axis labels
label_positions = [0:3].*Npts_cut;
label_positions(1) = 1; %The first point has an index of 1 not 0
label_str = {'\Gamma','M','K','\Gamma'};
set(gca,'xtick',label_positions,'xticklabel',label_str)

%Plot the vertical lines of the labels
ax_limits = axis;
for i = label_positions
    plot([i,i],[ax_limits(3),ax_limits(4)],'k-','LineWidth',1);
end

%% Calculating Density of States

E_range = linspace(0,3*t,500);
C = contourc(kx,ky,E_c_bz,E_range);
[kx_vals,ky_vals,l_vals]=read_contourMatrix(C);
dkx = kx(2)-kx(1);
dky = ky(2)-ky(1);
DOS = zeros(size(E_range));
%Remember to add a scaling value
for i = 1:length(l_vals)
    e_val = l_vals(i);
    e_idx = E_range == e_val;
    kx_tmp = kx_vals{i};
    ky_tmp = ky_vals{i};
    delta_kx = diff(kx_tmp);
    delta_ky = diff(ky_tmp);
    dl = sum(sqrt((delta_kx.^2)+(delta_ky.^2)));
    DOS(e_idx) = DOS(e_idx)+dl;
end
DOS = DOS./(2*pi*pi)*1e18*5.245e-20; %Scaling terms (/eV/atom)
figure;
plot(E_range,DOS)
xlabel('Energy (eV)');
ylabel('D(E) (eV^{-1} atom^{-1})');
