#*******************************************************************************

import os, sys, json

import numpy              as np
import matplotlib.pyplot  as plt

ext_py_path = os.path.join('..','Assets','python')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

from refdat_age_pyr import age_pyr_fun

#*******************************************************************************

intlist   = [221,222,223,224]
pname_long = ['AFRO:ANG','AFRO:ETH','EURO:ITA','EURO:UKR']
pname      = ['Angola','Ethiopia','Italy','Ukraine']


# Figure
fig01 = plt.figure(figsize=(12.8,9.6))

axs00 = fig01.add_subplot(111)

axs00.spines['top'].set_color('none')
axs00.spines['bottom'].set_color('none')
axs00.spines['left'].set_color('none')
axs00.spines['right'].set_color('none')
axs00.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

for k0 in range(len(pname)):

  pn  = pname[k0]
  pnl = pname_long[k0]
  figint = intlist[k0]
  axs01  = fig01.add_subplot(figint)

  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_xlim(-0.12,0.12)
  axs01.set_ylim(0,80)

  ticloc  = [0, 10, 20, 30, 40, 50, 60, 70, 80]
  cum_lab = ['0', '10', '20', '30', '40', '50', '60', '70', '80']
  axs01.set_yticks(ticks=ticloc)
  axs01.set_yticklabels(cum_lab)

  ticloc = [-0.1, -0.05, 0, 0.05, 0.10]
  mo_lab = ['10%','5%','0','5%','10%']
  axs01.set_xticks(ticks=ticloc)
  axs01.set_xticklabels(mo_lab)

  axs01.text(-0.111,72,pn,fontsize=16)

  daty = np.array(age_pyr_fun(pnl)[1])
  datx = np.arange(2.5,80,5)
  axs01.barh(datx, daty/2,color='C0',height=4.95,edgecolor='k')
  axs01.barh(datx,-daty/2,color='C0',height=4.95,edgecolor='k')

axs00.set_xlabel('Percentage',fontsize=26)
axs00.set_ylabel('Age (years)',fontsize=26)

#plt.savefig('fig_poppyr01.png')
plt.savefig('fig_poppyr01.svg')

plt.close()

#*******************************************************************************