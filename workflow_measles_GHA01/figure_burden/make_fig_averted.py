#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt

import matplotlib.cm      as cm

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_test04'

targfile = os.path.join('..',DIRNAME,'param_dict.json')
with open(targfile) as fid01:
  param_dict = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_brick.json')
with open(targfile) as fid01:
  data_brick = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_calib.json')
with open(targfile) as fid01:
  calib_dict = json.load(fid01)


nsims     = int(param_dict['NUM_SIMS'])
log10_rep = np.array(param_dict['EXP_VARIABLE']['log10_min_reporting'])
num_cases = np.array(param_dict['EXP_VARIABLE']['adm01_case_threshold'])


tvals    = data_brick.pop('tstamps')
ntstp    = len(tvals)
infBlock = np.zeros((nsims,ntstp))
sclVal   = np.zeros((nsims,1))
cdata    = np.zeros(nsims)

for sim_idx_str in data_brick:
  try:
    sim_idx = int(sim_idx_str)
  except:
    continue
  infDat = np.array(data_brick[sim_idx_str]['timeseries'])
  infBlock[sim_idx,:] = infDat
  sclVal[sim_idx,0]   = data_brick[sim_idx_str]['rep_rate']
  cdata[sim_idx]      = calib_dict[sim_idx_str]

ntval    = np.array(tvals)/365+1900
gidx     = (cdata > -4000)
nusim    = np.sum(gidx)
test_idx = np.argwhere(ntval>2020)[0][0]

infBlock              = infBlock[gidx,:]
log10_rep             = log10_rep[gidx]
num_cases             = num_cases[gidx]
infBlock[:,:test_idx] = 0
infBlock              = np.cumsum(infBlock,axis=1)

print(infBlock.shape,log10_rep.shape,num_cases.shape)


# Figure
fig01 = plt.figure(figsize=(8,5))
axs01 = fig01.add_subplot(111,label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Minimum Surveillance',fontsize=14)
axs01.set_ylabel('Case Threshold for Response', fontsize=14)
#axs01.set_title('Lab Rejected Cases: 2015 - 2017',fontsize=18)

axs01.set_xscale('log')

#axs01.spines['top'].set_color('none')
#axs01.spines['bottom'].set_color('none')
#axs01.spines['left'].set_color('none')
#axs01.spines['right'].set_color('none')
#axs01.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

axs01.set_xlim(  1e-3, 1e-1)
axs01.set_ylim(  0, 1000)

virmap   = cm.get_cmap('viridis')

xval = log10_rep
yval = num_cases
cval = infBlock[:,-1]
gdx2 = np.argsort(cval)[::-1]

# Binning
nbins = 8
dyval        = (1000-0)/(nbins-1)
dxval        = ((-1)-(-3))/(nbins-1)
(xvec,yvec) = np.meshgrid(np.linspace(-3-dxval/2,-1+dxval/2,nbins+1),np.linspace(0-dyval/2,1000+dyval/2,nbins+1))
zmat        = np.zeros((nbins,nbins))

print(dxval,dyval)
print(xvec[1,1]-xvec[0,0],yvec[1,1]-yvec[0,0])

for k1 in range(nbins):
  for k2 in range(nbins):
    gidx = (xval>xvec[k1,k2]) & (xval<xvec[k1,k2+1]) & (yval>yvec[k1,k2]) & (yval<yvec[k1+1,k2])
    zmat[k1,k2] = np.mean(cval[gidx])

plt.contour(np.power(10.0,xvec[:-1,:-1]+dxval/2),
                          yvec[:-1,:-1]+dyval/2,
                          zmat, levels=[101e3,151e3,201e3,226e3],linewidths=3, vmin=0, vmax=250e3)

axs01.scatter(np.power(10.0,xval[gdx2]), yval[gdx2], c=cval[gdx2], s=2, vmin=0, vmax=300e3, alpha=0.7)

ticloc = [0.001, 0.01, 0.1]
ticlab = ['0.1%','1.0%','10%']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

cbar_handle = plt.colorbar(cm.ScalarMappable(cmap=virmap), shrink=0.75)

axs01.plot([0.04, 0.04],[0,1000],'k:')

ticloc = [0.000,0.333,0.667,1.000]
ticlab = ['0','100k','200k','300k']

cbar_handle.set_ticks(ticks=ticloc)
cbar_handle.set_ticklabels(ticlab)
cbar_handle.set_label('Cumulative Infections',fontsize=14,labelpad=10)
cbar_handle.ax.tick_params(labelsize=14)

plt.savefig('fig_averted_t04.png')
plt.close()

