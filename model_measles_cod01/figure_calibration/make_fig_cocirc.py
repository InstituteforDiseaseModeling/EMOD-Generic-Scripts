#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************


DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
BIN_EDGES = np.cumsum(7*DAY_BINS) + 0.5
BIN_EDGES = np.insert(BIN_EDGES, 0, 0.5)



DIRNAME = 'experiment_meas_cod_base02'


# Sim outputs
tpath = os.path.join('..',DIRNAME)


with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)


# Create figure
fig01 = plt.figure(figsize=(16,12))

axs01 = fig01.add_subplot(1, 1, 1)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)


nsims    = int(param_dict['NUM_SIMS'])


inf_gen01 = np.zeros((4,nsims,48))-1
tinfval   = np.zeros((4,48))
tinfnum   = 0

for sim_idx_str in data_brick:
  if(sim_idx_str.isdecimal()):
    sim_idx = int(sim_idx_str)

    if(len(data_brick[sim_idx_str]['inf_trace']) < 2000):
      continue

    for k1 in [0,1,2,3]:
      inf_gen01[k1,sim_idx,:] = np.array(data_brick[sim_idx_str]['genome_trace'][k1])

    gen_sum = np.sum(inf_gen01,axis=0)
    if(np.sum(gen_sum[sim_idx,:18]) < 5000 and np.sum(gen_sum[sim_idx,-12:]) > 5000):
      for k1 in [0,1,2,3]:
        tinfval[k1,:] += inf_gen01[k1,sim_idx,:]
      tinfnum += 1


print(tinfnum)
for k1 in [0,1,2,3]:
  axs01.plot(2009+np.arange(48)/12+1/24,tinfval[k1,:]/tinfnum)


axs01.set_xlim(2009,2013)
#axs01.set_ylim(   0,  35)

#ticloc = [2009,2010,2011,2012,2013]
#ticlab = ['','','','','']
#axs01.set_xticks(ticks=ticloc)
#axs01.set_xticklabels(ticlab,fontsize=14)

#fig01.patch.set_alpha(0.0)
#axs01.patch.set_alpha(0.0)

# Save figure
plt.savefig('fig_gentrace01.png')
plt.close()

#*******************************************************************************
