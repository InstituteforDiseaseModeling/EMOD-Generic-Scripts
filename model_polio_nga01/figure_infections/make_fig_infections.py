# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.append(os.path.abspath(os.path.join('..', '..', 'local_python')))
sys.path.append(os.path.abspath(os.path.join('..', 'Assets', 'python')))
from py_assets_common.emod_constants import NUM_SIMS, P_FILE, D_FILE, MO_DAYS

from global_data import base_year

# *****************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_baseline']

# *****************************************************************************


def make_fig():

    for dirname in DIRNAMES:

        # Sim outputs
        tpath = os.path.join('..', dirname)

        with open(os.path.join(tpath, D_FILE)) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(tpath, P_FILE)) as fid01:
            param_dict = json.load(fid01)

        t_vec = np.array(data_brick.pop('t_vec'))
        n_dict = data_brick.pop('node_names')
        n_sims = param_dict[NUM_SIMS]

        inf_data = np.zeros((n_sims, len(n_dict), t_vec.shape[0]))
        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            infmat = np.array(data_brick[sim_idx_str]['infmat'])
            inf_data[sim_idx, :, :] = infmat

        totinf = np.sum(inf_data, axis=1)
        cuminf = np.cumsum(totinf, axis=1)
        ulgas1 = np.sum(inf_data>2000, axis=1)
        ulgas2 = np.sum(inf_data>1, axis=1)

        c2minf = np.cumsum(inf_data, axis=2)
        clgas1 = np.sum(c2minf>2000, axis=1)
        clgas2 = np.sum(c2minf>1, axis=1)

        gdix = (cuminf[:, -1] > 5000)

        # Figure setup
        fig01 = plt.figure(figsize=(8, 6))

        axs01 = fig01.add_subplot(1, 1, 1)
        plt.sca(axs01)

        axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
        axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
        axs01.set_axisbelow(True)

        #dvals = [0]+MO_DAYS*int(run_years)
        #ticloc = np.cumsum(dvals)
        #ticlab = ['']*25
        #axs01.plot([245, 245], [0, 400e3], 'k:')
        #axs01.plot([610, 610], [0, 400e3], 'k:')
        #axs01.text(31.5, -2e4, '2016', fontsize=14)
        #axs01.text(31.5+365, -2e4, '2017', fontsize=14)

        #axs01.set_xticks(ticks=ticloc)
        #axs01.set_xticklabels(ticlab)

        #ticloc = [0.5e5, 1.0e5, 1.5e5, 2.0e5, 2.5e5, 3.0e5, 3.5e5, 4.0e5]
        #ticlab = ['50k', '100k', '150k', '200k',
        #          '250k', '300k', '350k', '400k']

        #axs01.set_yticks(ticks=ticloc)
        #axs01.set_yticklabels(ticlab)

        #obp_lab = 'Outbreak Probability: {:4.2f}'.format(np.sum(gdix)/n_sims)
        #axs01.text(2017.3, 325e3, obp_lab, fontsize=14)

        xval = t_vec/365 + base_year
        yval2 = clgas1[gdix, :]
        yval1 = np.mean(yval2, axis=0)
        axs01.plot(xval, yval1, c='C3', lw=3)
        for k3 in range(np.sum(gdix)):
            axs01.plot(xval, yval2[k3, :], '-', c='C3', alpha=0.05)

        yval2 = clgas2[gdix, :]
        yval1 = np.mean(yval2, axis=0)
        axs01.plot(xval, yval1, c='C0', lw=3)
        for k3 in range(np.sum(gdix)):
            axs01.plot(xval, yval2[k3, :], '-', c='C0', alpha=0.05)


        axs01.set_ylabel('Unique LGAs', fontsize=14)
        axs01.set_xlim(xval[0], xval[-1])
        #axs01.set_ylim(0, 400e3)

        plt.tight_layout()
        plt.savefig('fig_inf_{:s}_01.png'.format(dirname))
        plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
