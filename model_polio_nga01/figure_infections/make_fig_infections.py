# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.append(os.path.abspath(os.path.join('..', '..', 'local_python')))
sys.path.append(os.path.abspath(os.path.join('..', 'Assets', 'python')))
from py_assets_common.emod_constants import NUM_SIMS, P_FILE, D_FILE

from global_data import run_years

# *****************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_noSIAs',
            'experiment_cVDPV2_NGA_100km_SIAs']

# *****************************************************************************


def make_fig():

    for dirname in DIRNAMES:

        # Sim outputs
        tpath = os.path.join('..', dirname)

        with open(os.path.join(tpath, D_FILE)) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(tpath, P_FILE)) as fid01:
            param_dict = json.load(fid01)

        data_brick.pop('node_names')
        n_sims = param_dict[NUM_SIMS]
        n_tstep = int(365.0*run_years)

        tot_inf = np.zeros((n_sims, n_tstep))
        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            tinf = np.array(data_brick[sim_idx_str]['totinf'])
            tot_inf[sim_idx, :] = np.cumsum(tinf)

        gdix = (tot_inf[:, -1] > 5000)

        # Figure setup
        fig01 = plt.figure(figsize=(8, 6))

        axs01 = fig01.add_subplot(1, 1, 1)
        plt.sca(axs01)

        axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
        axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
        axs01.set_axisbelow(True)

        axs01.set_ylabel('Cumulative Total Infections', fontsize=14)

        axs01.set_xlim(0, 750)
        axs01.set_ylim(0, 400e3)

        dvals = [0]+[31, 30, 31, 31, 30, 31, 30, 31, 31, 28, 31, 30]*2
        ticloc = np.cumsum(dvals)
        ticlab = ['']*25
        axs01.plot([245, 245], [0, 400e3], 'k:')
        axs01.plot([610, 610], [0, 400e3], 'k:')
        axs01.text(31.5, -2e4, '2016', fontsize=14)
        axs01.text(31.5+365, -2e4, '2017', fontsize=14)

        axs01.set_xticks(ticks=ticloc)
        axs01.set_xticklabels(ticlab)

        ticloc = [0.5e5, 1.0e5, 1.5e5, 2.0e5, 2.5e5, 3.0e5, 3.5e5, 4.0e5]
        ticlab = ['50k', '100k', '150k', '200k',
                  '250k', '300k', '350k', '400k']

        axs01.set_yticks(ticks=ticloc)
        axs01.set_yticklabels(ticlab)

        obp_lab = 'Outbreak Probability: {:4.2f}'.format(np.sum(gdix)/n_sims)
        axs01.text(30, 325e3, obp_lab, fontsize=14)

        xval = np.arange(n_tstep) + 0.0
        yval1 = np.mean(tot_inf[gdix, :], axis=0)
        yval2 = tot_inf[gdix, :]
        axs01.plot(xval, yval1, c='C0')
        for k3 in range(np.sum(gdix)):
            axs01.plot(xval[5::2*5], yval2[k3, 5::2*5], '.', c='C0')

        plt.tight_layout()
        plt.savefig('fig_inf_{:s}_01.png'.format(dirname))
        plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
