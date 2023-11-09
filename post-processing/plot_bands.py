import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs

mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['font.family'] = 'serif'

###########################################################################
###                     FUNCTION TO PLOT THE BANDS
###########################################################################
def bndplot(bandsfile,fermi,subplot,ylims, symmetry_points, symmetry_labels):
# bandsfile (.dat file): the file contaning plottable data from QE bands calculation
# fermi (float): the fermi energy
# subplot (plt.subplot)
# ylims (array [ymin, ymax]): y axis limits
# symmetry_points: array containing the x coordinates of the 1st Brilloin Zone k-path
# symmetry_labels: array contaning the 
  z = np.loadtxt(bandsfile) #This loads the bandx.dat.gnu file
  x = np.unique(z[:,0]) #This is all the unique x-points
  bands = []
  bndl = len(z[z[:,0]==x[1]]) #This gives the number of bands in the calculation
  axis = [min(x),max(x),-10, 10]

  for i in range(0,bndl):
    bands.append(np.zeros([len(x),2])) #This is where we store the bands

  for i in range(0,len(x)):
    sel = z[z[:,0] == x[i]]  #Here is the energies for a given x
    test = []
    for j in range(0,bndl): #This separates it out into a single band
      bands[j][i][0] = x[i]
      bands[j][i][1] = sel[j][1] - fermi #rescale the energy axis to E - Ef
  for i in bands: #Here we plots the bands
    subplot.plot(i[:,0],i[:,1],color="black", alpha=0.75, linewidth=1.25)

  # Plot the high simmetry points:
  if (len(symmetry_points) > 0):
    for i, j in zip(symmetry_points, symmetry_labels):
      subplot.axvline(i, ymin=0, ymax=1.0, color='k', ls='--', lw=1.0)
      subplot.text(i-0.02, ylims[0]-0.75, j, fontsize=15)

  #plot Fermi energy:
  fermi_plot = 0 # since the y axis was already rescaled, Fermi level is at 0 eV
  subplot.plot([min(x),max(x)],[fermi_plot,fermi_plot], '--',color='red', linewidth=1.5)
  subplot.set_xticklabels([])
  subplot.set_ylabel(r'E - $E_{F}$', fontsize=15)
  subplot.set_ylim([axis[2],axis[3]])
  subplot.set_xlim([axis[0],axis[1]])
  subplot.set_ylim([ylims[0],ylims[1]])