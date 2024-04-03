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
                                            EXP_V, NUM_SIMS, P_FILE, POP_PYR

# *****************************************************************************

DIRNAME = 'experiment_demog_UK01_sweep'

TLABS = ['8', '6', '4', '2', '0', '2', '4', '6', '8']
TLOCS = [-8, -6, -4, -2, 0, 2, 4, 6, 8]

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

    sim_pop_list = list()
    pyr_mat = np.zeros((N_SIMS, 30+1, 20))-1
    for sim_idx_str in data_brick:
        sim_idx = int(sim_idx_str)
        pyr_mat[sim_idx, :, :] = np.array(data_brick[sim_idx_str][POP_PYR])

    fidx = (pyr_mat[:, 0, 0] >= 0)

    # Reference data
    popfile = 'pop_dat_GBR.csv'
    fname_pop = os.path.join('..', 'Assets', 'data', popfile)
    pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')
    year_vec = pop_input[0, :]
    pop_mat = pop_input[1:, :]

    pop_mat_ref = np.zeros((pop_mat.shape[0], 30+1))
    for yr_idx in range(30+1):
        yr_val = yr_idx + 1950
        pop_vec_ref = [np.interp(yr_val, year_vec, pop_mat[idx, :])
                       for idx in range(pop_mat.shape[0])]
        pop_mat_ref[:, yr_idx] = pop_vec_ref

    p_tuple = [(VAR_SET[k1], AGE_SET[k1], MORT_SET[k1])
               for k1 in range(N_SIMS)]
    p_tuple = sorted(list(set(p_tuple)))

    # Pyramid figures
    for k0 in range(len(p_tuple)):
        fig01 = plt.figure(figsize=(24, 12))
        pt = p_tuple[k0]
        gidx = fidx & (VAR_SET == pt[0]) & \
                      (AGE_SET == pt[1]) & \
                      (MORT_SET == pt[2])

        pyr_mat_avg = np.mean(pyr_mat[gidx, :, :], axis=0)
        pyr_mat_std = np.std(pyr_mat[gidx, :, :], axis=0)

        sim_pop_list.append(np.sum(pyr_mat_avg, axis=1))

        for k1 in range(0, pyr_mat_avg.shape[0], 10):

            # Figures - Sims
            axs01 = fig01.add_subplot(2, 4, int(k1/10)+1, label=None)
            plt.sca(axs01)

            axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
            axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
            axs01.set_axisbelow(True)

            axs01.set_xlabel('Percentage', fontsize=14)
            axs01.set_ylabel('Age (yrs)', fontsize=14)

            if (k1 == 30):
                axs02 = axs01.twinx()
                axs02.set_ylabel('Simulation', fontsize=24)
                axs02.set_yticks(ticks=[0, 1])
                axs02.set_yticklabels(['', ''])

            axs01.set_xlim(-8, 8)
            axs01.set_ylim(0, 100)

            axs01.set_xticks(ticks=TLOCS)
            axs01.set_xticklabels(TLABS)

            ydat = np.array(POP_AGE_DAYS)/365.0 - 2.5
            pop_dat = pyr_mat_avg[k1, :]
            pop_dat_err = pyr_mat_std[k1, :]
            tpop = np.sum(pop_dat)

            pop_dat_n = 100*pop_dat/tpop
            pop_dat_n_err = 100*pop_dat_err/tpop

            axs01.barh(ydat[1:], pop_dat_n/2.0, height=4.75,
                       xerr=pop_dat_n_err, color=CLR_F)
            axs01.barh(ydat[1:], -pop_dat_n/2.0, height=4.75,
                       xerr=pop_dat_n_err, color=CLR_M)

            txt_str = 'Total Pop\n{:6.3f}M'.format(tpop/1.0e6)
            axs01.text(-7, 92.5, '{:04d}'.format(1950+k1), fontsize=18)
            axs01.text(3, 87.5, txt_str, fontsize=18)

            # Figures - Reference
            axs01 = fig01.add_subplot(2, 4, int(k1/10)+1+4, label=None)
            plt.sca(axs01)

            axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
            axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
            axs01.set_axisbelow(True)

            axs01.set_xlabel('Percentage', fontsize=14)
            axs01.set_ylabel('Age (yrs)', fontsize=14)

            if (k1 == 30):
                axs02 = axs01.twinx()
                axs02.set_ylabel('Reference', fontsize=24)
                axs02.set_yticks(ticks=[0, 1])
                axs02.set_yticklabels(['', ''])

            axs01.set_xlim(-8, 8)
            axs01.set_ylim(0, 100)

            axs01.set_xticks(ticks=TLOCS)
            axs01.set_xticklabels(TLABS)

            ydat = np.array(POP_AGE_DAYS)/365.0 - 2.5
            pop_dat = pop_mat_ref[:, k1]
            tpop = np.sum(pop_dat)
            pop_dat = pop_dat[:-1]/tpop

            axs01.barh(ydat[1:], 100*pop_dat/2.0, height=4.75, color=CLR_F)
            axs01.barh(ydat[1:], -100*pop_dat/2.0, height=4.75, color=CLR_M)

            txt_str = 'Total Pop\n{:6.3f}M'.format(tpop/1.0e6)
            axs01.text(-7, 92.5, '{:04d}'.format(1950+k1), fontsize=18)
            axs01.text(3, 87.5, txt_str, fontsize=18)

        # Save figure
        plt.tight_layout()
        plt.savefig('fig_pyr_set{:02d}_01.png'.format(k0+1))
        plt.close()

    # Total pop figure
    fig01 = plt.figure(figsize=(8, 6))

    axs01 = fig01.add_subplot(1, 1, 1, label=None)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Year', fontsize=14)
    axs01.set_ylabel('UK Population (M)', fontsize=14)

    axs01.set_xlim(0, 30)
    axs01.set_ylim(48, 58)

    ticloc = [0, 5, 10, 15, 20, 25, 30]
    ticlab = ['1950', '1955', '1960', '1965', '1970', '1975', '1980']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab, fontsize=14)

    ticloc = [48, 50, 52, 54, 56, 58]
    ticlab = ['48', '50', '52', '54', '56', '58']
    axs01.set_yticks(ticks=ticloc)
    axs01.set_yticklabels(ticlab, fontsize=14)

    lab_val = ['Equilib Demog', '+Birth Rate Data',
               '+Initial Age Data', '+Mortality Calib']
    for k1 in range(len(sim_pop_list)):
        sim_pop = sim_pop_list[k1]
        axs01.plot(sim_pop/1.0e6, label=lab_val[k1])
    axs01.plot(np.sum(pop_mat_ref, axis=0)/1.0e6, 'k.', ms=10)

    axs01.legend()

    plt.tight_layout()
    plt.savefig('fig_pop_tot_01.png')
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
