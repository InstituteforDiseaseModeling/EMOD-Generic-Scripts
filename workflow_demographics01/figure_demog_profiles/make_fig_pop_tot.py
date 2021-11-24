#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process import tpop_xval, tpop_yval

#*******************************************************************************

DIRNAME = 'experiment_demog_UK01_sweep'

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
var_set  = np.array(param_dict['EXP_VARIABLE']['variable_birthrate'])
age_set  = np.array(param_dict['EXP_VARIABLE']['modified_age_init'])
mort_set = np.array(param_dict['EXP_VARIABLE']['log_mortality_mult'])

pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str])

# Figures
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('Population (M)', fontsize=14)

axs01.set_xlim( 0, 30)
axs01.set_ylim(50, 58)

ticloc = [0, 5, 10, 15, 20, 25, 30]
ticlab = ['1950', '1955', '1960', '1965', '1970', '1975', '1980']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab,fontsize=14)

ticloc = [50, 52, 54, 56, 58, 60]
ticlab = ['50', '52', '54', '56', '58', '60']
axs01.set_yticks(ticks=ticloc)
axs01.set_yticklabels(ticlab,fontsize=14)


demog_lev = [False,  True,  True,  True]
mod_init  = [False, False,  True,  True]
mort_mul  = [  0.0,   0.0,   0.0,  0.23]
clr_val   = [    0,     2,     4,     3]
off_val   = [-0.15, -0.05,  0.05,  0.15]
lab_val   = ['Equilibrium', 'Forcing+InitEquilib', 'Forcing+InitHistory', 'Forcing+InitHistory+AdjustMort']

for k0 in range(len(demog_lev)):

  gidx        = (var_set==demog_lev[k0]) & (age_set==mod_init[k0]) & (mort_set==mort_mul[k0])

  pyr_mat_avg = np.mean(pyr_mat[gidx,:,:],axis=0)
  pyr_mat_std = np.std(pyr_mat[gidx,:,:],axis=0)

  pop_dat     = np.sum(pyr_mat_avg,axis=1)
  pop_dat_err = np.sum(pyr_mat_std,axis=1)

  yvals       = pop_dat/100000*yref[0]
  yvals_err   = pop_dat_err/100000*yref[0]

  axs01.errorbar(xvals+off_val[k0], yvals, yerr=yvals_err, zorder=3,
                 c='C{:d}'.format(clr_val[k0]), lw=2, label=lab_val[k0])

axs01.plot(xvals, yref, lw=0, c='k', marker='.', markersize=14, label='Data', zorder=1)
axs01.legend()

plt.tight_layout()
plt.savefig('fig_pop_tot_01.png')
plt.close()

#*******************************************************************************
