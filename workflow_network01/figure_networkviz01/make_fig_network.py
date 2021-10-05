#********************************************************************************

import os, json
import numpy as np

from aux_defaultgrid import svg_defaultgrid

#********************************************************************************


DIRNAME = 'experiment_network01'

# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join('..',DIRNAME,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

net_coef  = np.array(param_dict['EXP_VARIABLE']['network_coefficient'])
netc_vals = np.unique(net_coef)

# One animation for each coefficient value
for k1 in range(netc_vals.shape[0]):
  sim_idx = np.argwhere(net_coef==netc_vals[k1])[0][0]
  inf_dat = data_brick['{:05d}'.format(sim_idx)]
  f_lab   = '{:1.0e}'.format(netc_vals[k1])
  f_lab   = f_lab.replace('+','')
  svg_defaultgrid(inf_dat, sim_idx, f_lab)

#*******************************************************************************