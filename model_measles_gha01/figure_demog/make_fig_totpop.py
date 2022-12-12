#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process import tpop_xval, tpop_yval

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_base01'

xvals   = np.array(tpop_xval)
yref    = np.array(tpop_yval)/1e6

# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])

pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))
for sim_idx_str in data_brick:
  try:
    sim_idx = int(sim_idx_str)
  except:
    continue
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyramid'])

fidx = (pyr_mat[:,0,0]>=0)

# Figures
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('Ghana - Total Population (M)', fontsize=14)

axs01.set_xlim( 2007.5, 2027)
axs01.set_ylim(   22,     38)

ticloc = np.arange(2008, 2028)
ticlab = ['2008','','','','2012','','','',
          '2016','','','','2020','','','',
          '2024','','','']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab,fontsize=14)

axs01.tick_params(axis='x', labelsize=14)
axs01.tick_params(axis='y', labelsize=14)

pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
pyr_mat_std = np.std(pyr_mat[fidx,:,:],axis=0)

pop_dat     = np.sum(pyr_mat_avg,axis=1)
pop_dat_err = np.sum(pyr_mat_std,axis=1)
nyear       = pop_dat.shape[0]

yvals       = pop_dat/1e6
yvals_err   = pop_dat_err/1e6

axs01.errorbar(xvals[:nyear]-0.5, yvals, yerr=yvals_err, lw=2)
axs01.plot(xvals[:nyear], yref[:nyear], lw=0, c='k', marker='.', markersize=14, label='Data',zorder=4)

plt.tight_layout()
plt.savefig('fig_totpop_01.png')
plt.close()

#*******************************************************************************
