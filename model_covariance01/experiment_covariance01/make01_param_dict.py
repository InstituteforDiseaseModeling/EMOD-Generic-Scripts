# *****************************************************************************
#
# *****************************************************************************

import json
import os
import sys

import numpy as np

# Ought to go in emodpy
LOCAL_PATH = os.path.abspath(os.path.join('..', '..', 'local_python'))
sys.path.insert(0, LOCAL_PATH)
from py_assets_common.emod_constants import EXP_C, EXP_V, EXP_NAME, NUM_SIMS

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

    param_dict[EXP_NAME] = 'CovarainceDemo01'
    param_dict[NUM_SIMS] = 1500
    param_dict[EXP_V] = dict()
    param_dict[EXP_C] = dict()

    # Random number consistency
    np.random.seed(4)

    # Convenience naming
    NSIMS = param_dict[NUM_SIMS]
    P_VAR = param_dict[EXP_V]
    P_CON = param_dict[EXP_C]

    # Coordinated levels
    p_levels = [[0.5, 0.5, 0.388, 0.137],
                [0.0, 0.5, 0.500, 0.500],
                [0.0, 0.0, 0.400, 0.800]]
    rand_lev = np.random.randint(0, len(p_levels[0]), size=NSIMS).tolist()

    # Run number (EMOD random seed)
    P_VAR['run_number'] = list(range(NSIMS))

    # R0 values for tranmssion
    P_VAR['R0'] = np.random.uniform(low=0.50, high=1.75, size=NSIMS).tolist()

    # R0 variance; (log-normal distribution)
    P_VAR['R0_variance'] = [p_levels[0][val] for val in rand_lev]

    # Individual acquisition variance; (mean=1.0; log-normal distribution)
    P_VAR['indiv_variance_acq'] = [p_levels[1][val] for val in rand_lev]

    # Acquision-transmission correlation
    P_VAR['correlation_acq_trans'] = [p_levels[2][val] for val in rand_lev]

    # Number of days for simulation
    P_CON['num_tsteps'] = 1000.0

    # Write parameter dictionary
    with open('param_dict.json', 'w') as fid01:
        json.dump(param_dict, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
