# *****************************************************************************
#
# *****************************************************************************

import json
import os
import sys

import numpy as np

# Ought to go in emodpy
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'local_python')))
from py_assets_common.emod_constants import EXP_C, EXP_V, EXP_NAME, NUM_SIMS, \
                                            P_FILE

# *****************************************************************************

# This script makes a json dictionary that is used by the pre-processing script
# in EMOD. Variable names defined here will be available to use in creating
# the input files.

# The pre-process script will open the json dict created by this method. For
# everything with the EXP_V key, that script will assume a list and get a value
# from that list based on the sim index. For everything with the EXP_C key, it
# will assume a single value and copy that value.


def write_param_dict():

    # Setup
    param_dict = dict()

    param_dict[EXP_NAME] = 'NetworkInfectivityDemo01'
    param_dict[NUM_SIMS] = 25
    param_dict[EXP_V] = dict()
    param_dict[EXP_C] = dict()

    # Random number consistency
    np.random.seed(4)

    # Convenience naming
    NSIMS = param_dict[NUM_SIMS]
    P_VAR = param_dict[EXP_V]
    P_CON = param_dict[EXP_C]

    # Run number (EMOD random seed)
    P_VAR['run_number'] = list(range(NSIMS))

    # Gravity model - network coefficeint
    P_VAR['net_coef'] = np.random.choice([1.0e1, 1.0e2, 1.0e3, 1.0e4],
                                         size=NSIMS).tolist()

    # Number of days for simulation
    P_CON['num_tsteps'] = 2000.0

    # Gravity model - network power
    P_CON['net_exp'] = 4.0

    # Max node export fraction
    P_CON['max_export'] = 0.1

    # Threshold for edge truncation to zero
    P_CON['min_connect'] = 1.0e-8

    # Write parameter dictionary
    with open(P_FILE, 'w') as fid01:
        json.dump(param_dict, fid01)

    return None


# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
