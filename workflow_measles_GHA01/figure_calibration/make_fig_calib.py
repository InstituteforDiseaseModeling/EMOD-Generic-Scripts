#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_calib04'

x1l = 'log10_import_rate'
x2l = 'ind_variance_risk'
x3l = 'SIA_cover_GHA-2018'

# Sim outputs
tpath = os.path.join('..',DIRNAME)

# Calibration parameters
#with open(os.path.join(tpath,'param_calib.json')) as fid01:
  #param_calib = json.load(fid01)

# Create figure
fig01 = plt.figure(figsize=(24,6))

axs01 = fig01.add_subplot(131, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)
axs01.set_xlabel(x1l)
axs01.set_ylabel(x2l)

axs02 = fig01.add_subplot(132, label=None)
plt.sca(axs02)

axs02.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs02.grid(visible=True, which='minor', ls=':', lw=0.1)
axs02.set_axisbelow(True)
axs02.set_xlabel(x1l)
axs02.set_ylabel(x3l)

axs03 = fig01.add_subplot(133, label=None)
plt.sca(axs03)

axs03.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs03.grid(visible=True, which='minor', ls=':', lw=0.1)
axs03.set_axisbelow(True)
axs03.set_xlabel(x2l)
axs03.set_ylabel(x3l)

x1data = list()
x2data = list()
x3data = list()
cdata  = list()

# Plot scatter data
for k1 in range(1):#(param_calib['NUM_ITER']+1):
  with open(os.path.join(tpath,'param_dict_iter{:02d}.json'.format(k1))) as fid01:
    param_dict = json.load(fid01)
  with open(os.path.join(tpath,'data_calib_iter{:02d}.json'.format(k1))) as fid01:
    calib_dict = json.load(fid01)

  nsims    = int(param_dict['NUM_SIMS'])

  x1data.extend(param_dict['EXP_VARIABLE'][x1l])
  x2data.extend(param_dict['EXP_VARIABLE'][x2l])
  x3data.extend(param_dict['EXP_VARIABLE'][x3l])


  calib_vec = np.zeros(nsims)
  for sim_idx_str in calib_dict:
    sim_idx = int(sim_idx_str)
    calib_vec[sim_idx] = calib_dict[sim_idx_str]
  cdata.extend(calib_vec.tolist())

x1data = np.array(x1data)
x2data = np.array(x2data)
x3data = np.array(x3data)
cdata  = np.array(cdata)
sidx   = np.argsort(cdata)

axs01.scatter(x1data[sidx], x2data[sidx], c=cdata[sidx], vmin = -3300)
axs02.scatter(x1data[sidx], x3data[sidx], c=cdata[sidx], vmin = -3300)
axs03.scatter(x2data[sidx], x3data[sidx], c=cdata[sidx], vmin = -3300)


# Save figure
plt.tight_layout()
plt.savefig('fig_calib_3D_41.png')
plt.close()

#*******************************************************************************
