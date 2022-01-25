#********************************************************************************
#
#*******************************************************************************

import os, sys, shutil, json

from idmtools.core.platform_factory                    import  Platform
from idmtools.core.enums                import  ItemType
from idmtools_platform_comps.utils.download.download   import  DownloadWorkItem
from idmtools.core.id_file                             import  read_id_file

import numpy as np

# ******************************************************************************


# Paths
PATH_TEMP  = os.path.abspath('temp_dir_alt')



def get_sim_files():

  # Connect to COMPS; needs to be the same environment used to run the sims
  plat_obj = Platform(block        = 'COMPS',
                      endpoint     = 'https://comps.idmod.org',
                      environment  = 'Calculon')

  # Get initial experiment object
  (exp_id,_,_,_) = read_id_file('COMPS_ID.id')
  exp_obj = plat_obj.get_item(item_id=exp_id, item_type=ItemType.EXPERIMENT)


  # Get logging for each simulation
  logfile      = 'StdOut.txt'
  k1           = 0
  for sim_obj in exp_obj.simulations:
    resp_dict    = plat_obj.get_files(sim_obj,[logfile])
    print(resp_dict.keys())
    logdat = resp_dict[logfile].decode()
    with open(os.path.join(PATH_TEMP,'StdOut{:05d}.txt'.format(k1)), 'w') as fid01:
      fid01.write(logdat)
    k1 += 1


  return


# ******************************************************************************

if(__name__ == "__main__"):

  get_sim_files()

# ******************************************************************************