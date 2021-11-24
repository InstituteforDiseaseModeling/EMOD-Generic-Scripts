#*******************************************************************************

import os, sys, json

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from builder_demographics import br_base_val, br_force_xval, br_force_yval

#*******************************************************************************

ybase   = br_base_val
xval    = br_force_xval
yref    = np.array(br_force_yval)

# Figures
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('Crude Birth Rate (per-1k)', fontsize=14)

axs01.set_xlim( 0, 30)
axs01.set_ylim( 5, 25)

ticloc = [0, 5, 10, 15, 20, 25, 30]
ticlab = ['1950', '1955', '1960', '1965', '1970', '1975', '1980']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab,fontsize=14)

ticloc = [5, 10, 15, 20, 25]
ticlab = ['5', '10', '15', '20', '25']
axs01.set_yticks(ticks=ticloc)
axs01.set_yticklabels(ticlab,fontsize=14)

axs01.plot(xval, ybase*(yref), '.',  lw=0, c='k',  label='Data', ms=14, zorder=1)
axs01.plot(xval, ybase*(yref*0 + 1), lw=2, c='C0', label='Equilibrium', zorder=3)

axs01.legend()

plt.tight_layout()
plt.savefig('fig_pop_cbr_01.png')
plt.close()

#*******************************************************************************
