# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 18:35:48 2015

@author: momar
"""

from ase import Atoms, Atom
from ase.phonons import Phonons
from ase.io import write
from ase import io
from ase.visualize import view
from gpaw import GPAW,PW,FermiDirac
from ase.dft.kpoints import ibz_points, get_bandpath
import numpy as np
import matplotlib.pyplot as plt
import pickle,sys,os
import plot_bandstructure


def phonon_bandstructure(nPh = 3,nSamples = 3,E_cutoff = 100, fermi_width = 0.026):
    """
    Calculates and phonon bandstructure of graphene in accordance ot the input parameters using the RPBE method. The results are saved as PNG and MAT files as well using the suffix '_phonon_nPhxnPh_E_cutoff'. The calculations are performed using a 2-atom unit cell. The data are saved in the directories 'txt','mat','calc' and 'fig' according to their types. The program will create these directories if not available and will overwrite files in them with the same output file names. All calculations are performed while in the directory 'calc' inside a folder using the aforementioned file '_phonon_nPhxnPh_cell_nSamplesxnSamples_pts_E_cutoff'.
    :nPh (integer, optional, default = 3) : Length of super-cell square side used in calculations.
    :nSamples (integer, optional, default = 3): Number of sampling points in the k-space inside the bZ
    :E_cutoff (scalar, optional, default = 100) : Cut-off of PW energy (eV) used in the calculationsinitial calculations.
    :fermi_width (scalar, optional, default = 0.026) : Fermi-Dirac Distribution broadening (kT) in eV.
    """
    ##### Start of Code #####

    fileID = '_phonon_'+str(nPh)+'x'+str(nPh)+'_cell_'+str(nSamples)+'x'+str(nSamples)+'_pts_'+str(E_cutoff)
    dataID = 'bandstructure'
    
    makeDirs = ['txt','mat','fig','calc']
    for dirName in makeDirs:
        if not os.path.exists('./'+dirName):
            print('Making Directory ./'+dirName)
            try:
                os.makedirs('./'+dirName)
            except:
                print('Could not create directory!')

    if not os.path.exists('./calc'):
        return None #Exit if cannot perform calculations in the correct directory

    #Goto the calculations directory
    init_Dir = os.getcwd()
    txt_Dir = os.path.join(init_Dir,'./txt/')
    mat_Dir = os.path.join(init_Dir,'./mat/')
    fig_Dir = os.path.join(init_Dir,'./fig')
    os.chdir('./calc')
    if not os.path.exists(fileID[1:]):
        print('Creating calculations folder.')
        os.makedirs(fileID[1:])
    else:
        print('Calculations paths already exists!')
        
    os.chdir(fileID[1:])
    
    ao = 1.42 #Lattice spacing in angstroms between A and B sites
    C_A = Atom('C',(0,0,0))
    C_B = Atom('C',(ao,0,0))
    
    #Define a slab model for the graphene. Z-spacing is 10 times C-C spacing
    cell = 0.5*ao*np.array([[3.0,np.sqrt(3.0),0.0],[3.0,-np.sqrt(3.0),0],[0,0,10]])
    
    
    #Define the atoms and apply Periodic Boundary Conditions
    cell_atoms = Atoms([C_A,C_B],cell=cell,pbc =True)
    cell_atoms.center()

    #Band Calculation paths in terms of reciprogal latice basis
    G = [0,0,0]
    M = [0.5,0.5,0]
    K = [2.0/3.0,1.0/3.0,0] #According to the defined basis
    K_prime = [1.0/3.0,2.0/3.0,0.0]
    band_path = [G,M,K,G]
    band_path_labels=[r'\Gamma','M','K',r'\Gamma']
    nPts_band = 200 #Number of band structure points
    
    #Calculate Phonon Data
    log_path = os.path.join(txt_Dir,'gpaw_calc'+dataID+fileID+'_log.txt')
    kpts_calc = {'size':(nSamples,nSamples,1),'gamma':True}
    kpts_ph = {'size':(nPh,nPh,1),'gamma':True}
    ph_calc = GPAW(mode=PW(E_cutoff),basis='dzp',xc='RPBE',kpts = kpts_calc,occupations = FermiDirac(fermi_width),symmetry = 'off',txt = log_path)
    ph = Phonons(cell_atoms,ph_calc,supercell=(nPh,nPh,1))
    ph.run()
    ph.read(acoustic=True)
    kph_path,q_path,q_special =get_bandpath( band_path, cell_atoms.cell,nPts_band)
    omega_kn = 1000*ph.band_structure(kph_path) #Energy in meV
    
    #Phonon DOS calculations
    #omega_e,dos_e = ph.dos(kpts=(7,7,1),npts=500)
    #omega_e *= 1000

    #Save the data
    mat_path = os.path.join(mat_Dir,dataID+fileID)
    plot_bandstructure.save_to_matlab(mat_path,q_path,omega_kn,q_special)
    
    #Plot the data
    fig_path = os.path.join(fig_Dir,dataID+fileID+'.png')
    plt.figure() #In case of any other functionality additions
    plot_bandstructure.plot_bands(fig_path,q_path,omega_kn,q_special,band_path_labels,y_axis=r'$\Omega$ (meV)')
    plt.close() #Close the window in case of multiple runs

    os.chdir(init_Dir) #Get back to original directory
