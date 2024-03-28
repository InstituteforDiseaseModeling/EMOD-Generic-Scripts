# *****************************************************************************
#
# *****************************************************************************

import os
import sys

from idmtools.core.platform_factory import Platform

# Ought to go in emodpy
LOCAL_PATH = os.path.abspath(os.path.join('..', '..', 'local_python'))
sys.path.insert(0, LOCAL_PATH)
from emod_exp import calib_from_def_file
from emod_reduce import FILENAME_ID

# *****************************************************************************

# Paths
PATH_EXP_DEF = os.path.abspath('param_dict.json')
PATH_PYTHON = os.path.abspath(os.path.join('..', 'Assets', 'python'))
PATH_DATA = os.path.abspath(os.path.join('..', 'Assets', 'data'))
PATH_EXE = os.path.abspath(os.path.join('..', '..', 'env_Debian12'))

# *****************************************************************************


# Start a calibration on COMPS
def run_the_calibration():

    # Prepare the platform
    Platform(block='COMPS',
             endpoint='https://comps.idmod.org',
             environment='Calculon')

    # Create calibration object
    wi_obj = calib_from_def_file(PATH_EXP_DEF, PATH_PYTHON,
                                 PATH_EXE, PATH_DATA, LOCAL_PATH)

    # Send work item to COMPS; start processing
    wi_obj.run(wait_on_done=False)

    # Save work item id to file
    wi_obj.to_id_file(FILENAME_ID)
    print()
    print(wi_obj.uid.hex)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    # Calibration, Calibration, Calibration
    # Calibration, Calibration, Calibration
    # Calibration, Calibration, oh, oh, oh Calibration
    run_the_calibration()

# *****************************************************************************
