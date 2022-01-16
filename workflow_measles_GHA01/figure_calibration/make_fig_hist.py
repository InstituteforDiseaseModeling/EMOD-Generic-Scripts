#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************


DIRNAME = 'experiment_meas_gha_base01'


# Create figure
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(111, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

#axs01.set_ylim(-6000, 0)


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_calib.json')) as fid01:
  calib_dict = json.load(fid01)


# Plot scatter data

cdata    = list()
nsims    = int(param_dict['NUM_SIMS'])

calib_vec = np.zeros(nsims)
for sim_idx_str in calib_dict:
  sim_idx = int(sim_idx_str)
  calib_vec[sim_idx] = calib_dict[sim_idx_str]
cdata.extend(calib_vec.tolist())

cdata  = np.array(cdata)

axs01.hist(cdata)


# Save figure
plt.tight_layout()
plt.savefig('fig_calib_1D_01.png')
plt.close()

#*******************************************************************************
