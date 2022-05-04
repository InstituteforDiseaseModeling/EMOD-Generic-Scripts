#********************************************************************************
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index
  TIME_DELTA    = gdata.var_params['nTsteps']


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Output parcing
  databrick = np.zeros((17,TIME_DELTA))
  with open(os.path.join(output_path,'PropertyReport.json')) as fid01:
    rep_file = json.load(fid01)
    rep_channels = rep_file['Channels']
    for channel_value in rep_channels:
      if('New Infections' not in channel_value):
        continue
      else:
        infDat = np.array(rep_channels[channel_value]['Data'])
      for k1 in range(16):
        agestr = 'age{:02d}'.format(5*k1)
        if(agestr in channel_value):
          databrick[k1,:] += infDat
      if('HCW' in channel_value):
          databrick[-1,:] += infDat  
  parsed_dat[key_str] = databrick.tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as tmpFile:
    json.dump(parsed_dat, tmpFile)


  return None

#********************************************************************************
