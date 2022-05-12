#*******************************************************************************

import os, json, sys

import numpy               as np
import matplotlib.pyplot   as plt

sys.path.insert(0, os.path.join('..','refdat_namesets'))
from  aux_namematch  import  reprule, tlc_dict
from  aux_namematch  import  adm01_alias_dict, adm02_alias_dict

#*******************************************************************************


COUNTRY = 'NGA'
DATA    = 'IHME'


# Parse CSV
fname = 'IHME_LMIC_MCV1_2000_2019_ADMIN_2_Y2020M12D16.CSV'
with open(fname, errors='ignore') as fid01:
  flines = [val.strip().split(',') for val in fid01.readlines()[1:]]

dat_lines = [val for val in flines if val[1]==tlc_dict[COUNTRY]]


# Get nameset
fname = os.path.join('..','refdat_namesets','{:s}_NAMES_ADMIN02.csv'.format(COUNTRY))
with open(fname) as fid01:
  adm02_names = sorted([val.strip() for val in fid01.readlines()])

adm02_short = sorted(list(set([val.rsplit(':',1)[1] for val in adm02_names])))
adm01_short = sorted(list(set([val.rsplit(':',2)[1] for val in adm02_names])))
adm00_short = sorted(list(set([val.rsplit(':',3)[1] for val in adm02_names])))
who_region  = adm02_names[0].split(':')[0]

adm1_alias = adm01_alias_dict[DATA][COUNTRY]
adm2_alias = adm02_alias_dict[DATA][COUNTRY]


# Name matching
mcv1_dict = dict()
for lval in dat_lines:
  adm0_val = reprule(lval[1])
  if(adm0_val not in adm00_short):
    raise Exception(adm0_val+' not found in admin00.')

  adm1_val = reprule(lval[3])
  if(adm1_val in adm1_alias):
    adm1_val = adm1_alias[adm1_val]
  if(adm1_val not in adm01_short):
    raise Exception(adm1_val+' not found in admin01.')

  adm2_val = reprule(lval[5])
  if(adm2_val in adm2_alias):
    adm2_val = adm2_alias[adm2_val]
  if(adm2_val not in adm02_short):
    raise Exception(adm2_val+' not found in admin02.')

  dotname = ':'.join([who_region,adm0_val,adm1_val,adm2_val])
  if(dotname not in adm02_names):
    raise Exception(dotname+' not found.')
  if(dotname not in mcv1_dict):
    mcv1_dict[dotname] = list()


print(len(mcv1_dict))
1/0



#Get admin01 name set
admin01 = sorted(list(dict_birth.keys()))


# Propagate aliases in mortality data
for reg_name in list(dict_death.keys()):
  if(reg_name in dict_alias):
    for sub_reg in dict_alias[reg_name]:
      dict_death[sub_reg] = dict_death[reg_name]


# Sum populations to admin01
adm01_pop = dict()
for k1 in range(len(admin01)):
  cum_pop = 0
  for adm02 in dict_pop_admin02:
    if(adm02.startswith(admin01[k1]+':')):
      cum_pop += dict_pop_admin02[adm02][0]
  adm01_pop[admin01[k1]] = cum_pop


# Figure
fig01 = plt.figure(figsize=(49,42))


# Pyramid plots
adm01_growth = dict()
for k1 in range(len(admin01)):
  axs01 = fig01.add_subplot(7,7,k1+1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_xlabel('Percentage', fontsize=14)
  axs01.set_ylabel('Age (yrs)', fontsize=14)

  axs01.set_xlim( -12,  12)
  axs01.set_ylim(   0, 100)

  ticloc = [-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12]
  ticlab = ['12', '10', '8', '6', '4', '2', '0', '2', '4', '6', '8', '10', '12']
  axs01.set_xticks(ticks=ticloc)
  axs01.set_xticklabels(ticlab)

  brth_rate = dict_birth[admin01[k1]]
  d_rate_y  = dict_death[admin01[k1]]
  d_rate_x  = dict_death['BIN_EDGES']
  force_v   = 12*[1.0] # No seasonal forcing
  (grow_rate, age_x, age_y) = demoCalc_AgeDist(brth_rate,d_rate_x,d_rate_y)

  ydat        = np.array(pop_age_days)/365.0 - 2.5
  xdat        = 100*np.diff(np.interp(pop_age_days, age_y, age_x))

  axs01.barh(ydat[1:],  xdat/2.0, height=4.75, color=CF)
  axs01.barh(ydat[1:], -xdat/2.0, height=4.75, color=CM)

  adm_name = admin01[k1].rsplit(':',1)[1]
  axs01.text( -11,   92.5, adm_name, fontsize=18)
  axs01.text(   2.1, 92.5, 'GrowthRate {:4.2f}%'.format(100*(grow_rate-1)), fontsize=18)
  adm01_growth[admin01[k1]] = grow_rate

plt.tight_layout()
plt.savefig('fig_pyr_mat_01.png')
plt.close()


# Figure
fig01 = plt.figure(figsize=(8,6))


# Population plot
axs01 = fig01.add_subplot(1,1,1)
plt.sca(axs01)
axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('Population (M)', fontsize=14)

axs01.set_xlim( 2015, 2025)
axs01.set_ylim(  180, 240)

xvals = np.arange(2015,2026)
yvals = xvals*0
for k1 in range(xvals.shape[0]):
  yvals[k1] = np.sum([adm01_pop[val]*np.power(adm01_growth[val],xvals[k1]-2015) for val in admin01])/1e6

ny = np.power(yvals/yvals[0],1/np.arange(11))
print(100*(ny-1))

axs01.plot(xvals,yvals)

plt.tight_layout()
plt.savefig('fig_pop_vec_01.png')
plt.close()


#*******************************************************************************
