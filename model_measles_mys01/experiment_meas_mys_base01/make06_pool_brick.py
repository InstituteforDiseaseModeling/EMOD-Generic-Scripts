#********************************************************************************
#
#*******************************************************************************

import os, sys, json

from idmtools.core.platform_factory     import  Platform
from idmtools.core.id_file              import  read_id_file

from COMPS.Data                         import  WorkItem

# ******************************************************************************

def get_data_brick():

  # Connect to COMPS
  plat  = Platform(block        = 'COMPS',
                   endpoint     = 'https://comps.idmod.org',
                   environment  = 'Calculon')

  # Get Work Item ID for calibration
  (wi_id,_,_,_) = read_id_file('COMPS_ID.id')
  wi_obj        = WorkItem.get(wi_id)

  # Calibration parameters
  with open('param_dict.json') as fid01:
    param_dict = json.load(fid01)

  # Prep file request list
  filelist  = list()
  for k1 in range(param_dict['NUM_ITER']):
    filelist.append('param_dict_iter{:02d}.json'.format(k1))
    filelist.append('data_brick_iter{:02d}.json'.format(k1))

  # Download reduced output
  resp_dict = plat.get_files(wi_obj, filelist)

  # Process and save response
  merged_params = dict()
  merged_data   = dict()
  for key_str in resp_dict:
    iter_str = key_str[-7:-5]
    dict_val = json.loads(resp_dict[key_str].decode())
    if('param' in key_str):
      merged_params[iter_str] = dict_val
    if('data' in key_str):
      merged_data[iter_str]   = dict_val

  with open('param_dict_iters.json','w') as fid01:
    json.dump(merged_params,fid01)
  with open('data_brick_iters.json','w') as fid01:
    json.dump(merged_data,  fid01)

  return None

# ******************************************************************************

if(__name__ == "__main__"):

  get_data_brick()

# ******************************************************************************