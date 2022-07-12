#*******************************************************************************

import os, json, sys

#*******************************************************************************

DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]

#*******************************************************************************


# Set three letter country code
COUNTRY = ''


# Get nameset
fname = os.path.join('..','refdat_namesets','{:s}_NAMES_LEV02.csv'.format(COUNTRY))
with open(fname) as fid01:
  lev02_names = sorted([val.strip() for val in fid01.readlines()])

lev01_names = sorted(list(set([val.rsplit(':',1)[0] for val in lev02_names])))
lev00_names = sorted(list(set([val.rsplit(':',2)[0] for val in lev02_names])))
who_region  = lev02_names[0].split(':')[0]


# Parse CSV
idm_file = r'IDM_MCV_SIA.csv'
with open(idm_file, errors='ignore') as fid01:
  flines = [val.strip().split(',') for val in fid01.readlines()[1:]]


# Process data
sia_input_dict = dict()
sia_tot        = 0

for lval in flines:
  dotparts = lval[0].split(':')

  # Validate table
  if(':'.join(dotparts[0:1]) != who_region):
    continue

  if(':'.join(dotparts[0:2]) not in lev00_names):
    continue

  if(len(dotparts)>2 and ':'.join(dotparts[:3]) not in lev01_names):
    raise Exception(lval[0]+' not found in nameset.')

  if(len(dotparts)>3 and ':'.join(dotparts[:4]) not in lev02_names):
    raise Exception(lval[0]+' not found in nameset.')

  new_key = True
  age_min = int(365.0*float(lval[4]))
  age_max = int(365.0*float(lval[5]))
  targ_frac = float(lval[6])
  date      = int(365.0*(int(lval[1])-1900) + sum(DAY_BINS[:(int(lval[2])-1)]) + int(lval[3]))

  for sia_key in sia_input_dict:
    if(sia_input_dict[sia_key]['date']      == date      and
       sia_input_dict[sia_key]['age_min']   == age_min   and
       sia_input_dict[sia_key]['age_max']   == age_max   and
       sia_input_dict[sia_key]['targ_frac'] == targ_frac):
      new_key = False
      sia_input_dict[sia_key]['nodes'].append(lval[0])
      break

  if(new_key):
    sia_tot     = sia_tot + 1
    new_sia_key = COUNTRY + '_{:s}_{:d}'.format(lval[1],sia_tot)
    sia_input_dict[new_sia_key]              = dict()
    sia_input_dict[new_sia_key]['date']      = date
    sia_input_dict[new_sia_key]['age_min']   = age_min
    sia_input_dict[new_sia_key]['age_max']   = age_max
    sia_input_dict[new_sia_key]['targ_frac'] = targ_frac
    sia_input_dict[new_sia_key]['nodes']     = [lval[0]]


# Write data files
with open('{:s}_MCV_SIA.json'.format(COUNTRY),'w') as fid01:
  json.dump(sia_input_dict, fid01, indent=2, sort_keys=True)

#*******************************************************************************
