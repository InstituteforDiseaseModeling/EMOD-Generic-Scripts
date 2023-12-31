#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_base01'
YMAX    =  350

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
sclVal   = np.zeros((nsims,1))-1
cdata    = np.zeros(nsims)

for sim_idx_str in data_brick:
  try:
    sim_idx = int(sim_idx_str)
  except:
    continue
  infBlock[sim_idx,:] = np.array(data_brick[sim_idx_str]['timeseries'])
  sclVal[sim_idx,0]   = data_brick[sim_idx_str]['rep_rate']
  cdata[sim_idx]      = data_brick[sim_idx_str]['cal_val']

fidx = (sclVal[:,0]>=0)

# Scaling factor
infBlock = infBlock * sclVal

# Figure
fig01 = plt.figure(figsize=(8,6))

axs01  = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

gidx = (cdata > -4000) & fidx

infBlock = infBlock[gidx,:]

yval = np.mean(infBlock,axis=0)
xval = np.array(tvals)/365+1900

print(np.median(sclVal[gidx]))

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
axs01.set_ylabel('Monthly Cases - Simulated',fontsize=16)
axs01.set_xlim(2010, 2020)
axs01.set_ylim(   0, YMAX)

ticloc = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
ticlab = ['','','','','','','','','','','']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)
for k1 in ticloc[:-1]:
  axs01.text(k1+0.5,-0.04*YMAX,str(k1),fontsize=11,ha='center')

sia01 = np.array([40460,40460])/365+1900
axs01.plot(sia01,[0,YMAX],color='c',linewidth=3,ls=':')
axs01.text(sia01[0]+0.2,0.9*YMAX,'SIA',fontsize=13)

sia02 = np.array([41508,41508])/365+1900
axs01.plot(sia02,[0,YMAX],color='c',linewidth=5,ls='--')
axs01.text(sia02[0]+0.2,0.9*YMAX,'RCV Catch-up',fontsize=13)

sia03 = np.array([43365,43365])/365+1900
axs01.plot(sia03,[0,YMAX],color='c',linewidth=3,ls=':')
axs01.text(sia03[0]+0.2,0.9*YMAX,'SIA',fontsize=13)

plt.tight_layout()
plt.savefig('fig_clouds_base_01.png')
plt.close()

#*******************************************************************************

