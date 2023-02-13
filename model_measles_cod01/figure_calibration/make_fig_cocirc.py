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
print(nsims)

inf_gen01 = np.zeros((4,nsims,48))-1
tinfval   = np.zeros((4,48))
tinfnum   = 0
ssetsim   = 0
fracgen   = [[],[],[],[]]
cmap      = [[ 96/255,96/255,96/255,0.65],[127/255,96/255, 0/255,0.65],
             [197/255,90/255,17/255,0.65],[132/255,60/255,12/255,0.65]]

for sim_idx_str in data_brick:
  if(sim_idx_str.isdecimal()):
    sim_idx = int(sim_idx_str)

    if(len(data_brick[sim_idx_str]['inf_trace']) < 2000):
      continue

    ssetsim += 1

    for k1 in [0,1,2,3]:
      inf_gen01[k1,sim_idx,:] = np.array(data_brick[sim_idx_str]['genome_trace'][k1])

    gen_sum = np.sum(inf_gen01,axis=0)
    #if(np.sum(gen_sum[sim_idx,-12:]) > 1000 and np.sum(gen_sum[sim_idx,:18]) < 5000):
    if(np.sum(gen_sum[sim_idx,:18]) < 5000):
    #if(True):
      for k1 in [0,1,2,3]:
        tinfval[k1,:] += inf_gen01[k1,sim_idx,:]
        fracgen[k1].append(np.sum(inf_gen01[k1,sim_idx,:],axis=-1)/np.sum(gen_sum[sim_idx,:],axis=-1))
      tinfnum += 1
      #axs01.plot(2009+np.arange(48)/12+1/24,gen_sum[sim_idx,:])

print(ssetsim)
print(tinfnum)
for k1 in [3,2,1,0]:
  pass
  #axs01.plot(2009+np.arange(48)/12+1/24,np.sum(tinfval,axis=0)/tinfnum)
  #axs01.plot(2009+np.arange(48)/12+1/24,tinfval[k1,:]/tinfnum)
  axs01.hist(fracgen[k1],np.arange(26)/25,color=cmap[k1],density=True)

axs01.set_xlim(0,1)
axs01.xaxis.set_tick_params(labelsize=18)

axs01.set_ylim(0,20)
ticloc = [0,4,8,12,16,20]
ticlab = ['','','','','','']
axs01.set_yticks(ticloc)
axs01.set_yticklabels(ticlab,fontsize=18)

fig01.patch.set_alpha(0.0)
axs01.patch.set_alpha(0.0)

# Save figure
plt.savefig('fig_gentrace01.png')
plt.close()

#*******************************************************************************
