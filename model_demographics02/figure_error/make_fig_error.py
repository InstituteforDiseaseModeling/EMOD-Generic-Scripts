# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
LOCAL_PATH = os.path.abspath(os.path.join('..', '..', 'local_python'))
sys.path.insert(0, LOCAL_PATH)
from py_assets_common.emod_constants import EXP_C, NUM_SIMS, P_FILE, POP_PYR

# *****************************************************************************

DIRNAMES = ['experiment_demog_WPP_estimates01',
            'experiment_demog_WPP_projections01']

# *****************************************************************************


def make_fig():

    # Figure
    fig01 = plt.figure(figsize=(8, 6))

    axs01 = fig01.add_subplot(1, 1, 1)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Year', fontsize=14)
    axs01.set_ylabel('Error - Total Population (%)', fontsize=14)

    axs01.set_xlim(1950, 2090)
    axs01.set_ylim(-20, 20)

    ticloc = np.arange(1950, 2100, 10)
    ticlab = ['1950', '', '1970', '', '1990', '', '2010', '',
              '2030', '', '2050', '', '2070', '', '2090']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab)

    ticloc = np.arange(-20, 21, 5)
    ticlab = ['-20', '-15', '-10', '-5', '0',
              '5', '10', '15', '20']
    axs01.set_yticks(ticks=ticloc)
    axs01.set_yticklabels(ticlab)

    axs01.plot([1950, 2090], [0, 0], c=[0.4, 0.4, 0.4])

    # Sim outputs
    for dirname in DIRNAMES:
        tpath = os.path.join('..', dirname)

        with open(os.path.join(tpath, 'data_brick.json')) as fid01:
            data_brick = json.load(fid01)

        with open(os.path.join(tpath, P_FILE)) as fid01:
            param_dict = json.load(fid01)

        nsims = int(param_dict[NUM_SIMS])
        init_year = int(param_dict[EXP_C]['start_year'])
        num_years = int(param_dict[EXP_C]['num_years'])
        pop_dat_str = param_dict[EXP_C]['pop_dat_file']

        pyr_mat = np.zeros((nsims, num_years+1, 20))-1
        year_vec = np.arange(init_year, init_year+num_years+1)
        chart_yrs = year_vec[np.mod(year_vec, 5) == 0]

        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            pyr_mat[sim_idx, :, :] = np.array(data_brick[sim_idx_str][POP_PYR])

        fidx = (pyr_mat[:, 0, 0] >= 0)

        popfile = 'pop_dat_{:s}.csv'.format(pop_dat_str)
        fname_pop = os.path.join('..', 'Assets', 'data', popfile)
        pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

        year_vec_dat = pop_input[0, :]
        pop_mat_dat = pop_input[1:, :]
        tpop_dat = np.sum(pop_mat_dat, axis=0)

        pyr_mat_avg = np.mean(pyr_mat[fidx, :, :], axis=0)
        tpop_avg = np.sum(pyr_mat_avg, axis=1)

        yidx = np.intersect1d(chart_yrs, year_vec, return_indices=True)[2]
        y_sim = tpop_avg[yidx]

        yidx = np.intersect1d(chart_yrs, year_vec_dat, return_indices=True)[2]
        y_ref = tpop_dat[yidx]

        axs01.plot(chart_yrs, 100*(y_sim-y_ref)/y_ref,
                   c='k', marker='.', ms=14)

    # Save figure
    plt.tight_layout()
    plt.savefig('fig_err_{:s}_01.png'.format(pop_dat_str))
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
