import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import os

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

def prowfc_to_dataframe(filename, cols):
  df = pd.read_table(filepath_or_buffer=filename,
                     engine="python",
                     sep="\s+",
                     names=cols,
                     skiprows=1)

  return df


filebands = "../electronic-structure/BANDS/graphene.gnu"
Fermi = float(os.popen("grep Fermi ../electronic-structure/NSCF/graphene.nscf.pwo").read().split()[4])
# Fermi = 0.6438

sym_points = [0.0000, 0.6667, 1.2440, 1.5774]
sym_labels = ['K', r'$\Gamma$', 'M', 'K']

fig, axs = plt.subplots(1,2, sharey=True, figsize=[16,9],gridspec_kw={'width_ratios': [16, 8]})

bndplot(bandsfile=filebands,
        fermi=Fermi,
        subplot=axs[0],
        symmetry_labels=sym_labels,
        symmetry_points=sym_points, 
        ylims=[-6,6])

ratio = .3
# x_left, x_right = axs[1].get_xlim()
# y_low, y_high = axs[1].get_ylim()
# axs[1].set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)

filename = "../electronic-structure/pDOS/graphene.pdos_tot"
cols = ["E (eV)","dos(E)","pdos(E)"]

pdos = prowfc_to_dataframe(filename, cols)

print(pdos.head(3))

axs[1].plot(pdos["dos(E)"].to_numpy(),
            pdos["E (eV)"].to_numpy()-Fermi,
            color='k',
            lw=1.25)

axs[1].axhline(0, 0, 1, color='r', ls='--', lw=1.5)
axs[1].set_xlim([0,8])
axs[1].set_xlabel("states/eV")

axs[1].fill_betweenx(pdos["E (eV)"].to_numpy()-Fermi,
                0,
                pdos["dos(E)"].to_numpy(),
                where=(pdos["E (eV)"].to_numpy()-Fermi < 0),
                facecolor='b',
                alpha=0.35)

plt.savefig("graphene-bands-dos.png", dpi=300)
plt.show()