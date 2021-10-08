#********************************************************************************
#
# Python 3.6.0
#
#*******************************************************************************

import os, json

import numpy as np

# ******************************************************************************

OUTPUT_DIR = 'output'

if __name__ == '__main__':

  exp_dat01 = dict()
  exp_dat02 = dict()
  exp_dat03 = dict()

  for fname in os.listdir(OUTPUT_DIR):

    if(not fname.startswith('inf_circ')):
      continue

    sim_num = int(fname[9:14])
    sidx_str  = '{:05d}'.format(sim_num)

    temp_dat = np.loadtxt(os.path.join(OUTPUT_DIR,fname),delimiter=',')
    t_vec    = temp_dat[0, :]
    dbrick   = temp_dat[1:,:]

    print(sidx_str, dbrick.shape, np.count_nonzero(np.sum(dbrick,axis=1)))

    fatime    = np.argmax(dbrick,axis=1)
    exp_dat01[sidx_str] = fatime.tolist()

    totinf    = np.sum(dbrick,axis=0)
    exp_dat02[sidx_str] = totinf.tolist()

    maxextent = np.count_nonzero(dbrick,axis=0)/dbrick.shape[0]
    exp_dat03[sidx_str] = maxextent.tolist()


  with open('data_fatime.json','w') as fid01:
    json.dump(dict(exp_dat01),fid01,sort_keys=True)

  with open('data_totinf.json','w') as fid01:
    json.dump(dict(exp_dat02),fid01,sort_keys=True)

  with open('data_maxextent.json','w') as fid01:
    json.dump(dict(exp_dat03),fid01,sort_keys=True)

# ******************************************************************************
