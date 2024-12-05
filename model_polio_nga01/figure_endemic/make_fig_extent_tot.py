# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.append(os.path.abspath(os.path.join('..', '..', 'local_python')))
sys.path.append(os.path.abspath(os.path.join('..', 'Assets', 'python')))
from py_assets_common.emod_constants import NUM_SIMS, P_FILE, D_FILE, \
                                            MO_DAYS, EXP_C

from global_data import base_year

# *****************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_baseline',
            'experiment_cVDPV2_NGA_100km_baseline_SIAs',
            'experiment_cVDPV2_NGA_100km_baseline_RI']

# *****************************************************************************


def make_fig():

    # Figure setup
    fig01 = plt.figure(figsize=(12, 6))

    axs01 = fig01.add_subplot(1, 1, 1)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)
    axs01.tick_params(axis='x', which='major', labelsize=18)
    axs01.tick_params(axis='y', which='major', labelsize=14)

    refx = None
    refy = None

    for dirname in DIRNAMES:

        # Sim outputs
        tpath = os.path.join('..', dirname)

        with open(os.path.join(tpath, D_FILE)) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(tpath, P_FILE)) as fid01:
            param_dict = json.load(fid01)

        t_vec = np.array(data_brick.pop('t_vec'))/365 + base_year
        n_dict = data_brick.pop('node_names')
        n_sims = param_dict[NUM_SIMS]
        run_years = param_dict[EXP_C]['run_years']

        inf_data = np.zeros((n_sims, len(n_dict), t_vec.shape[0]))
        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            infmat = np.array(data_brick[sim_idx_str]['infmat'])
            inf_data[sim_idx, :, :] = infmat

        totinf = np.sum(inf_data, axis=1)
        cuminf = np.cumsum(totinf, axis=1)
        totlga = np.sum(inf_data>0, axis=1)

        #gidx = (cuminf[:, -1] > 5000)
        #gidx = (totinf[:, -1] > 0) & (totlga[:, -240] > 15) & (totlga[:, -145] > 10)
        gidx = (totinf[:, -1] > 0)
        #print(np.sum(gidx))
        #print(np.argwhere(gidx))
        #gidx = (cuminf[:, -1] > 1e6) & (cuminf[:, -1] < 2.5e6)

        dvals = [0]+MO_DAYS*int(run_years)
        ticloc = np.cumsum(dvals) + t_vec[0]
        axs01.set_xticks(ticks=ticloc, minor=True)

        ticloc = np.arange(0, int(run_years)+1) + t_vec[0]
        axs01.set_xticks(ticks=ticloc)

        yval2 = totlga[gidx, :]
        yval1 = np.mean(yval2, axis=0)
        #for k3 in range(np.sum(gidx)):
            #axs01.plot(t_vec, yval2[k3, ], '.', c='C0', alpha=0.1)
            #axs01.plot(t_vec, yval2[k3, ])
        axs01.plot(t_vec, yval1, lw=3)

        axs01.set_ylabel('LGAs with Transmission', fontsize=14)
        axs01.set_xlim(t_vec[0], t_vec[-1])
        axs01.set_ylim(0, 200)

        if (refx is None):
            refx = t_vec[:-165]
            refy = yval1[:-165]

    axs01.plot(refx, refy, lw=3, c='k')
    plt.tight_layout()
    plt.savefig('fig_extent_tot_{:s}_01.png'.format(dirname))
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
