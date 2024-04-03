# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
LOCAL_PATH = os.path.abspath(os.path.join('..', '..', 'local_python'))
sys.path.insert(0, LOCAL_PATH)
from py_assets_common.emod_constants import EXP_V, NUM_SIMS

# *****************************************************************************

DIRNAME = 'experiment_demog_UK01_calib'

# *****************************************************************************


def make_fig():

    # Sim outputs
    tpath = os.path.join('..', DIRNAME)

    # Create figure
    fig01 = plt.figure(figsize=(24, 6))

    axs01 = fig01.add_subplot(1, 3, 1)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlim(-4.0, 4.0)
    axs01.set_ylim(-4.0, 4.0)

    axs01.set_xlabel('Log Mortality Multiplier: <15yrs',     fontsize=14)
    axs01.set_ylabel('Log Mortality Multiplier: 15 - 50yrs', fontsize=14)

    axs02 = fig01.add_subplot(1, 3, 2)
    plt.sca(axs02)

    axs02.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs02.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs02.set_axisbelow(True)

    axs02.set_xlim(-4.0, 4.0)
    axs02.set_ylim(-4.0, 4.0)

    axs02.set_xlabel('Log Mortality Multiplier: <15yrs',     fontsize=14)
    axs02.set_ylabel('Log Mortality Multiplier: 50 - 80yrs', fontsize=14)

    axs03 = fig01.add_subplot(1, 3, 3)
    plt.sca(axs03)

    axs03.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs03.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs03.set_axisbelow(True)

    axs03.set_xlim(-4.0, 4.0)
    axs03.set_ylim(-4.0, 4.0)

    axs03.set_xlabel('Log Mortality Multiplier: 15 - 50yrs', fontsize=14)
    axs03.set_ylabel('Log Mortality Multiplier: 50 - 80yrs', fontsize=14)

    x1data = list()
    x2data = list()
    x3data = list()
    cdata = list()

    # Plot scatter data
    with open(os.path.join(tpath, 'param_dict_iters.json')) as fid01:
        param_dict = json.load(fid01)

    with open(os.path.join(tpath, 'data_brick_iters.json')) as fid01:
        data_brick = json.load(fid01)

    for inum_str in param_dict:

        nsims = int(param_dict[inum_str][NUM_SIMS])

        x1data.extend(param_dict[inum_str][EXP_V]['log_mort_mult01'])
        x2data.extend(param_dict[inum_str][EXP_V]['log_mort_mult02'])
        x3data.extend(param_dict[inum_str][EXP_V]['log_mort_mult03'])

        calib_vec = np.zeros(nsims) + 1
        for sim_idx_str in data_brick[inum_str]:
            sim_idx = int(sim_idx_str)
            calib_vec[sim_idx] = data_brick[inum_str][sim_idx_str]['cal_val']
        cdata.extend(calib_vec.tolist())

    cdata = np.array(cdata)
    fidx = (cdata < 0)
    cdata = cdata[fidx]
    x1data = np.array(x1data)[fidx]
    x2data = np.array(x2data)[fidx]
    x3data = np.array(x3data)[fidx]
    sidx = np.argsort(cdata)

    axs01.scatter(x1data[sidx], x2data[sidx], c=cdata[sidx], vmin=-20)
    axs02.scatter(x1data[sidx], x3data[sidx], c=cdata[sidx], vmin=-20)
    axs03.scatter(x2data[sidx], x3data[sidx], c=cdata[sidx], vmin=-20)

    max_dex = np.argsort(cdata)
    print(cdata[max_dex[-3:]])
    print(x1data[max_dex[-3:]])
    print(x2data[max_dex[-3:]])
    print(x3data[max_dex[-3:]])

    # Save figure
    plt.tight_layout()
    plt.savefig('fig_calib_01.png')
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
