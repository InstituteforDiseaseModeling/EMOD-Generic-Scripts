#*******************************************************************************

import os, json, sys

import numpy              as np
import matplotlib.pyplot  as plt

sys.path.append(os.path.join('..','Assets','python'))

EPS = np.finfo(np.float32).eps

#*******************************************************************************

from refdat_location_admin02 import data_dict as ref_longlatref

#*******************************************************************************

# Calculated haversine distance
def h_dist(lat1=0.0, long1=0.0, lat2=0.0, long2=0.0):

  lat1  = np.pi*lat1 /180.0
  lat2  = np.pi*lat2 /180.0
  long1 = np.pi*long1/180.0
  long2 = np.pi*long2/180.0

  delt = 6371*2*np.arcsin(np.sqrt(np.sin(0.5*lat2-0.5*lat1)**2 +
                     np.cos(lat2)*np.cos(lat1)*np.sin(0.5*long2-0.5*long1)**2))

  return delt
 
#*******************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_noSIAs',
            'experiment_cVDPV2_NGA_100km_SIAs']

TITLES   = ['May 2017 Outbreak\nNo SIAs Post Cessation',
            'May 2017 Outbreak\nEMOD SIA Calendar through Outbreak']

INIT_NAME = 'AFRO:NIGERIA:KANO:KANO_MUNICIPAL'

for k1 in range(len(DIRNAMES)):
  dirval = DIRNAMES[k1]

  # Figure setup
  fig01 = plt.figure(figsize=(8,6))
  axs01 = fig01.add_subplot(111,label=None)
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

  with open(os.path.join(tpath,'output','node_names.json')) as fid01:
    node_name_dict = json.load(fid01)

  with open(os.path.join(tpath,'data_fatime.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'data_totinf.json')) as fid01:
    inf_brick  = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  n_sims   = param_dict['NUM_SIMS']
  n_tstep  = int(param_dict['EXP_CONSTANT']['num_tsteps'])
  n_nodes  = len(node_name_dict)

  init_xy   = ref_longlatref[INIT_NAME]
  dist_vec  = np.zeros((n_nodes))
  for nname in node_name_dict:
    curr_xy  = ref_longlatref[nname]
    curr_idx = node_name_dict[nname]-1
    dist_vec[curr_idx] = h_dist(curr_xy[1],curr_xy[0],init_xy[1],init_xy[0])

  vel_mat = np.zeros((n_sims, n_nodes))
  for sim_idx_str in data_brick:
    sim_idx = int(sim_idx_str)
    vel_mat[sim_idx,:] = np.array(data_brick[sim_idx_str])

  tot_inf = np.zeros((n_sims, n_tstep))
  for sim_idx_str in inf_brick:
    sim_idx = int(sim_idx_str)
    tot_inf[sim_idx,:] = np.cumsum(np.array(inf_brick[sim_idx_str]))

  max_vel = np.zeros((n_sims, n_tstep))
  for k2 in range(n_tstep):
    for k3 in range(n_sims):
      tnodes = (vel_mat[k3,:]<k2)&(vel_mat[k3,:]>0)
      if(np.sum(tnodes)>0):
        max_vel[k3,k2] = np.max(dist_vec[tnodes])

  gdex   = (tot_inf[:,-1]>5000)

  axs01.text(30,812.5,'Outbreak Probability: {:4.2f}'.format(np.sum(gdex)/n_sims),fontsize=14)

  xval   = np.arange(n_tstep)+0.0
  yval1  = np.mean(max_vel[gdex,:],axis=0)
  yval2  = max_vel[gdex,:]
  scplt1 = axs01.plot(xval, yval1, c='C0')
  for k3 in range(np.sum(gdex)):
    scplt2 = axs01.plot(xval[5::10], yval2[k3,5::10], '.', c='C0')

  # Generate figure
  #plt.savefig(os.path.join('fig_extent_max_{:s}_01.png'.format(dirval)))
  plt.savefig(os.path.join('fig_extent_max_{:s}_01.svg'.format(dirval)))

  plt.close()

#*******************************************************************************
