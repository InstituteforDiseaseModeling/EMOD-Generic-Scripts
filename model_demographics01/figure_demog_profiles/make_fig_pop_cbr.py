# *****************************************************************************

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
REL_PATH = os.path.join('..', '..', 'local_python', 'py_assets_common')
sys.path.insert(0, os.path.abspath(REL_PATH))
from emod_demog_func import demog_vd_calc

# *****************************************************************************


def make_fig():

    # Load reference data
    yr_init = 50
    yr_base = 1900
    fname_pop = os.path.join('..', 'Assets', 'data', 'pop_dat_GBR.csv')
    pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')
    year_vec = pop_input[0, :]-yr_base
    pop_mat = pop_input[1:, :] + 0.1
    pop_init = [np.interp(yr_init, year_vec, pop_mat[idx, :])
                for idx in range(pop_mat.shape[0])]

    # Calculate vital dynamics
    vd_tup = demog_vd_calc(year_vec, yr_init, pop_mat, pop_init)
    xref = (vd_tup[4]/365)[::2]
    yref = (vd_tup[5])[::2]
    ybase = vd_tup[3]*365*1000

    # Figures
    fig01 = plt.figure(figsize=(8, 6))

    axs01 = fig01.add_subplot(1, 1, 1, label=None)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Year', fontsize=14)
    axs01.set_ylabel('Crude Birth Rate (per-1k)', fontsize=14)

    axs01.set_xlim(0, 30)
    axs01.set_ylim(8, 20)

    ticloc = [0, 5, 10, 15, 20, 25, 30]
    ticlab = ['1950', '1955', '1960', '1965', '1970', '1975', '1980']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab, fontsize=14)

    axs01.tick_params(axis='y', labelsize=14)

    axs01.plot(xref, ybase*yref, '.', lw=0, c='k', label='Data', ms=14)
    axs01.plot(xref, ybase*(yref*0 + 1), lw=2, c='C0', label='Equilibrium')

    # Save figure
    plt.tight_layout()
    plt.savefig('fig_pop_cbr_01.png')
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
