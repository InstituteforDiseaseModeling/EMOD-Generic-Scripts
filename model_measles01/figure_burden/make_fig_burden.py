#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt
import matplotlib.patches  as patch
import matplotlib          as mpl

from global_data           import run_years

#*******************************************************************************


DIRNAMES = ['experiment_popL1' ]
YMAX     = 1500

for dirname in DIRNAMES:

  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  infBlock     = np.zeros((nsims,12*int(run_years)))
  pyr_mat      = np.zeros((nsims,   int(run_years)+1,20))-1

  for sim_idx_str in data_brick:
    if(not sim_idx_str.isdigit()):
      continue

    sim_idx = int(sim_idx_str)
    pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])
    infBlock[sim_idx,:]  = np.array(data_brick[sim_idx_str]['timeseries'])

  fidx = (pyr_mat[:,0,0]>=0)

  pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
  tpop_avg    = np.sum(pyr_mat_avg, axis=1)
  tpop_xval   = np.arange(len(tpop_avg))


  # Figures
  fig01 = plt.figure(figsize=(8,6))

  # Figures - Sims - Infections
  axs01 = fig01.add_subplot(1, 1, 1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  infBlock = infBlock[fidx,:]

  xval = np.arange(0,run_years,1/12) + 1/24
  pops = np.interp(xval, tpop_xval, tpop_avg)
  yval = np.mean(infBlock,axis=0)/pops*1e5

  infDatSetSort = np.sort(infBlock,axis=0)
  infDatSetSort = infDatSetSort

  #axs01.set_yticks(ticks=np.arange(0,6001,1000))
  #axs01.set_yticklabels(['0','1k','2k','3k','4k','5k','6k'],fontsize=16)
  #axs01.tick_params(axis='x', labelsize=16)

  for patwid in [0.45,0.375,0.25]:
    xydat = np.zeros((2*infDatSetSort.shape[1],2))
    xydat[:,0] = np.hstack((xval,xval[::-1]))
    tidx = int((0.5-patwid)*infDatSetSort.shape[0])
    xydat[:,1] = np.hstack((infDatSetSort[tidx,:],infDatSetSort[-tidx,::-1]))

    polyShp = patch.Polygon(xydat, facecolor='C0', alpha=0.7-patwid, edgecolor=None)
    axs01.add_patch(polyShp)

  axs01.plot(xval,yval,color='C0',linewidth=2)
  axs01.set_ylabel('Monthly Infections per 100k',fontsize=16)
  axs01.set_xlabel('Year',fontsize=16)
  axs01.set_ylim(   0, YMAX)

  plt.tight_layout()
  plt.savefig('fig_clouds_{:s}_01.png'.format(dirname))
  plt.close()


#*******************************************************************************
