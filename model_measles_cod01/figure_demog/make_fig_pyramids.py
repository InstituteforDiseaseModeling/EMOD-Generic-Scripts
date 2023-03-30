#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process import tpop_xval, tpop_yval

from dtk_post_process import pop_age_days
from dtk_post_process import cod_2010_frac

#*******************************************************************************

DIRNAME = 'experiment_meas_cod_base01'

xvals   = np.array(tpop_xval)
yref    = np.array(tpop_yval)/1e6

CM    = np.array([ 70,130,180])/255
CF    = np.array([238,121,137])/255

# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
tvals_mo = data_brick.pop('tstamps')

pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))-1
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyramid'])

fidx = (pyr_mat[:,-1,0]>0)
x_dat_list = [cod_2010_frac]

fig01 = plt.figure(figsize=(14,6))

pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
pyr_mat_std = np.std(pyr_mat[fidx,:,:],axis=0)

# Figures - Sims
axs01 = fig01.add_subplot(1, 2, 1, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Percentage', fontsize=16)
axs01.set_ylabel('Age (yrs)', fontsize=16)

axs02 = axs01.twinx()
axs02.set_ylabel('Simulation', fontsize=18)
axs02.set_yticks(ticks=[0,1])
axs02.set_yticklabels(['',''])

axs01.set_xlim( -10,  10)
axs01.set_ylim(   0, 100)

ticloc = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
ticlab = ['-10','8', '6', '4', '2', '0', '2', '4', '6', '8', '10']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

ydat        = np.array(pop_age_days)/365.0 - 2.5
pop_dat     = pyr_mat_avg[4,:]
pop_dat_err = pyr_mat_std[4,:]
tpop        = np.sum(pop_dat)

pop_dat_n     = 100*pop_dat/tpop
pop_dat_n_err = 100*pop_dat_err/tpop

axs01.barh(ydat[1:],  pop_dat_n/2.0, height=4.75, xerr=pop_dat_n_err, color=CF)
axs01.barh(ydat[1:], -pop_dat_n/2.0, height=4.75, xerr=pop_dat_n_err, color=CM)

axs01.text(-7.5, 87.5, '2010', fontsize=20)
axs01.text( 5.0, 87.5, '{:4.1f}M'.format(tpop/1e6), fontsize=20)

# Figures - Reference
axs01 = fig01.add_subplot(1, 2, 2, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Percentage', fontsize=16)
#axs01.set_ylabel('Age (yrs)', fontsize=16)

axs02 = axs01.twinx()
axs02.set_ylabel('Reference', fontsize=18)
axs02.set_yticks(ticks=[0,1])
axs02.set_yticklabels(['',''])

axs01.set_xlim( -10,  10)
axs01.set_ylim(   0, 100)

ticloc = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
ticlab = ['-10', '8', '6', '4', '2', '0', '2', '4', '6', '8', '10']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

ydat        = np.array(pop_age_days)/365.0 - 2.5
pop_dat     = np.array(x_dat_list[0])
effpop      = yref[4]

axs01.barh(ydat[1:],  100*pop_dat[:-1]/2.0, height=4.75, color=CF)
axs01.barh(ydat[1:], -100*pop_dat[:-1]/2.0, height=4.75, color=CM)

axs01.text(-7.5, 87.5, '2010', fontsize=20)
axs01.text( 5.0, 87.5, '{:4.1f}M'.format(effpop), fontsize=20)

plt.tight_layout()
plt.savefig('fig_pyr_01.png')
plt.close()

#*******************************************************************************
