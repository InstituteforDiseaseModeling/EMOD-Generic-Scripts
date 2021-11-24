#********************************************************************************
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


  # Calculate total attack rate and store in a json dict
  with open(os.path.join(output_path,'InsetChart.json')) as fid01:
    inset_chart = json.load(fid01)

  tot_inf = np.sum(inset_chart['Channels']['New Infections']['Data'])
  tot_pop = inset_chart['Channels']['Statistical Population']['Data'][-1]

  parsed_dat[key_str] = int(tot_inf)/tot_pop


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
