# *****************************************************************************

import json
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# Ought to go in emodpy
sys.path.append(os.path.abspath(os.path.join('..', '..', 'local_python')))
sys.path.append(os.path.abspath(os.path.join('..', 'Assets', 'python')))

from global_data import run_years
from refdat_location_admin02 import data_dict as ref_longlatref

# *****************************************************************************

# Calculated haversine distance
def demoCalc_hDist(lat1, long1, lat2, long2):

  lat1  = np.pi*lat1 /180.0
  lat2  = np.pi*lat2 /180.0
  long1 = np.pi*long1/180.0
  long2 = np.pi*long2/180.0

  delt = 6371*2*np.arcsin(np.sqrt(np.sin(0.5*lat2-0.5*lat1)**2 +
                     np.cos(lat2)*np.cos(lat1)*np.sin(0.5*long2-0.5*long1)**2))

  return delt

# *****************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_noSIAs',
            'experiment_cVDPV2_NGA_100km_SIAs']

TITLES = ['May 2017 Outbreak\nNo SIAs Post Cessation',
          'May 2017 Outbreak\nEMOD SIA Calendar through Outbreak']

INIT_NAME = 'AFRO:NIGERIA:KANO:KANO_MUNICIPAL'

# *****************************************************************************

nfigs = len(DIRNAMES)

# Figure setup
fig01 = plt.figure(figsize=(8*nfigs,6))

for k1 in range(len(DIRNAMES)):
  dirval = DIRNAMES[k1]

  axs01 = fig01.add_subplot(1, nfigs, k1+1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_title(TITLES[k1],fontsize=14)

  axs01.set_ylabel('Distance from Emergence (km)  [Max 873]',fontsize=14)

  axs01.set_xlim( 0, 750)
  axs01.set_ylim( 0, 1000)

  dvals  = [0]+[31,30,31,31,30,31,30,31,31,28,31,30]*2
  ticloc = np.cumsum(dvals)
  ticlab = ['']*25
  axs01.plot([245,245],[0,1000],'k:')
  axs01.plot([610,610],[0,1000],'k:')
  axs01.text(31.5,    -50,'2016', fontsize=14)
  axs01.text(31.5+365,-50,'2017', fontsize=14)

  axs01.set_xticks(ticks=ticloc)
  axs01.set_xticklabels(ticlab)

  # Sim outputs
  tpath = os.path.join('..',dirval)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick  = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  node_names = data_brick.pop('node_names')
  n_sims     = param_dict['NUM_SIMS']
  n_tstep    = int(365.0*run_years)
  n_nodes    = len(node_names)

  init_xy   = ref_longlatref[INIT_NAME]
  dist_vec  = np.zeros((n_nodes))
  for nname in node_names:
    curr_xy  = ref_longlatref[nname]
    curr_idx = node_names[nname]-1
    dist_vec[curr_idx] = demoCalc_hDist(curr_xy[1],curr_xy[0],init_xy[1],init_xy[0])

  tot_inf = np.zeros((n_sims, n_tstep))
  vel_mat = np.zeros((n_sims, n_nodes))
  for sim_idx_str in data_brick:
    sim_idx = int(sim_idx_str)
    tot_inf[sim_idx,:] = np.cumsum(np.array(data_brick[sim_idx_str]['totinf']))
    vel_mat[sim_idx,:] = np.array(data_brick[sim_idx_str]['fatime'])

  max_vel = np.zeros((n_sims, n_tstep))
  for k2 in range(n_tstep):
    for k3 in range(n_sims):
      tnodes = (vel_mat[k3,:]<k2)&(vel_mat[k3,:]>0)
      if(np.sum(tnodes)>0):
        max_vel[k3,k2] = np.max(dist_vec[tnodes])

  gdix   = (tot_inf[:,-1]>5000)

  axs01.text(30,812.5,'Outbreak Probability: {:4.2f}'.format(np.sum(gdix)/n_sims),fontsize=14)

  xval   = np.arange(n_tstep)+0.0
  yval1  = np.mean(max_vel[gdix,:],axis=0)
  yval2  = max_vel[gdix,:]
  scplt1 = axs01.plot(xval, yval1, c='C0')
  for k3 in range(np.sum(gdix)):
    scplt2 = axs01.plot(xval[5::10], yval2[k3,5::10], '.', c='C0')

# Generate figure
plt.tight_layout()
plt.savefig('fig_extent_max_01.png')
plt.close()

#*******************************************************************************
