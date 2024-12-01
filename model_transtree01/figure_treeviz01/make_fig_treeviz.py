# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'local_python')))
from py_assets_common.emod_constants import EXP_V, NUM_SIMS, P_FILE, D_FILE

# *****************************************************************************

DIRNAME = 'experiment_transtree01'

# *****************************************************************************


def rec_tree(tree_dat, targ_id):

    subdat = tree_dat[tree_dat[:, 3] == targ_id, :]
    subtree = list()

    for k1 in range(subdat.shape[0]):
        addleaf = rec_tree(tree_dat, subdat[k1, 2])
        subtree.append([subdat[k1, 0], addleaf])

    return subtree

# *****************************************************************************


def print_branch(axs_id, leaf_list, c_yval, pxy=None):

    sort_leaf = sorted(leaf_list, key=lambda val: val[0], reverse=True)

    for leaf_val in sort_leaf:
        axs_id.plot(leaf_val[0], c_yval, marker='.', lw=0, c='r', ms=0.5)
        new_pxy = (leaf_val[0], c_yval)
        if (pxy):
            if (pxy[0] < new_pxy[0]):
                xdat = [pxy[0]+0.25, pxy[0]+0.5, pxy[0]+0.5, new_pxy[0]-0.25]
                ydat = [pxy[1],      pxy[1],     new_pxy[1], new_pxy[1]]
            else:  # Secondary infection on same timestep; edge case in seeding
                xdat = [pxy[0],   new_pxy[0]]
                ydat = [pxy[1]+1, new_pxy[1]-1]
            axs_id.plot(xdat, ydat, lw=0.5, c='k')
        c_yval = print_branch(axs_id, leaf_val[1], c_yval+5, new_pxy)

    return c_yval

# *****************************************************************************


def make_fig():

    # Sim outputs
    tpath = os.path.join('..', DIRNAME)

    with open(os.path.join(tpath, D_FILE)) as fid01:
        data_brick = json.load(fid01)

    with open(os.path.join(tpath, P_FILE)) as fid01:
        param_dict = json.load(fid01)

    BI_VAR = np.array(param_dict[EXP_V]['base_inf_stddev_mult'])
    nsims = int(param_dict[NUM_SIMS])

    tree_list = [np.array([]) for k1 in range(nsims)]
    for idx_str in data_brick:
        idx_val = int(idx_str)
        tree_list[idx_val] = np.array(data_brick[idx_str])

    # Simulations with outbreak
    obr_bool = np.array([tree.shape[0] > 100 for tree in tree_list])

    # Number of simulations at each level
    sim_num = np.array([np.sum(BI_VAR == 0.0),
                        np.sum(BI_VAR == 1.0)])

    # Number of simulations with outbreak at each level
    obr_num = np.array([np.sum(obr_bool[BI_VAR == 0.0]),
                        np.sum(obr_bool[BI_VAR == 1.0])])

    print(np.around(obr_num/sim_num, 3))

    gdex0 = np.argwhere(obr_bool & (BI_VAR == 0.0))[0, 0]
    gdex1 = np.argwhere(obr_bool & (BI_VAR == 1.0))[0, 0]

    # Figure setup
    fig01 = plt.figure(figsize=(16, 6))

    axs01 = fig01.add_subplot(1, 2, 1, label=None)
    plt.sca(axs01)

    tree_dat = tree_list[gdex0]
    tdelt = list()
    for k1 in range(tree_dat.shape[0]):
        for k2 in range(tree_dat.shape[0]):
            if (tree_dat[k2, 3] == tree_dat[k1, 2]):
                dt = tree_dat[k2, 0] - tree_dat[k1, 0]
                tdelt.append((dt, max(tree_dat[k2, 0], tree_dat[k1, 0])))

    td2 = sorted(tdelt, key=lambda ttup: ttup[1])
    td3 = [val[0] for val in td2]
    td4 = td3[:int(len(td3)/2)]

    ltxt = 'Mean = {:4.1f}'.format(np.mean(td4))
    # axs01.hist(td4, density=True, bins=np.arange(-0.5, 15), edgecolor='k')
    # axs01.text(0.1, 0.8, ltxt, transform=axs01.transAxes)
    # axs01.set_xlabel('Interval (days)')
    # axs01.set_title('Poisson')

    axs01 = fig01.add_subplot(1, 2, 2, label=None)
    plt.sca(axs01)

    tree_dat = tree_list[gdex1]
    tdelt = list()
    for k1 in range(tree_dat.shape[0]):
        for k2 in range(tree_dat.shape[0]):
            if (tree_dat[k2, 3] == tree_dat[k1, 2]):
                dt = tree_dat[k2, 0] - tree_dat[k1, 0]
                tdelt.append((dt, max(tree_dat[k2, 0], tree_dat[k1, 0])))

    td2 = sorted(tdelt, key=lambda ttup: ttup[1])
    td3 = [val[0] for val in td2]
    td4 = td3[(int(len(td3)/2)):]

    ltxt = 'Mean = {:4.1f}'.format(np.mean(td4))
    axs01.hist(td4, density=True, bins=np.arange(-0.5, 30), edgecolor='k')
    axs01.text(0.1, 0.8, ltxt, transform=axs01.transAxes)
    axs01.set_xlabel('Interval (days)')
    axs01.set_title('Negative Binomial')

    # Generate figures
    plt.tight_layout()
    plt.savefig('fig_transtree_01.png')
    plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
