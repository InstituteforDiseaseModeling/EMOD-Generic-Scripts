#********************************************************************************
#
#*******************************************************************************

import os, sys, shutil, json

from idmtools.core.platform_factory     import  Platform
from idmtools.core.enums                import  ItemType
from idmtools.core.id_file              import  read_id_file

# ******************************************************************************

NITER = 8

def get_sim_files():

  # Connect to COMPS; needs to be the same environment used to run work item
  plat_obj  = Platform(block        = 'COMPS',
                       endpoint     = 'https://comps.idmod.org',
                       environment  = 'Calculon')

  # Get Work Item ID
  (wi_id,_,_,_) = read_id_file('CALIB_ID.id')
  wi_obj = plat_obj.get_item(item_id=wi_id, item_type=ItemType.WORKFLOW_ITEM)

  # Get files
  filelist = list()
  for k1 in range(NITER+1):
    filelist.append('param_dict_iter{:02d}.json'.format(k1))
    filelist.append('data_calib_iter{:02d}.json'.format(k1))
  resp_dict = plat_obj.get_files(wi_obj,filelist)
  for fname in filelist:
    temp_dict = json.loads(resp_dict[fname].decode())
    with open(fname, 'w') as fid01:
      json.dump(temp_dict, fid01)

# ******************************************************************************

if(__name__ == "__main__"):

  get_sim_files()

# ******************************************************************************