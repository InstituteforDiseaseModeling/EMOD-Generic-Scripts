# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.append(os.path.abspath(os.path.join('..', 'local_python')))
sys.path.append(os.path.abspath(os.path.join('Assets', 'python')))
from py_assets_common.emod_local_proc import crs_proc
from py_assets_common.emod_constants import EXP_C, EXP_V, CBR_VEC, \
                                            NUM_SIMS, P_FILE, POP_PYR
from global_data import run_years, start_year

# *****************************************************************************

DIRNAMES = [('experiment_DRC_popEQL', 'No Vaccine'),
            ('experiment_DRC_popEQL_RI', 'RI Only'),
            ('experiment_DRC_popEQL_RI-CU90', 'RI + Catch-up'),
            ('experiment_DRC_popEQL_RI-CU-FU90', 'RI + Catch-up + Follow-ups')]

# *****************************************************************************


def make_fig():

    # Figures
    fig01 = plt.figure(figsize=(8, 6))

    # Figures - Sims - CRS
    axs01 = fig01.add_subplot(1, 1, 1)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_ylabel('Annual Rubella Burden per 100k Births', fontsize=16)
    axs01.set_xlabel('Year', fontsize=16)

    axs01.set_xlim(0, 30)
    axs01.set_ylim(0, 300)
    axs01.tick_params(axis='x', labelsize=16)
    axs01.tick_params(axis='y', labelsize=16)


    for dirname in DIRNAMES:

        # Sim outputs
        with open(os.path.join(dirname[0], 'data_brick.json')) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(dirname[0], P_FILE)) as fid01:
            param_dict = json.load(fid01)

        nsims = int(param_dict[NUM_SIMS])
        ss_demog = param_dict[EXP_C]['steady_state_demog']
        demog_set = param_dict[EXP_C]['demog_set']

        pyr_mat = np.zeros((nsims, int(run_years)+1, 20))-1
        inf_mat = np.zeros((nsims, int(run_years), 20))
        birth_mat = np.zeros((nsims, int(run_years)))

        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            sim_data = data_brick[sim_idx_str]
            pyr_mat[sim_idx, :, :] = np.array(sim_data[POP_PYR])
            inf_mat[sim_idx, :, :] = np.array(sim_data['inf_data'])
            birth_mat[sim_idx, :] = np.array(sim_data[CBR_VEC])

        # Index for simulations with output
        fidx = (pyr_mat[:, 0, 0] >= 0)

        # Average population
        pyr_mat_avg = np.mean(pyr_mat[fidx, :, :], axis=0)

        # CRS calculations
        XDAT = np.arange(start_year, start_year+run_years) + 0.5 - 2025
        fname = 'fert_dat_{:s}.csv'.format(demog_set)
        fnabs = os.path.abspath(os.path.join('Assets', 'data', fname))
        (frt_brth, crs_prob_vec) = crs_proc(fnabs, XDAT, pyr_mat_avg, ss_demog)

        # Normalize timeseries required for CRS calculation
        brth_vec = np.mean(birth_mat[fidx, :], axis=0)

        gidx = fidx
        inf_mat_avg = np.mean(inf_mat[gidx, :, :], axis=0)
        crs_mat = inf_mat_avg*np.transpose(crs_prob_vec)
        ydat = np.sum(crs_mat, axis=1)/brth_vec*1e5

        axs01.plot(XDAT, ydat, label=dirname[1], lw=3)

    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.savefig('fig_DRC90_01.svg')
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
