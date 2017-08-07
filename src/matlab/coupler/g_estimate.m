function [k,G] = g_estimate(d_nm,Ef_eV,xi_insulator_eV,m_insulator)
%%g_esmiate esimates the tunneling resistance across a GIG junction.
% [k,G] = g_estimate(d_nm,Ef_eV,xi_insulator_eV,m_insulator)
% Calculates the 1D tunneling resistance between to graphene electrodes
% that are d_nm apart, both with a Fermi-Level of Ef_eV with an insulator
% of electron affinity of xi_insulator_eV and charge carrier effective
% mass of m_insulator.
%
% d_nm is in nm, Ef_eV and xi_insulator_eV are in eV and m_insulator is
% dimensionless.

q = 1.602e-19; %Electronic Charge
hbar = 1.0545718e-34; %Reduced Planck's constant
vf = 1e6; %Fermi velocity in graphene
mo = 9.11e-31; %Free Electron mass
m = m_insulator*mo; %Effective mass of SiO2
ao = 1.42e-10; %Graphene C-C distance
K_prime = 4*pi/(3*sqrt(3)*ao); %Wavevector magnitude to the Dirac point
I_const = q*(hbar^2)/(vf*(m^2)); %Current scaling factor
d = d_nm.*1e-9;
Ef = Ef_eV.*q;

phi_graphene = 4.5*q;%Work function of graphene
 
phi = phi_graphene - (xi_insulator_eV*q) -abs(Ef); %Barrier height

k = sqrt((2.*m.*phi./(hbar.^2))+(0*K_prime).^2); %Decay characteristic length does not need the K_prime momentum

tunnel_sum = q.*(2./(hbar*vf));
G = I_const.*((k.*exp(-k.*d)).^2).*tunnel_sum;