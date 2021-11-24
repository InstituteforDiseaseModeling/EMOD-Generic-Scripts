#*******************************************************************************

import os, json

import numpy              as np
import matplotlib.pyplot  as plt

EPS = np.finfo(np.float32).eps

#*******************************************************************************

DIRNAMES = ['experiment_cVDPV2_NGA_100km_noSIAs',
            'experiment_cVDPV2_NGA_100km_SIAs']

TITLES   = ['May 2017 Outbreak\nNo SIAs Post Cessation',
            'May 2017 Outbreak\nEMOD SIA Calendar through Outbreak']

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
  axs01.set_ylabel('Cumulative Total Infections',fontsize=14)

  axs01.set_xlim( 0, 750)
  axs01.set_ylim( 0, 400e3)

  dvals  = [0]+[31,30,31,31,30,31,30,31,31,28,31,30]*2
  ticloc = np.cumsum(dvals)
  ticlab = ['']*25
  axs01.plot([245,245],[0,400e3],'k:')
  axs01.plot([610,610],[0,400e3],'k:')
  axs01.text(31.5,    -2e4,'2016', fontsize=14)
  axs01.text(31.5+365,-2e4,'2017', fontsize=14)

  axs01.set_xticks(ticks=ticloc)
  axs01.set_xticklabels(ticlab)

  ticloc = [0.5e5,1.0e5,1.5e5,2.0e5,2.5e5,3.0e5,3.5e5,4.0e5]
  ticlab = ['50k','100k','150k','200k','250k','300k','350k','400k']

  axs01.set_yticks(ticks=ticloc)
  axs01.set_yticklabels(ticlab)

  # Sim outputs
  tpath = os.path.join('..',dirval)

  with open(os.path.join(tpath,'output','node_names.json')) as fid01:
    node_name_dict = json.load(fid01)

  with open(os.path.join(tpath,'data_totinf.json')) as fid01:
    inf_brick  = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  n_sims   = param_dict['NUM_SIMS']
  n_tstep  = int(param_dict['EXP_CONSTANT']['num_tsteps'])
  n_nodes  = len(node_name_dict)

  tot_inf = np.zeros((n_sims, n_tstep))
  for sim_idx_str in inf_brick:
    sim_idx = int(sim_idx_str)
    tot_inf[sim_idx,:] = np.cumsum(np.array(inf_brick[sim_idx_str]))

  gdex   = (tot_inf[:,-1]>5000)

  axs01.text(30,325e3,'Outbreak Probability: {:4.2f}'.format(np.sum(gdex)/n_sims),fontsize=14)
  
  xval   = np.arange(n_tstep) + 0.0
  yval1  = np.mean(tot_inf[gdex,:],axis=0)
  yval2  = tot_inf[gdex,:]
  scplt1 = axs01.plot(xval, yval1, c='C0')
  for k3 in range(np.sum(gdex)):
    scplt2 = axs01.plot(xval[5::10], yval2[k3,5::10], '.', c='C0')

  # Generate figure
  #plt.savefig(os.path.join('fig_burden_{:s}_01.png'.format(dirval)))
  plt.savefig(os.path.join('fig_burden_{:s}_01.svg'.format(dirval)))

  plt.close()

#*******************************************************************************
