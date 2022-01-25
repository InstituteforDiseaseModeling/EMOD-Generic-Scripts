#********************************************************************************
#
#*******************************************************************************

import os, sys, shutil, json

import numpy as np

# ******************************************************************************


# Paths
PATH_TEMP  = os.path.abspath('temp_dir_alt')

mem_set = list()
tim_set = list()

for k1 in range(1500):
  with open(os.path.join(PATH_TEMP,'StdOut{:05d}.txt'.format(k1))) as fid01:
    flines = fid01.readlines()

  for lval in flines[::-1]:
    if('Controller executed' in lval):
      tvals = [int(val) for val in lval.split()[0].split(':')]
      tim_set.append(tvals[0]*60 + tvals[1] + tvals[2]/60)
    if('Peak working-set' in lval):
      page_mb = int(lval.strip().split()[-1][:-2])
      mem_set.append(page_mb)
      break


with open('comp_prof.json','w') as fid01:
  dat_dict = {'mem':mem_set, 'time':tim_set}
  json.dump(dat_dict,fid01,indent=3)


# ******************************************************************************