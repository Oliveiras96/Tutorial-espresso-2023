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
###                     FUNÇÃO PARA PLOTAR AS BANDAS
###########################################################################
def bndplot(bandsfile,fermi,subplot,ylims, symmetry_points, symmetry_labels):
  z = np.loadtxt(bandsfile)
  x = np.unique(z[:,0])
  bands = []
  bndl = len(z[z[:,0]==x[1]])
  axis = [min(x),max(x),-10, 10]

  for i in range(0,bndl):
    bands.append(np.zeros([len(x),2]))

  for i in range(0,len(x)):
    sel = z[z[:,0] == x[i]]
    test = []
    for j in range(0,bndl):
      bands[j][i][0] = x[i]
      bands[j][i][1] = sel[j][1] - fermi 
  for i in bands: 
    subplot.plot(i[:,0],i[:,1],color="black", alpha=0.75, linewidth=1.5)

  # Desenhar as linhas com os pontos de alta simetria:
  if (len(symmetry_points) > 0):
    for i, j in zip(symmetry_points, symmetry_labels):
      subplot.axvline(i, ymin=0, ymax=1.0, color='k', ls='--', lw=1.25)
      subplot.text(i-0.02, ylims[0]-1.5, j, fontsize=20)

  # Desenhar a linha da energia de Fermi:
  fermi_plot = 0 
  subplot.plot([min(x),max(x)],[fermi_plot,fermi_plot], '--',color='red', linewidth=1.5)
  subplot.set_xticklabels([])
  subplot.set_ylabel(r'E - $E_{F}$', fontsize=20)
  subplot.set_ylim([axis[2],axis[3]])
  subplot.set_xlim([axis[0],axis[1]])
  subplot.set_ylim([ylims[0],ylims[1]])
##############################################################################################

##############################################################################################
#               FUNÇÃO PARA LER O ARQUIVO DE DENSIDADE DE ESTADOS COM O PANDAS
##############################################################################################
def prowfc_to_dataframe(filename, cols):
  df = pd.read_table(filepath_or_buffer=filename,
                     engine="python",
                     sep="\s+",
                     names=cols,
                     skiprows=1)

  return df
##############################################################################################

# Arquivo de saida do pos-processamento de bandas:
filebands = "../electronic-structure-new/BANDS/graphene.gnu"

# Pegar a energia de Fermi diretamente 
Fermi = float(os.popen("grep Fermi ../electronic-structure-new/NSCF/graphene.nscf.pwo").read().split()[4])

# Pontos de simetria:
sym_points = [0.0000, 0.6667, 1.2440, 1.5774]
# Label dos pontos de alta simetria:
sym_labels = ['K', r'$\Gamma$', 'M', 'K']

fig, axs = plt.subplots(1,2, sharey=True, figsize=[16,9],gridspec_kw={'width_ratios': [16, 8]})

bndplot(bandsfile=filebands,
        fermi=Fermi,
        subplot=axs[0],
        symmetry_labels=sym_labels,
        symmetry_points=sym_points, 
        ylims=[-15,15])

# Arquivo com a densidade de estados:
pdos_filename = "../electronic-structure-new/DOS-new/graphene.pdos_tot"
cols = ["E (eV)","dos(E)","pdos(E)"]

pdos = prowfc_to_dataframe(pdos_filename, cols)
axs[1].plot(pdos["dos(E)"].to_numpy(),
            pdos["E (eV)"].to_numpy()-Fermi,
            color='k',
            lw=1.25)

axs[1].axhline(0, 0, 1, color='r', ls='--', lw=1.5)
axs[1].set_xlim([0,4])
axs[1].set_xlabel("states/eV", fontsize=20)

axs[1].fill_betweenx(pdos["E (eV)"].to_numpy()-Fermi,
                0,
                pdos["dos(E)"].to_numpy(),
                where=(pdos["E (eV)"].to_numpy()-Fermi < 0),
                facecolor='b',
                alpha=0.35)


# Salva a figura:
plt.savefig("graphene-bands-dos.png", dpi=300)
plt.show()