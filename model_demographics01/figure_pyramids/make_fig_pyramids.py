#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process import tpop_xval, tpop_yval

from dtk_post_process import pop_age_days
from dtk_post_process import uk_1950_frac, uk_1960_frac
from dtk_post_process import uk_1970_frac, uk_1980_frac

#*******************************************************************************

DIRNAME = 'experiment_demog_UK01_sweep'

xvals   = np.array(tpop_xval)
yref    = np.array(tpop_yval)/1e6

CM    = np.array([ 70,130,180])/255
CF    = np.array([238,121,137])/255
SYEAR = 50


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
var_set  = np.array(param_dict['EXP_VARIABLE']['variable_birthrate'])
age_set  = np.array(param_dict['EXP_VARIABLE']['modified_age_init'])
mort_set = np.array(param_dict['EXP_VARIABLE']['log_mort_mult03'])

pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))-1
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_dat'])

fidx = (pyr_mat[:,0,0]>=0)

demog_lev = [False,  True,  True,  True]
mod_init  = [False, False,  True,  True]
mort_mul  = [  0.0,   0.0,   0.0,  0.28]

x_dat_list = [uk_1950_frac, uk_1960_frac, uk_1970_frac, uk_1980_frac]

for k0 in range(len(demog_lev)):

  fig01 = plt.figure(figsize=(24,12))
  gidx  = fidx & (var_set==demog_lev[k0]) & (age_set==mod_init[k0]) & (mort_set==mort_mul[k0])

  pyr_mat_avg = np.mean(pyr_mat[gidx,:,:],axis=0)
  pyr_mat_std = np.std(pyr_mat[gidx,:,:],axis=0)

  # Figures - Sims
  for k1 in range(0, pyr_mat_avg.shape[0], 10):

    axs01 = fig01.add_subplot(int('24{:d}'.format(int(k1/10)+1)), label=None)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Percentage', fontsize=14)
    axs01.set_ylabel('Age (yrs)', fontsize=14)

    if(k1 == 30):
      axs02 = axs01.twinx()
      axs02.set_ylabel('Simulation', fontsize=24)
      axs02.set_yticks(ticks=[0,1])
      axs02.set_yticklabels(['',''])

    axs01.set_xlim(  -8,   8)
    axs01.set_ylim(   0, 100)

    ticloc = [-8, -6, -4, -2, 0, 2, 4, 6, 8]
    ticlab = ['8', '6', '4', '2', '0', '2', '4', '6', '8']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab)

    ydat        = np.array(pop_age_days)/365.0 - 2.5
    pop_dat     = pyr_mat_avg[k1,:]
    pop_dat_err = pyr_mat_std[k1,:]
    tpop        = np.sum(pop_dat)
    effpop      = tpop/100000*yref[0]

    pop_dat_n     = 100*pop_dat/tpop
    pop_dat_n_err = 100*pop_dat_err/tpop

    axs01.barh(ydat[1:],  pop_dat_n/2.0, height=4.75, xerr=pop_dat_n_err, color=CF)
    axs01.barh(ydat[1:], -pop_dat_n/2.0, height=4.75, xerr=pop_dat_n_err, color=CM)

    axs01.text( -7, 92.5, '{:04d}'.format(1950+k1), fontsize=18)
    axs01.text(  3, 87.5, 'Total Pop\n{:6.3f}M'.format(effpop), fontsize=18)

  # Figures - Reference

  for k1 in range(len(x_dat_list)):

    axs01 = fig01.add_subplot(int('24{:d}'.format(k1+4+1)), label=None)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Percentage', fontsize=14)
    axs01.set_ylabel('Age (yrs)', fontsize=14)

    if(k1 == 3):
      axs02 = axs01.twinx()
      axs02.set_ylabel('Reference', fontsize=24)
      axs02.set_yticks(ticks=[0,1])
      axs02.set_yticklabels(['',''])

    axs01.set_xlim(  -8,   8)
    axs01.set_ylim(   0, 100)

    ticloc = [-8, -6, -4, -2, 0, 2, 4, 6, 8]
    ticlab = ['8', '6', '4', '2', '0', '2', '4', '6', '8']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab)

    ydat        = np.array(pop_age_days)/365.0 - 2.5
    pop_dat     = np.array(x_dat_list[k1])
    effpop      = yref[10*k1]

    axs01.barh(ydat[1:],  100*pop_dat[1:]/2.0, height=4.75, color=CF)
    axs01.barh(ydat[1:], -100*pop_dat[1:]/2.0, height=4.75, color=CM)

    axs01.text( -7, 92.5, '{:04d}'.format(1950+10*k1), fontsize=18)
    axs01.text(  3, 87.5, 'Total Pop\n{:6.3f}M'.format(effpop), fontsize=18)

  plt.tight_layout()
  plt.savefig('fig_pyr_set{:02d}_01.png'.format(k0+1))
  plt.close()

#*******************************************************************************
