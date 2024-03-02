#********************************************************************************

import os, json
import numpy as np

from aux_defaultgrid import svg_defaultgrid

#********************************************************************************


DIRNAME = 'experiment_sweepRI_popEQL_noSIAs'
SIM_IDX = 3


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join('..',DIRNAME,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)


sim_idx_str = '{:05d}'.format(SIM_IDX)


inf_dat = np.array(data_brick[sim_idx_str]['inf_nodes'])
inf_dat = np.transpose(np.sum(inf_dat, axis=1))


pyr_mat = np.array(data_brick[sim_idx_str]['pyr_data'])
pop_tot = np.sum(pyr_mat,axis=1)
pop_tot = np.diff(pop_tot)/2.0 + pop_tot[:-1]
pop_x   = np.arange(0, 12*pop_tot.shape[0], 12)
pop_vec = np.interp(np.arange(inf_dat.shape[1]), pop_x, pop_tot)


inf_dat_norm = inf_dat/pop_vec*1e5


# Requires nodes to be in a square (1, 4, 9, 16, 25, 36, etc.)
fig_lab   =   '00'
unused    =   None
svg_defaultgrid(inf_dat_norm, unused, fig_lab)


#*******************************************************************************