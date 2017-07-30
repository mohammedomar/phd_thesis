import matplotlib.pyplot as plt
import numpy as np
from scipy.io import savemat

def plot_bands(output_file,x,y,x_special,x_labels,x_axis='k-vector',y_axis='E-E$_F$ (eV)',title=''):
    """
    Plots the data obtained from the band structure calculations used in GPAW
    :output_file s(string) : Path to save the figure, the extension defines the image type. .PNG is recommended.
    :x (array-like) : X-Axis points of the plot, obtained typically from the get_bandstructure command as the second argument
    :y (array-like) : Y-Axis points of the plot, typically the results of the calculations
    :x_special (array-like) : Formatted string of the special symmetry points used in the band structure calculation, obtained typically from the get_band_structure command as the third argument
    :x_labels (array-like) : String array of the same size as x_special representing the labels of the Special points as will be shown on the plotted data
    :x_axis (string, optional, default = 'k-vector') : String label of the X-Axis
    :y_axis (string, optional, default = 'E-E$_F$ (eV)' : String label of the Y-Axis
    :title (string optional, default ='') : String title of the plot
    
    Returns:
    None
    """
    nPlots = np.shape(y)[1] #Number of plots
    plt.plot(x,y)

    #Special points Vertical Lines
    y_min = y.min()
    y_max = y.max()
    for i in range(len(x_special)):
        plt.plot([x_special[i],x_special[i]],[y_min,y_max],'k-')

    #Plotting the special labels and the Fermi Level
    plt.plot([0, x_special[-1]], [0, 0], 'k-') #Fermi Level Plot
    plt.xticks(x_special, ['$%s$' % n for n in x_labels])
    plt.axis(xmin=0, xmax=x_special[-1], ymin=y_min, ymax=y_max)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    plt.savefig(output_file,dpi=600)
    return None

def save_to_matlab(output_file,x,y,x_special):
    """
    Saves the results of GPAW bandstructure simulation into MATLAB. The ouput parameters in MATLAB has the labels x,y and x_special
    
    : output_file (string) : path to output MATLAB file
    :x (array-like) : X-Axis points of the plot, obtained typically from the get_bandstructure command as the second argument
    :y (array-like) : Y-Axis points of the plot, typically the results of the calculations
    :x_special (array-like) : Formatted string of the special symmetry points used in the band structure calculation, obtained typically from the get_band_structure command as the third argument
    """
    savemat(output_file,dict(x=x,y=y,x_special=x_special))
