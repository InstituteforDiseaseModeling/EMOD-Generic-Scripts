#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

#*******************************************************************************

DIRNAME = 'experiment_MEAS-GHA-Base01'
YMAX    = 300

targfile = os.path.join('..',DIRNAME,'param_dict.json')
with open(targfile) as fid01:
  param_dict = json.load(fid01)

targfile = os.path.join('..',DIRNAME,'data_brick.json')
with open(targfile) as fid01:
  dbrick = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
tvals    = dbrick.pop('tstamps')
ntstp    = len(tvals)

ref_dat = [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
             4,  17,  26,  11,  11,   6,   5,   8,  13,  17,  12,   6,
            32,  47,  73,  48,  39,  33,  15,  27,  11,   7,  14,   1,
            38,  48,  58,  71,  25,  10,  16,  14,  20,   5,   9,   8,
            38,  35,  21,  13,  14,  16,   2,   1,   1,   1,   0,   0,
             1,   5,   3,   7,  11,   4,   3,   3,   5,   4,   5,   0,
             6,   5,   9,  39,  78,  90,  74,  96,  38,  17,   2,   1,
            12,   4,  14,  80, 191, 167,  52,   1,   5, 166, 147, 104,
           161, 194,  51,  66, 144,  39,  19,  66,  95, 198, 137,  38,
            30, 260, 250, 242, 100,  37,  43,  72,  47,  77, 189,  73,
            16,   7,   3,  10,   9,  11,   7,   9,  11,   7,   7,   0]


# Figure
fig01 = plt.figure(figsize=(8,6))

axs01  = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(b=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(b=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

yval = np.array(ref_dat)
xval = np.array(tvals)/365+1900


axs01.plot(xval[12:],yval[12:],color='k',linewidth=2)
axs01.set_ylabel('Monthly Cases',fontsize=14)
axs01.set_xlim(2010,2020)
axs01.set_ylim(   0, YMAX)
axs01.tick_params(axis='x', labelsize=16)

sia01 = np.array([40460,40460])/365+1900
axs01.plot(sia01,[0,YMAX],color='C0',linewidth=3)

sia02 = np.array([41508,41508])/365+1900
axs01.plot(sia02,[0,YMAX],color='C2',linewidth=5)

sia03 = np.array([43365,43365])/365+1900
axs01.plot(sia03,[0,YMAX],color='C0',linewidth=3)

#plt.savefig('fig_reference01.png')
plt.savefig('fig_reference01.svg')

plt.close()

#*******************************************************************************

