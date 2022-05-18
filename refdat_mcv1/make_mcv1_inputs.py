#*******************************************************************************

import os, json, sys

import numpy               as np
import matplotlib.pyplot   as plt

sys.path.insert(0, os.path.join('..','refdat_namesets'))
from  aux_namematch  import  reprule, tlc_dict
from  aux_namematch  import  adm01_alias_dict, adm02_alias_dict

#*******************************************************************************


# Set three letter country code
COUNTRY = 'NGA'


# Parse CSV
ihme_file = r'IHME_LMIC_MCV1_2000_2019_ADMIN_2_Y2020M12D16.CSV'
with open(ihme_file, errors='ignore') as fid01:
  flines = [val.strip().split(',') for val in fid01.readlines()[1:]]

dat_lines = [val for val in flines if reprule(val[1])==tlc_dict[COUNTRY]]
year_vec  = np.arange(2000,2020)


# Get nameset
fname = os.path.join('..','refdat_namesets','{:s}_NAMES_ADMIN02.csv'.format(COUNTRY))
with open(fname) as fid01:
  adm02_names = sorted([val.strip() for val in fid01.readlines()])

adm02_short = sorted(list(set([val.rsplit(':',1)[1] for val in adm02_names])))
adm01_short = sorted(list(set([val.rsplit(':',2)[1] for val in adm02_names])))
adm00_short = sorted(list(set([val.rsplit(':',3)[1] for val in adm02_names])))
who_region  = adm02_names[0].split(':')[0]

DATA_SET   = 'IHME'
adm1_alias = adm01_alias_dict[DATA_SET][COUNTRY]
adm2_alias = adm02_alias_dict[DATA_SET][COUNTRY]


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
    mcv1_dict[dotname] = np.zeros(year_vec.shape[0])

  year_val = int(lval[6])
  idx_val  = year_val%2000
  frac_val = float(lval[13])
  mcv1_dict[dotname][idx_val] = frac_val


# Format outputs
mcv1_mat = np.zeros((len(mcv1_dict),len(year_vec)))
sum_dict = dict()
sum_dict['namevec'] = sorted(list(mcv1_dict.keys()))
sum_dict['timevec'] = (365.0*(year_vec+0.5-1900)).tolist()
for k1 in range(len(sum_dict['namevec'])):
  mcv1_mat[k1,:] = mcv1_dict[sum_dict['namevec'][k1]]


# Write data files
with open('{:s}_MCV1.json'.format(COUNTRY),'w') as fid01:
  json.dump(sum_dict, fid01, indent=2, sort_keys=True)

np.savetxt('{:s}_MCV1.csv'.format(COUNTRY),mcv1_mat,delimiter=',',fmt='%5.3f')

#*******************************************************************************
