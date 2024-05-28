# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.append(os.path.abspath(os.path.join('..', '..', 'local_python')))
sys.path.append(os.path.abspath(os.path.join('..', 'Assets', 'python')))
from py_assets_common.emod_constants import EXP_C, EXP_V, NUM_SIMS, \
                                            P_FILE, POP_PYR
from global_data import t_step_days, run_years

# *****************************************************************************

DIRNAMES = ['experiment_interruption01',]

# *****************************************************************************


def make_fig():

    for dirname in DIRNAMES:

        # Sim outputs
        tpath = os.path.join('..', dirname)

        with open(os.path.join(tpath, 'data_brick.json')) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(tpath, P_FILE)) as fid01:
            param_dict = json.load(fid01)

        nsims = int(param_dict[NUM_SIMS])

        targ_clust_vec = np.array(param_dict[EXP_V]['target_cluster'])
        targ_clusts = np.unique(targ_clust_vec).tolist()

        inf_dat = np.zeros((nsims, int(365*run_years/t_step_days)))
        pyr_mat = np.zeros((nsims, int(run_years)+1, 20))-1

        for skey in data_brick:
            if (not skey.isdigit()):
                continue

            sidx = int(skey)
            inf_dat[sidx, :] = np.array(data_brick[skey]['inf_frac_vec'])
            pyr_mat[sidx, :, :] = np.array(data_brick[skey][POP_PYR])

        fidx = (pyr_mat[:, 0, 0] >= 0)

        # Figures
        fig01 = plt.figure(figsize=(8, 6))

        # Figures - Sims - Infections
        axs01 = fig01.add_subplot(1, 1, 1)
        plt.sca(axs01)

        axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
        axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
        axs01.set_axisbelow(True)

        for targ_clust in targ_clusts:
            idx02 = (targ_clust_vec == targ_clust)
            tidx = (fidx & idx02)

            sub_samp = int(365*10/t_step_days)
            inf_dat_sub = inf_dat[tidx,-sub_samp:]
            frac_zeros = np.sum(inf_dat_sub==0, axis=1)/inf_dat_sub.shape[1]
            print("Cluster {:d} - Prob Endemic: ".format(targ_clust), np.sum(frac_zeros==0)/frac_zeros.shape[0])

            hist_lab = 'Cluster {:d}: Avg = {:4.2f}'.format(targ_clust, np.mean(frac_zeros))

            axs01.hist(frac_zeros, bins=np.arange(0,1.01,0.05), density=True, edgecolor='k', alpha=0.7, label=hist_lab)

        axs01.set_ylabel('Probability', fontsize=16)
        axs01.set_xlabel('Zero Prevalence (Fraction of Time)', fontsize=16)

        axs01.legend()
        axs01.tick_params(axis='both', which='major', labelsize=14)

        plt.tight_layout()
        plt.savefig('fig_interrupt_{:s}_01.png'.format(dirname))
        plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
