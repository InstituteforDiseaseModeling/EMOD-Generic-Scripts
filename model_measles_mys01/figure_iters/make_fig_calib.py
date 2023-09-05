#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

#*******************************************************************************

DIRNAME = 'experiment_meas_mys_base01'
YMAX    =  350

targfile = os.path.join('..',DIRNAME,'param_dict_iters.json')
with open(targfile) as fid01:
  param_dict = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_brick_iters.json')
with open(targfile) as fid01:
  data_brick = json.load(fid01)

nsims    = int(param_dict['00']['NUM_SIMS'])
niter    = int(param_dict['00']['NUM_ITER'])

cdata    = np.zeros((nsims*niter,1))
R0       = np.zeros((nsims*niter,1))
R0_covid = np.zeros((nsims*niter,1))
R0_peak  = np.zeros((nsims*niter,1))
imp_rate = np.zeros((nsims*niter,1))

infBlock = np.zeros((nsims*niter,120))

for iter_dex_str in data_brick:
  iter_dex = int(iter_dex_str)

  for sim_idx_str in data_brick[iter_dex_str]:
    if(not sim_idx_str.isdigit()):
      continue

    sim_idx = int(sim_idx_str)

    cdata[sim_idx+nsims*iter_dex]     = data_brick[iter_dex_str][sim_idx_str]['cal_val']
    R0[sim_idx+nsims*iter_dex]        = param_dict[iter_dex_str]['EXP_VARIABLE']['R0'][sim_idx]
    R0_covid[sim_idx+nsims*iter_dex]  = param_dict[iter_dex_str]['EXP_VARIABLE']['R0_covid_fac'][sim_idx]
    R0_peak[sim_idx+nsims*iter_dex]   = param_dict[iter_dex_str]['EXP_VARIABLE']['R0_peak_day'][sim_idx]
    imp_rate[sim_idx+nsims*iter_dex]  = param_dict[iter_dex_str]['EXP_VARIABLE']['log10_import_rate'][sim_idx]

    infBlock[sim_idx+nsims*iter_dex,:] = np.array(data_brick[iter_dex_str][sim_idx_str]['timeseries'])


fidx = (imp_rate[:,0]>=-0.25)

# Scaling factor
#infBlock = infBlock * sclVal

# Figure
fig01 = plt.figure(figsize=(8,6))

axs01  = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

print(np.amax(cdata))

#axs01.scatter(R0_peak[fidx],R0[fidx],c=cdata[fidx],vmin=-4e3)
#axs01.hist(cdata[fidx],bins=50)
axs01.plot(np.mean(infBlock[fidx,:],axis=0))

plt.tight_layout()
plt.savefig('fig_iters_01.png')
plt.close()

#*******************************************************************************

