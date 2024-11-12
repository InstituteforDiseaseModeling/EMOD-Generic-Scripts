# *****************************************************************************
#
# *****************************************************************************

import os
import sys

from idmtools.core.platform_factory import Platform

# Ought to go in emodpy
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'local_python')))
from emod_exp import exp_from_def_file
from py_assets_common.emod_constants import P_FILE

# *****************************************************************************

# Paths
PATH_EXP_DEF = os.path.abspath(P_FILE)
PATH_PYTHON = os.path.abspath(os.path.join('..', 'Assets', 'python'))
PATH_DATA = os.path.abspath(os.path.join('..', 'Assets', 'data'))

# *****************************************************************************


# Start an experiment locally using Docker
def run_sims():

    # Prepare the platform
    plat_obj = Platform(block='Container',
                        job_directory='docker_test01',
                        docker_image='emod_env:latest')

    # Create experiment object
    exp_obj = exp_from_def_file(PATH_EXP_DEF, PATH_PYTHON, None, PATH_DATA)

    # Start processing simulations
    plat_obj.run_items(exp_obj)

    return None

# ******************************************************************************


if (__name__ == "__main__"):

    run_sims()

# ******************************************************************************
