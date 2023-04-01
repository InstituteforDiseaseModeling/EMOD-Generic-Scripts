#********************************************************************************
#
#*******************************************************************************

import os

from idmtools.core.platform_factory                           import  Platform
#from idmtools_platform_comps.ssmt_work_items.comps_workitems  import  SSMTWorkItem
from idmtools.core.id_file                                    import  write_id_file

# Ought to go in emodpy
import sys
LOCAL_PATH = os.path.abspath(os.path.join('..','..','local_python'))
sys.path.insert(0, LOCAL_PATH)
from emod_exp import calib_from_def_file

# ******************************************************************************


# Paths
PATH_EXP_DEF  = os.path.abspath('param_dict.json')
PATH_PYTHON   = os.path.abspath(os.path.join('..', 'Assets', 'python'))
PATH_DATA     = os.path.abspath(os.path.join('..', 'Assets', 'data'))
PATH_ENV      = os.path.abspath(os.path.join('..', '..', 'env_Alma9', 'EMOD_ENV.id'))
PATH_EXE      = os.path.abspath(os.path.join('..', '..', 'env_Alma9', 'EMOD_EXE.id'))


# Start a calibration on COMPS
def run_the_calibration():

  # Prepare the platform
  plat_obj = Platform(block        = 'COMPS',
                      endpoint     = 'https://comps.idmod.org',
                      environment  = 'Calculon')

  # Create calibration object
  wi_obj = calib_from_def_file(PATH_EXP_DEF, PATH_PYTHON, PATH_ENV, PATH_EXE, PATH_DATA, LOCAL_PATH)

  # Send work item to COMPS; start processing
  wi_obj.run(wait_on_done=False)

  # Save work item id to file
  write_id_file('COMPS_ID.id', wi_obj)
  print()
  print(wi_obj.uid.hex)

  return None

# ******************************************************************************

if(__name__ == "__main__"):

  # Calibration, Calibration, Calibration
  # Calibration, Calibration, Calibration
  # Calibration, Calibration, oh, oh, oh Calibration
  run_the_calibration()

# ******************************************************************************