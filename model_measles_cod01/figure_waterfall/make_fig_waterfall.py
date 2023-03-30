#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************


DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
BIN_EDGES = np.cumsum(7*DAY_BINS) + 0.5
BIN_EDGES = np.insert(BIN_EDGES, 0, 0.5)



DIRNAME = 'experiment_meas_cod_base01'


# Sim outputs
tpath = os.path.join('..',DIRNAME)


with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)


# Create figure
fig01 = plt.figure(figsize=(24,18))

axs01 = fig01.add_subplot(1, 1, 1, projection='3d',computed_zorder=False)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)


nsims    = int(param_dict['NUM_SIMS'])


inf_cum1  = np.zeros(nsims)-1
inf_cum2  = np.zeros(nsims)-1

wf_mat   = np.zeros((36,48))
wf_num   = np.zeros(36)

for sim_idx_str in data_brick:
  if(sim_idx_str.isdecimal()):
    sim_idx = int(sim_idx_str)

    inf_trace = np.array(data_brick[sim_idx_str]['inf_trace'])
    (inf_mo, tstamps) = np.histogram(np.arange(inf_trace.shape[0]),
                                     bins    = BIN_EDGES,
                                     weights = inf_trace)
    tstamps = (np.diff(tstamps) + tstamps[:-1])/365.0 + 2006

    inf_cum1[sim_idx] = np.sum(inf_trace)
    inf_cum2[sim_idx] = np.log(np.sum(inf_mo[36:42]))

    if(inf_cum2[sim_idx] < 8):
      wf_idx = np.argmax(inf_mo[48:])
      wf_num[wf_idx]   += 1
      wf_mat[wf_idx,:] += inf_mo[36:]


print(np.sum(wf_num),np.min(wf_num),np.max(wf_num))
fidx   = (inf_cum1>0)
print(np.sum(fidx))

nplts = wf_mat.shape[0]
for k1 in range(nplts):
  rk1 = nplts - 1 - k1
  wsh = k1/nplts
  if(wsh > 0.5):
    wsh1 = 0.5
    wsh2 = 1.2*(wsh-0.5)
  else:
    wsh1 = wsh
    wsh2 = 0
  axs01.bar(tstamps[36:], wf_mat[rk1,:]/wf_num[rk1], zs=rk1, zdir='y', width=(1/12), color=[0.3+wsh1,wsh2,wsh2,0.9], edgecolor='k' )


axs01.set_xlim(2009,2013)
axs01.set_ylim(   0,  35)
axs01.set_box_aspect((4,9,1))

ticloc = [2009,2010,2011,2012,2013]
ticlab = ['','','','','']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab,fontsize=14)

axs01.set_yticks([])
axs01.set_zticks([])

axs01.xaxis.pane.fill = False
axs01.yaxis.pane.fill = False
axs01.zaxis.pane.fill = False

fig01.patch.set_alpha(0.0)
axs01.patch.set_alpha(0.0)

# Save figure
plt.savefig('fig_waterfall01.png')
plt.close()

#*******************************************************************************
