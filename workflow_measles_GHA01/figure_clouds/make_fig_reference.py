#*******************************************************************************

import os, sys, json

sys.path.append(os.path.join('..','Assets','python'))

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

from dtk_post_process   import   ref_dat

#*******************************************************************************

DIRNAME = 'experiment_meas_gha_base01'
YMAX    = 300

targfile = os.path.join('..',DIRNAME,'param_dict.json')
with open(targfile) as fid01:
  param_dict = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_brick.json')
with open(targfile) as fid01:
  dbrick = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
tvals    = dbrick.pop('tstamps')

# Figure
fig01 = plt.figure(figsize=(8,6))

axs01  = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

yval = np.array(ref_dat)
xval = np.array(tvals)[:len(ref_dat)]/365+1900

axs01.bar(xval,yval,color='r',linewidth=0.5,edgecolor='k',width=0.9/12)
axs01.set_ylabel('Monthly Cases',fontsize=14)
axs01.set_xlim(2010,2025)
axs01.set_ylim(   0, YMAX)
axs01.tick_params(axis='x', labelsize=16)

sia01 = np.array([40460,40460])/365+1900
axs01.plot(sia01,[0,YMAX],color='C0',linewidth=3,ls='--')

sia02 = np.array([41508,41508])/365+1900
axs01.plot(sia02,[0,YMAX],color='C2',linewidth=5,ls='--')

sia03 = np.array([43365,43365])/365+1900
axs01.plot(sia03,[0,YMAX],color='C0',linewidth=3,ls='--')

plt.savefig('fig_reference01.png')

plt.close()

#*******************************************************************************

