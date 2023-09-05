#*******************************************************************************

import os, sys, json

sys.path.append(os.path.join('..','Assets','python'))

import numpy              as np
import matplotlib.pyplot  as plt
import matplotlib.patches as patch
import matplotlib         as mpl

from dtk_post_process   import   ref_dat_01
from global_data        import   start_year, start_log

#*******************************************************************************

DIRNAME = 'experiment_meas_mys_base01'
YMAX    = 300

# Figure
fig01 = plt.figure(figsize=(8,6))

axs01  = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

yval = np.array(ref_dat_01)
xval = np.arange(2016, 2024, 1/12) + 1/24

axs01.bar(xval,yval,color='r',linewidth=0.5,edgecolor='k',width=0.9/12)
axs01.set_ylabel('Monthly Cases - Observed',fontsize=16)

axs01.set_xlim(2016, 2024)
axs01.set_ylim(   0, YMAX)

ticloc = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
ticlab = ['','','','','','','', '']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)
for k1 in ticloc:
  axs01.text(k1+0.5,-0.04*YMAX,str(k1),fontsize=11,ha='center')

#sia01 = np.array([40460,40460])/365+1900
#axs01.plot(sia01,[0,YMAX],color='c',linewidth=3,ls=':')
#axs01.text(sia01[0]+0.2,0.9*YMAX,'SIA',fontsize=13)

#sia02 = np.array([41508,41508])/365+1900
#axs01.plot(sia02,[0,YMAX],color='c',linewidth=5,ls='--')
#axs01.text(sia02[0]+0.2,0.9*YMAX,'RCV Catch-up',fontsize=13)

#sia03 = np.array([43365,43365])/365+1900
#axs01.plot(sia03,[0,YMAX],color='c',linewidth=3,ls=':')
#axs01.text(sia03[0]+0.2,0.9*YMAX,'SIA',fontsize=13)

plt.tight_layout()
plt.savefig('fig_reference_01.png')
plt.close()

#*******************************************************************************

