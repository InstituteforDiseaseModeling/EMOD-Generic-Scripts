#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************

DIRNAME = 'experiment_demog_UK01_calib'

# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_brick_calib.json')) as fid01:
  data_brick_calib = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
mort_set = np.array(param_dict['EXP_VARIABLE']['log_mortality_mult'])

calib_vec = np.zeros(nsims)
for sim_idx_str in data_brick_calib:
  sim_idx = int(sim_idx_str)
  calib_vec[sim_idx] = data_brick_calib[sim_idx_str]

# Figures
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
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
plt.savefig('fig_calib_01.png')
plt.close()

#*******************************************************************************
