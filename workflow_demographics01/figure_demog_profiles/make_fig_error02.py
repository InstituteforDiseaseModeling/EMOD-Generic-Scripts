#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process import tpop_xval, tpop_yval

from dtk_post_process import uk_1950_frac, uk_1960_frac
from dtk_post_process import uk_1970_frac, uk_1980_frac

#*******************************************************************************

DIRNAME = 'experiment_demog_UK01_calib'

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
mort_set = np.array(param_dict['EXP_VARIABLE']['log_mortality_mult'])

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

axs01.set_xlim( -1.0,  1.0)
axs01.set_ylim(  0,   80  )

#ticloc = [0, 1, 2,]
#ticlab = ['', '', '']
#axs01.set_xticks(ticks=ticloc)
#axs01.set_xticklabels(ticlab,fontsize=14)

#ticloc = [  0,  5, 10, 15, 20, 25, 30]
#ticlab = ['0', '5', '10', '15', '20', '25', '30']
#axs01.set_yticks(ticks=ticloc)
#axs01.set_yticklabels(ticlab,fontsize=14)

axs01.set_xlabel('Log Mortality Multiplier', fontsize=14)
axs01.set_ylabel('Error Metric', fontsize=14)


axs01.plot(mort_set, calib_vec, '.', c='C3')


plt.tight_layout()
plt.savefig('fig_error02.png')
plt.close()

#*******************************************************************************
