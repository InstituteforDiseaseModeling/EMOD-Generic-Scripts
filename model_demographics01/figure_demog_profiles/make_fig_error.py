# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
REL_PATH = os.path.join('..', '..', 'local_python', 'py_assets_common')
sys.path.insert(0, os.path.abspath(REL_PATH))
from emod_constants import P_FILE, EXP_V, NUM_SIMS, POP_PYR

# *****************************************************************************

DIRNAME = 'experiment_demog_UK01_sweep'

# *****************************************************************************


def make_fig():

    # Sim outputs
    tpath = os.path.join('..', DIRNAME)

    with open(os.path.join(tpath, 'data_brick.json')) as fid01:
        data_brick = json.load(fid01)

    with open(os.path.join(tpath, P_FILE)) as fid01:
        param_dict = json.load(fid01)

    N_SIMS = int(param_dict[NUM_SIMS])
    VAR_SET = np.array(param_dict[EXP_V]['variable_birthrate'])
    AGE_SET = np.array(param_dict[EXP_V]['modified_age_init'])
    MORT_SET = -np.array(param_dict[EXP_V]['log_mort_mult03'])

    pyr_mat = np.zeros((N_SIMS, 30+1, 20))-1
    for sim_idx_str in data_brick:
        sim_idx = int(sim_idx_str)
        pyr_mat[sim_idx, :, :] = np.array(data_brick[sim_idx_str][POP_PYR])

    fidx = (pyr_mat[:, 0, 0] >= 0)

    calib_vec = np.zeros(N_SIMS)
    error_pop = np.zeros(N_SIMS)
    for sim_idx_str in data_brick:
        sim_idx = int(sim_idx_str)
        calib_vec[sim_idx] = data_brick[sim_idx_str]['cal_val']
        error_pop[sim_idx] = data_brick[sim_idx_str]['pop_err']

    # Figures
    fig01 = plt.figure(figsize=(8, 6))

    axs01 = fig01.add_subplot(1, 1, 1, label=None)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlim(-0.5, 3.5)
    axs01.set_ylim(0, 70)

    ticloc = [0, 1, 2, 3]
    ticlab = ['', '', '', '']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab, fontsize=14)

    axs01.set_ylabel('Error Metric', fontsize=14)

    p_tuple = [(VAR_SET[k1], AGE_SET[k1], MORT_SET[k1])
               for k1 in range(N_SIMS)]
    p_tuple = sorted(list(set(p_tuple)))

    for k0 in range(len(p_tuple)):
        pt = p_tuple[k0]
        gidx = fidx & (VAR_SET == pt[0]) & \
                      (AGE_SET == pt[1]) & \
                      (MORT_SET == pt[2])

        calib_set = -calib_vec[gidx]
        error_set = -error_pop[gidx]

        axs01.plot(k0+0*calib_set, calib_set, '.', c='C{:d}'.format(k0))

        clr_val = 'C{:d}'.format(k0)
        error_pyr = calib_set-error_set
        axs01.plot(k0, np.mean(error_set), '+', ms=16, mew=4, c=clr_val)
        axs01.plot(k0, np.mean(error_pyr), 'x', ms=16, mew=4, c=clr_val)
        axs01.plot(k0, np.mean(calib_set), 'o', ms=16, mew=4, c=clr_val)

    ticloc = [-0.5, 0.5, 1.5, 2.5]
    ticlab = ['      Equilib Demog',
              '   +Birth Rate Data',
              '  +Initial Age Data',
              '   +Mortality Calib']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab, ha='left', fontsize=12)

    axs01.text(2.30, 62.0, 'Sum', fontsize=18, va='center')
    axs01.text(2.30, 58.0, 'Total Pop', fontsize=18, va='center')
    axs01.text(2.30, 54.0, 'Pyramid', fontsize=18, va='center')

    axs01.plot(2.20, 62.0, 'o', ms=12, mew=3, c='k')
    axs01.plot(2.20, 58.0, '+', ms=13, mew=3, c='k')
    axs01.plot(2.20, 54.0, 'x', ms=13, mew=3, c='k')

    # Save figure
    plt.tight_layout()
    plt.savefig('fig_error_01.png')
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
