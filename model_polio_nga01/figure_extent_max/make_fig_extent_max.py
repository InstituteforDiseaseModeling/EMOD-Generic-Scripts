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
from py_assets_common.emod_local_proc import haversine_dist
from global_data import run_years, base_year, seed_inf_loc
from refdat_location_admin02 import data_dict as ref_longlatref

# *****************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_noSIAs',
            'experiment_cVDPV2_NGA_100km_SIAs']

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
        node_names = data_brick.pop('node_names')
        n_sims = param_dict[NUM_SIMS]
        n_nodes = len(node_names)

        i_xy = ref_longlatref[seed_inf_loc]
        c_long = [ref_longlatref[nname][0] for nname in node_names]
        c_lat = [ref_longlatref[nname][1] for nname in node_names]
        dist_vec = haversine_dist(c_lat, c_long, i_xy[1], i_xy[0])

        tot_inf = np.zeros((n_sims, tvec.shape[0]))
        vel_mat = np.zeros((n_sims, n_nodes))
        for sim_idx_str in data_brick:
            sim_idx = int(sim_idx_str)
            tinf = np.array(data_brick[sim_idx_str]['totinf'])
            vinf = np.array(data_brick[sim_idx_str]['fatime'])
            tot_inf[sim_idx, :] = np.cumsum(tinf)
            vel_mat[sim_idx, :] = vinf

        max_vel = np.zeros((n_sims, t_vec.shape[0]))
        for k2 in range(t_vec.shape[0]):
            for k3 in range(n_sims):
                tnodes = (vel_mat[k3, :] < k2) & (vel_mat[k3, :] > 0)
                if (np.sum(tnodes) > 0):
                    max_vel[k3, k2] = np.max(dist_vec[tnodes])

        gdix = (tot_inf[:, -1] > 5000)

        # Figure setup
        fig01 = plt.figure(figsize=(8, 6))

        axs01 = fig01.add_subplot(1, 1, 1)
        plt.sca(axs01)

        axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
        axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
        axs01.set_axisbelow(True)

        #dvals = [0]+MO_DAYS*2
        #ticloc = np.cumsum(dvals)
        #ticlab = ['']*25
        #axs01.plot([245, 245], [0, 1000], 'k:')
        #axs01.plot([610, 610], [0, 1000], 'k:')
        #axs01.text(31.5, -50, '2016', fontsize=14)
        #axs01.text(31.5+365, -50, '2017', fontsize=14)

        #axs01.set_xticks(ticks=ticloc)
        #axs01.set_xticklabels(ticlab)

        obp_lab = 'Outbreak Probability: {:4.2f}'.format(np.sum(gdix)/n_sims)
        axs01.text(2017.3, 812.5, obp_lab, fontsize=14)

        xval = t_vec/365 + base_year
        yval1 = np.mean(max_vel[gdix, :], axis=0)
        yval2 = max_vel[gdix, :]
        axs01.plot(xval, yval1, c='C0')
        for k3 in range(np.sum(gdix)):
            axs01.plot(xval[::2], yval2[k3, ::2], '.', c='C0')

        axs01.set_ylabel('Distance from Emergence (km)', fontsize=14)
        axs01.set_xlim(xval[0], xval[-1])
        axs01.set_ylim(0, 1000)

        plt.tight_layout()
        plt.savefig('fig_extent_max_{:s}_01.png'.format(dirname))
        plt.close()

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    make_fig()

# *****************************************************************************
