#********************************************************************************
#
#*******************************************************************************

import os

from idmtools.core.platform_factory                           import  Platform
from idmtools.assets                                          import  AssetCollection
from idmtools_models.python.python_task                       import  PythonTask
from idmtools_platform_comps.ssmt_work_items.comps_workitems  import  SSMTWorkItem

# ******************************************************************************


# Paths
PATH_PYTHON   = os.path.abspath(os.path.join('..', 'Assets', 'python'))
PATH_DATA     = os.path.abspath(os.path.join('..', 'Assets', 'data'))
PATH_ENV      = os.path.abspath(os.path.join('..', '..', 'env_Debian10', 'EMOD_ENV.id'))
PATH_EXE      = os.path.abspath(os.path.join('..', '..', 'env_Debian10', 'EMOD_EXE.id'))
PATH_LOCAL    = os.path.abspath(os.path.join('..', '..', 'local_python'))


# Start a work item on COMPS
def run_the_calibration():

  # Connect to COMPS; needs to be the same environment used to run the sims
  plat_obj = Platform(block        = 'COMPS',
                      endpoint     = 'https://comps.idmod.org',
                      environment  = 'Calculon')

  # Create python task for SSMT work item
  task_obj = PythonTask(python_path = 'python3',
                        script_path = os.path.join(PATH_LOCAL,'emod_calib.py'))

  # Add everything needed to run an experiment and ID from the initial sweep
  task_obj.common_assets.add_directory(PATH_PYTHON, relative_path='python')
  task_obj.common_assets.add_directory(PATH_DATA,   relative_path='data')
  task_obj.common_assets.add_directory(PATH_LOCAL)
  task_obj.common_assets.add_asset(PATH_ENV)
  task_obj.common_assets.add_asset(PATH_EXE)

  # Add working directory assets
  ac_obj = AssetCollection()
  ac_obj.add_asset('COMPS_ID.id')
  ac_obj.add_asset('idmtools.ini')

  # Es liebten alle Frauen
  wi_obj = SSMTWorkItem(name             = 'Calibd_EMOD',
                        task             = task_obj,
                        transient_assets = ac_obj)
  wi_obj.run(wait_on_done=False)


  return None

# ******************************************************************************

if(__name__ == "__main__"):

  # Calibration, Calibration, Calibration
  # Calibration, Calibration, Calibration
  # Calibration, Calibration, oh, oh, oh Calibration
  run_the_calibration()

# ******************************************************************************