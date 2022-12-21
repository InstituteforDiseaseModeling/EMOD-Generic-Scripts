#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

#*******************************************************************************


DIRNAME = 'experiment_test01'


targfile = os.path.join('..',DIRNAME,'param_dict.json')
with open(targfile) as fid01:
  param_dict = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_brick.json')
with open(targfile) as fid01:
  data_brick = json.load(fid01)


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)


nsims        = int(param_dict['NUM_SIMS'])
pop_dat_str  =     param_dict['EXP_CONSTANT']['nga_state_name']
sia_list     =     param_dict['EXP_CONSTANT']['test_sias']

tvals    = data_brick.pop('tstamps')
ntstp    = len(tvals)
infBlock = np.zeros((nsims,ntstp))
sia_num  = np.zeros((len(sia_list),nsims))
sia_den  = np.zeros((len(sia_list),nsims))


for sim_idx_str in data_brick:
  try:
    sim_idx = int(sim_idx_str)
  except:
    continue
  infDat = np.array(data_brick[sim_idx_str]['inf_mo'])
  siaVal = np.array(data_brick[sim_idx_str]['sia_summary'])

  infBlock[sim_idx,:] = infDat/1000
  sia_num[:,sim_idx]  = siaVal[:,1]
  sia_den[:,sim_idx]  = siaVal[:,2]


# Figure
fig01 = plt.figure(figsize=(8,6))
axs01 = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

yval = np.mean(infBlock,axis=0)
xval = np.array(tvals)/365+1900

infDatSetSort = np.sort(infBlock,axis=0)
infDatSetSort = infDatSetSort


for patwid in [0.45,0.375,0.25]:
  xydat = np.zeros((2*infDatSetSort.shape[1],2))
  xydat[:,0] = np.hstack((xval,xval[::-1]))
  tidx = int((0.5-patwid)*infDatSetSort.shape[0])
  xydat[:,1] = np.hstack((infDatSetSort[tidx,:],infDatSetSort[-tidx,::-1]))

  polyShp = patch.Polygon(xydat, facecolor='C0', alpha=0.7-patwid, edgecolor=None)
  axs01.add_patch(polyShp)

axs01.plot(xval,yval,color='C0',linewidth=2)
axs01.set_ylabel('Monthly Cases (thousands) - Simulated',fontsize=16)

ylim_val = axs01.get_ylim()
for k1 in range(len(sia_list)):
  sia_time   = sia_list[k1]
  num_immune = np.mean(sia_num[k1,:])
  num_target = np.mean(sia_den[k1,:])

  axs01.plot([sia_time,sia_time],[0,0.7*ylim_val[1]],'g--',lw=2)
  stat_str = 'Year: {:7.2f}; Immunized: {:.0f}; Targetted: {:.0f}; Frac: {:4.2f}'
  print(stat_str.format(sia_time,num_immune,num_target,num_immune/num_target))


plt.tight_layout()
plt.savefig('fig_inf_{:s}_01.png'.format(pop_dat_str))
plt.close()


#*******************************************************************************
