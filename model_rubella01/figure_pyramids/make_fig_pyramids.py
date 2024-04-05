# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
LOCAL_PATH = os.path.abspath(os.path.join('..', '..', 'local_python'))
sys.path.insert(0, LOCAL_PATH)
from py_assets_common.emod_constants import POP_AGE_DAYS, CLR_M, CLR_F, \
                                            NUM_SIMS, P_FILE, POP_PYR

# *****************************************************************************

DIRNAMES = ['experiment_sweepRI_popEQL_noSIAs']

TLABS = ['12', '10', '8', '6', '4', '2', '0', '2', '4', '6', '8', '10', '12']
TLOCS = [-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12]
START_YR = 2000
RUN_YEARS = 60

# *****************************************************************************


def make_fig():

    for dirname in DIRNAMES:

        # Sim outputs
        tpath = os.path.join('..', dirname)

        with open(os.path.join(tpath, 'data_brick.json')) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(tpath, P_FILE)) as fid01:
            param_dict = json.load(fid01)

        NSIMS = int(param_dict[NUM_SIMS])
        pyr_mat = np.zeros((NSIMS, RUN_YEARS+1, 20))-1
        year_vec = np.arange(START_YR, START_YR+RUN_YEARS+1, dtype=int)
        chart_yrs = year_vec[np.mod(year_vec, 10) == 0]
        num_charts = chart_yrs.shape[0]

        fig01 = plt.figure(figsize=(8*num_charts, 6))

        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            pyr_mat[sim_idx, :, :] = np.array(data_brick[sim_idx_str][POP_PYR])

        fidx = (pyr_mat[:, 0, 0] >= 0)

        pyr_mat_avg = np.mean(pyr_mat[fidx, :, :], axis=0)
        pyr_mat_std = np.std(pyr_mat[fidx, :, :], axis=0)

        # Figures - Sims
        for k1 in range(num_charts):

            gidx = np.argwhere(year_vec == chart_yrs[k1])[0][0]

            axs01 = fig01.add_subplot(1, num_charts, k1+1)
            plt.sca(axs01)

            axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
            axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
            axs01.set_axisbelow(True)

            axs01.set_xlabel('Percentage', fontsize=14)
            axs01.set_ylabel('Age (yrs)', fontsize=14)

            axs01.set_xlim(-12, 12)
            axs01.set_ylim(0, 100)

            axs01.set_xticks(ticks=TLOCS)
            axs01.set_xticklabels(TLABS)

            ydat = np.array(POP_AGE_DAYS)/365.0 - 2.5
            pop_dat = pyr_mat_avg[gidx, :]
            pop_dat_err = pyr_mat_std[gidx, :]
            tpop = np.sum(pop_dat)

            pop_dat_n = 100*pop_dat/tpop
            pop_dat_n_err = 100*pop_dat_err/tpop

            axs01.barh(ydat[1:], pop_dat_n/2.0, height=4.75,
                       xerr=pop_dat_n_err, color=CLR_F)
            axs01.barh(ydat[1:], -pop_dat_n/2.0, height=4.75,
                       xerr=pop_dat_n_err, color=CLR_M)

            tpop_str = 'Total Pop\n{:5.1f}M'.format(tpop/1e6)
            axs01.text(-11, 92.5, '{:04d}'.format(year_vec[gidx]), fontsize=18)
            axs01.text(5, 87.5, tpop_str, fontsize=18)

        plt.tight_layout()
        plt.savefig('fig_pyr_{:s}_01.png'.format(dirname))
        plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
