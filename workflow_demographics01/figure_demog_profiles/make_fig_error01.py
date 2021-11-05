#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process import tpop_xval, tpop_yval

from dtk_post_process import uk_1950_frac, uk_1960_frac
from dtk_post_process import uk_1970_frac, uk_1980_frac

#*******************************************************************************

DIRNAME = 'experiment_demographics01'

xvals   = np.array(tpop_xval)
yref    = np.array(tpop_yval)/1e6


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_brick_calib.json')) as fid01:
  data_brick_calib = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
var_set  = np.array(param_dict['EXP_VARIABLE']['variable_birthrate'])
age_set  = np.array(param_dict['EXP_VARIABLE']['modified_age_init'])
mort_set = np.array(param_dict['EXP_VARIABLE']['log_mortality_mult'])

pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str])

calib_vec = np.zeros(nsims)
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  calib_vec[sim_idx] = data_brick_calib[sim_idx_str]

# Figures
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(b=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(b=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlim( -0.5,   3.5)
axs01.set_ylim(  0,    20  )

ticloc = [0, 1, 2, 3]
ticlab = ['', '', '', '']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab,fontsize=14)

ticloc = [  0,  5, 10, 15, 20, 25, 30]
ticlab = ['0', '5', '10', '15', '20', '25', '30']
axs01.set_yticks(ticks=ticloc)
axs01.set_yticklabels(ticlab,fontsize=14)

axs01.set_xlabel('Sim Set', fontsize=14)
axs01.set_ylabel('Error Metric', fontsize=14)


demog_lev = [False,  True,  True,  True]
mod_init  = [False, False,  True,  True]
mort_mul  = [  0.0,   0.0,   0.0,  0.23]
clr_val   = [    0,     2,     4,     3]

for k0 in range(len(demog_lev)):

  gidx        = (var_set==demog_lev[k0]) & (age_set==mod_init[k0]) & (mort_set==mort_mul[k0])

  pyr_mat_avg = np.mean(pyr_mat[gidx,:,:],axis=0)
  pyr_mat_std = np.std(pyr_mat[gidx,:,:],axis=0)

  pop_dat     = np.sum(pyr_mat_avg,axis=1)
  pop_dat_err = np.sum(pyr_mat_std,axis=1)

  calib_set   = calib_vec[gidx]

  ref_pop     = 100000*yref/yref[0]

  err_score1  = np.sqrt(np.sum(np.power(100*(pop_dat-ref_pop)/ref_pop,2.0)))

  axs01.plot(k0, err_score1, '+', c='C{:d}'.format(clr_val[k0]), ms=16, mew=4)


  err_score2  = 0

  simdat1950  = 100*pyr_mat_avg[ 0,:]/np.sum(pyr_mat_avg[ 0,:])
  refdat1950  = 100*np.array(uk_1950_frac[1:])
  err_score2  = err_score2 + np.sqrt(np.sum(np.power(simdat1950-refdat1950,2.0)))

  simdat1960  = 100*pyr_mat_avg[10,:]/np.sum(pyr_mat_avg[10,:])
  refdat1960  = 100*np.array(uk_1960_frac[1:])
  err_score2  = err_score2 + np.sqrt(np.sum(np.power(simdat1960-refdat1960,2.0)))

  simdat1970  = 100*pyr_mat_avg[20,:]/np.sum(pyr_mat_avg[20,:])
  refdat1970  = 100*np.array(uk_1970_frac[1:])
  err_score2  = err_score2 + np.sqrt(np.sum(np.power(simdat1970-refdat1970,2.0)))

  simdat1980  = 100*pyr_mat_avg[30,:]/np.sum(pyr_mat_avg[30,:])
  refdat1980  = 100*np.array(uk_1980_frac[1:])
  err_score2  = err_score2 + np.sqrt(np.sum(np.power(simdat1980-refdat1980,2.0)))

  axs01.plot(k0, err_score2, 'x', c='C{:d}'.format(clr_val[k0]), ms=16, mew=4)

  axs01.plot(k0+0*calib_set, calib_set, '.', c='C{:d}'.format(clr_val[k0]))

  axs01.plot(k0, np.mean(calib_set), 'o', c='C{:d}'.format(clr_val[k0]), ms=16, mew=4)

axs01.text( 0.15, 26.0, '+  Total Pop\nx   Pyramid', fontsize=18)

plt.tight_layout()
plt.savefig('fig_error01.png')
plt.close()

#*******************************************************************************
