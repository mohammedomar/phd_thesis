import sys
import phonon_calculations

#Accepts the input from the command line. Otherwise, uses the data from the file

nPh = 3 #Super Cell size
nSamples = 3 #Number of Samples in each direction in the k-space inside the BZ
E_cut = 100 #PW Energy Cut-off
fermi_width = 0.026 #Fermi Broadening (kT at Room Temperature)

if len(sys.argv) > 1:
    nPh = int(sys.argv[1])
    if len(sys.argv) > 2:
        nSamples = int(sys.argv[2])
        if len(sys.argv) > 3:
            E_cut = float(sys.argv[3])
            if len(sys.argv) > 4:
                fermi_width = float(sys.argv[4])
        

print('##########################################################')
print('Running phonon calculations with the following parameters:')
print('nPh      = '+str(nPh))
print('nSamples = '+str(nSamples))
print('Ecut     = '+str(E_cut))
print('kbT      = '+str(fermi_width))

phonon_calculations.phonon_bandstructure(nPh,nSamples,E_cut,fermi_width)
