#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_base01'
YMAX    =  2500

targfile = os.path.join('..',DIRNAME,'param_dict.json')
with open(targfile) as fid01:
  param_dict = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_brick.json')
with open(targfile) as fid01:
  data_brick = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])

tvals    = data_brick.pop('tstamps')
ntstp    = len(tvals)
infBlock = np.zeros((nsims,ntstp))

for sim_idx_str in data_brick:
  try:
    sim_idx = int(sim_idx_str)
  except:
    continue
  infDat = np.array(data_brick[sim_idx_str]['timeseries'])
  infBlock[sim_idx,:] = infDat


# Figure
fig01 = plt.figure(figsize=(8,6))

axs01  = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

yval = np.median(infBlock,axis=0)
xval = np.array(tvals)/365+1900

infDatSetSort = np.sort(infBlock,axis=0)
infDatSetSort = infDatSetSort  

for patwid in [0.475,0.375,0.25]:
  xydat = np.zeros((2*infDatSetSort.shape[1],2))
  xydat[:,0] = np.hstack((xval,xval[::-1]))
  tidx = int((0.5-patwid)*infDatSetSort.shape[0])
  xydat[:,1] = np.hstack((infDatSetSort[tidx,:],infDatSetSort[-tidx,::-1]))

  polyShp = patch.Polygon(xydat, facecolor='C0', alpha=0.7-patwid, edgecolor=None)
  axs01.add_patch(polyShp)

axs01.plot(xval,yval,color='C0',linewidth=2)
axs01.set_ylabel('Monthly Infections',fontsize=14)
axs01.set_xlim(2010, 2020)
axs01.set_ylim(   0, YMAX)
axs01.tick_params(axis='x', labelsize=16)

plt.savefig('fig_clouds01.png')

plt.close()

#*******************************************************************************

