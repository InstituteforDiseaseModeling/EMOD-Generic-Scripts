#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************

DIRNAME = 'experiment_demog_UK01_calib'
NITER   = 8

# Sim outputs
tpath = os.path.join('..',DIRNAME)

# Create figure
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlim( -2.0,  2.0)
axs01.set_ylim( -2.0,  2.0)

axs01.set_xlabel('Log Mortality Multiplier: <20yrs', fontsize=14)
axs01.set_ylabel('Log Mortality Multiplier: >20yrs', fontsize=14)

xdata = list()
ydata = list()
cdata = list()

# Plot scatter data
for k1 in range(NITER+1):
  with open(os.path.join(tpath,'param_dict_iter{:02d}.json'.format(k1))) as fid01:
    param_dict = json.load(fid01)
  with open(os.path.join(tpath,'data_calib_iter{:02d}.json'.format(k1))) as fid01:
    calib_dict = json.load(fid01)

  nsims    = int(param_dict['NUM_SIMS'])

  xdata.extend(param_dict['EXP_VARIABLE']['log_mort_mult01'])
  ydata.extend(param_dict['EXP_VARIABLE']['log_mort_mult02'])

  calib_vec = np.zeros(nsims)
  for sim_idx_str in calib_dict:
    sim_idx = int(sim_idx_str)
    calib_vec[sim_idx] = -calib_dict[sim_idx_str]
  cdata.extend(calib_vec.tolist())

xdata = np.array(xdata)
ydata = np.array(ydata)
cdata = np.array(cdata)
sidx  = np.argsort(cdata)
axs01.scatter(xdata[sidx], ydata[sidx], c=cdata[sidx], vmin=-30)

# Save figure
plt.tight_layout()
plt.savefig('fig_calib_04.png')
plt.close()

#*******************************************************************************
