#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt

import matplotlib.cm      as cm

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_test03'
YMAX    =  400e3

#targfile = os.path.join('..',DIRNAME,'param_dict.json')
#with open(targfile) as fid01:
#  param_dict = json.load(fid01)

#targfile = os.path.join('..',DIRNAME,'data_brick.json')
#with open(targfile) as fid01:
#  data_brick = json.load(fid01)

#targfile = os.path.join('..',DIRNAME,'data_calib.json')
#with open(targfile) as fid01:
#  calib_dict = json.load(fid01)


# Figure
fig01 = plt.figure(figsize=(8,5))
axs01 = fig01.add_subplot(111,label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Minimum Surveillance',fontsize=14)
axs01.set_ylabel('Cases for Response', fontsize=14)
#axs01.set_title('Lab Rejected Cases: 2015 - 2017',fontsize=18)

axs01.set_xscale('log')

#axs01.spines['top'].set_color('none')
#axs01.spines['bottom'].set_color('none')
#axs01.spines['left'].set_color('none')
#axs01.spines['right'].set_color('none')
#axs01.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

#axs01.set_xlim(  2, 15)
#axs01.set_ylim(  4, 14)

virmap   = cm.get_cmap('viridis')

xval = np.random.uniform(-3,   -1, size=1000)
yval = np.random.uniform( 0, 1000, size=1000)
cval = np.random.uniform( 0,    3, size=1000)

axs01.scatter(np.power(10.0,xval), yval, c=cval)

cbar_handle = plt.colorbar(cm.ScalarMappable(cmap=virmap), shrink=0.75)

ticloc = [0,0.333,0.666,1.0]
ticlab = ['0','1','2','3']

cbar_handle.set_ticks(ticks=ticloc)
cbar_handle.set_ticklabels(ticlab)
cbar_handle.set_label('Cases Averted',fontsize=14,labelpad=10)
cbar_handle.ax.tick_params(labelsize=14)

plt.savefig('fig_averted_t03.png')
plt.close()

