clear all;
close all;
clc;

%% Perform calculations
xi_sio2 = 0.95; %Electron affinity of SiO2
m_eff_sio2 = 0.5; %Charge carrier average effective mass
d = linspace(1,25,200); %Separation to be studied
Ef = linspace(0,0.3,200); %Fermi-level

k = zeros(length(d),length(Ef)); %Decay constant
G = zeros(length(d),length(Ef)); %Conductance per unit length estimate)

for j=1:length(Ef)
    for i=1:length(d)
        [k(i,j),G(i,j)] = g_estimate(d(i),Ef(j),xi_sio2,m_eff_sio2);
    end
end

%% Plot the results
figure;
contourf(d,Ef,log10(1e9.*G'),20)
xlabel('d (nm)');
ylabel('E_f (eV)');
title('log_{10}(g_c) (nS/m)'); %Conversion factor in the plot command
colorbar;

figure;
plot(Ef,k(1,:)./1e9) %The extinction coefficient is not a function of distance
xlabel('E_F (eV)');
ylabel('\kappa (nm^{-1})'); %Conversion factor was in the plot command