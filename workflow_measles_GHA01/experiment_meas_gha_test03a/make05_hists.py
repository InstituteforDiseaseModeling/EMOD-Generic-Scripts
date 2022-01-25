#********************************************************************************
#
#*******************************************************************************

import os, sys, shutil, json

import numpy as np

import matplotlib.pyplot  as plt


# ******************************************************************************


with open('comp_prof.json') as fid01:
  dat_dict = json.load(fid01)

with open('param_dict.json') as fid01:
  param_dict = json.load(fid01)

var1 = param_dict['EXP_VARIABLE']['adm01_case_threshold']
var2 = param_dict['EXP_VARIABLE']['log10_min_reporting']

gidx = (np.array(var1) > 0) & (np.array(var2) < 3)

# Figure
fig01 = plt.figure(figsize=(8,6))

axs00 = fig01.add_subplot(111)

axs00.spines['top'].set_color('none')
axs00.spines['bottom'].set_color('none')
axs00.spines['left'].set_color('none')
axs00.spines['right'].set_color('none')
axs00.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)


axs01 = fig01.add_subplot(111,label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

#axs01.set_title('')
axs01.set_xlabel('Max Resident Set Size (MB)')
#axs01.set_ylabel('')

axs01.set_xlim(900,1600)

#ticloc = [60, 90, 120, 151, 181]
#ticlab = ['Mar','Apr','May','Jun']
#axs01.set_xticks(ticks=ticloc)
#axs01.set_xticklabels(ticlab)

#axs01.set_ylim()

#ticloc = [0, 5e3, 10e3, 15e3, 20e3, 25e3]
#ticlab = ['0','5k','10k','15k','20k','25k']
#axs01.set_yticks(ticks=ticloc)
#axs01.set_yticklabels(ticlab)

axs01.hist(np.array(dat_dict['mem'])[gidx],edgecolor='k',bins=50)

plt.tight_layout()
plt.savefig('memory01.png')
plt.close()


# Figure
fig01 = plt.figure(figsize=(8,6))

axs00 = fig01.add_subplot(111)

axs00.spines['top'].set_color('none')
axs00.spines['bottom'].set_color('none')
axs00.spines['left'].set_color('none')
axs00.spines['right'].set_color('none')
axs00.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)


axs01 = fig01.add_subplot(111,label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

#axs01.set_title('')
axs01.set_xlabel('Wall Time (min)')
#axs01.set_ylabel('')

axs01.set_xlim(30,150)

#ticloc = [60, 90, 120, 151, 181]
#ticlab = ['Mar','Apr','May','Jun']
#axs01.set_xticks(ticks=ticloc)
#axs01.set_xticklabels(ticlab)

#axs01.set_ylim()

#ticloc = [0, 5e3, 10e3, 15e3, 20e3, 25e3]
#ticlab = ['0','5k','10k','15k','20k','25k']
#axs01.set_yticks(ticks=ticloc)
#axs01.set_yticklabels(ticlab)

#axs01.hist(dat_dict['time'],edgecolor='k',bins=50)
axs01.hist(np.array(dat_dict['time'])[gidx],edgecolor='k',bins=50)


plt.tight_layout()
plt.savefig('walltime01.png')
plt.close()


# Figure
fig01 = plt.figure(figsize=(8,6))

axs00 = fig01.add_subplot(111)

axs00.spines['top'].set_color('none')
axs00.spines['bottom'].set_color('none')
axs00.spines['left'].set_color('none')
axs00.spines['right'].set_color('none')
axs00.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)


axs01 = fig01.add_subplot(111,label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

#axs01.set_title('')
axs01.set_xlabel('Wall Time (min)')
axs01.set_ylabel('Max Resident Set Size (MB)')

axs01.set_xlim(30,150)
axs01.set_ylim(900,1600)

#ticloc = [60, 90, 120, 151, 181]
#ticlab = ['Mar','Apr','May','Jun']
#axs01.set_xticks(ticks=ticloc)
#axs01.set_xticklabels(ticlab)

#axs01.set_ylim()

#ticloc = [0, 5e3, 10e3, 15e3, 20e3, 25e3]
#ticlab = ['0','5k','10k','15k','20k','25k']
#axs01.set_yticks(ticks=ticloc)
#axs01.set_yticklabels(ticlab)

#axs01.hist(dat_dict['time'],edgecolor='k',bins=50)
axs01.plot(np.array(dat_dict['time']),np.array(dat_dict['mem']),'k.')


plt.tight_layout()
plt.savefig('corr01.png')
plt.close()

# ******************************************************************************