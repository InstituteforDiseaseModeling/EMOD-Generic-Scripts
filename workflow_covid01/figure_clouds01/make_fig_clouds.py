#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

#*******************************************************************************

intlist   = [221,222,223,224]
pname     = ['ANG','ETH','ITA','UKR']

path_list = [('experiment_{:s}_Base_Age_UrbRur01', 'C0', '-')]

datlist = dict()
parlist = dict()

for pn in pname:
  datlist[pn] = list()

  for pathval in path_list:
    targfile = os.path.join('..',pathval[0].format(pn),'param_dict.json')
    with open(targfile) as fid01:
      parlist[pn] = json.load(fid01)

    nSims  = 1000#parlist[pn]['num_sims']
    nTimes = 730#np.array(parlist[pn]['nTsteps'])
    nTime  = np.max(nTimes)

    infBlock = np.zeros((nSims,nTime))

    targfile = os.path.join('..',pathval[0].format(pn),'data_brick.json')
    with open(targfile) as fid01:
      dbrick = json.load(fid01)

    for simKey in dbrick:
      idx = int(simKey)
      infDat = np.sum(np.array(dbrick[simKey]),axis=0)
      if(infDat.shape[0] != nTimes):
        print(infDat.shape[0], nTimes)
      infBlock[idx,:] = infDat

    datlist[pn].append(infBlock)


# Figure
fig01 = plt.figure(figsize=(12.8,9.6))

axs00 = fig01.add_subplot(111)

axs00.spines['top'].set_color('none')
axs00.spines['bottom'].set_color('none')
axs00.spines['left'].set_color('none')
axs00.spines['right'].set_color('none')
axs00.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

for k0 in range(len(pname)):

  pn     = pname[k0]
  figint = intlist[k0]
  axs01  = fig01.add_subplot(figint)

  plt.sca(axs01)

  axs01.grid(b=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(b=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_xlim(0,500)

  axs01.text(0.05,0.85,pn,fontsize=16, transform=axs01.transAxes)

  for k1 in range(len(datlist[pn])):

    pathval = path_list[k1]

    infDatPart = datlist[pn][k1]
    infDatCum  = np.cumsum(datlist[pn][k1],axis=1)
    gIdx = (infDatCum[:,-1]>0)
    tyslice = infDatPart[gIdx,:]/10.0
    yval = np.mean(tyslice,axis=0)
    xval = np.arange(0.5,yval.shape[0])

    infDatSetSort = np.sort(tyslice,axis=0)
    infDatSetSort = infDatSetSort  

    for patwid in [0.475,0.375,0.25]:
      xydat = np.zeros((2*infDatSetSort.shape[1],2))
      xydat[:,0] = np.hstack((xval-60,xval[::-1]-60))
      tidx = int((0.5-patwid)*infDatSetSort.shape[0])
      xydat[:,1] = np.hstack((infDatSetSort[tidx,:],infDatSetSort[-tidx,::-1]))

      polyShp = patch.Polygon(xydat, facecolor=pathval[1], alpha=0.7-patwid, edgecolor=None)
      axs01.add_patch(polyShp)
    
    axs01.plot(xval-60,yval,color=pathval[1],linestyle=pathval[2],linewidth=2)

axs00.set_xlabel('Days Post Introduction',fontsize=26)
axs00.set_ylabel('Daily Infections per-100k',fontsize=26)

#plt.savefig('fig_clouds01.png')
plt.savefig('fig_clouds01.svg')

plt.close()

#*******************************************************************************

