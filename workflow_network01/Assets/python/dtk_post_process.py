#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Post-process spatial reporter
  with open(os.path.join(output_path,'SpatialReport_New_Infections.bin'),'rb') as fid01:
    num_nodes = np.fromfile(fid01, dtype=np.int32,   count=        1)[0]
    num_times = np.fromfile(fid01, dtype=np.int32,   count=        1)[0]
    node_ids  = np.fromfile(fid01, dtype=np.int32,   count=num_nodes)
    node_vals = np.fromfile(fid01, dtype=np.float32, count=       -1)
    node_vals = node_vals.reshape((num_times,-1)).T

  # Take all the data
  parsed_dat[key_str] = node_vals.tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
