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

    param_dict[EXP_NAME] = 'DemogExample-UK01-Sweep'
    param_dict[NUM_SIMS] = 600
    param_dict[EXP_V] = dict()
    param_dict[EXP_C] = dict()

    # Random number consistency
    np.random.seed(4)

    # Convenience naming
    NSIMS = param_dict[NUM_SIMS]
    P_VAR = param_dict[EXP_V]
    P_CON = param_dict[EXP_C]

    # Coordinated levels
    p_levels = [[False, True, True, True],
                [False, False, True, True],
                [0.0, 0.0, 0.0, 0.28]]
    rand_lev = np.random.randint(0, len(p_levels[0]), size=NSIMS).tolist()

    # Run number (EMOD random seed)
    P_VAR['run_number'] = list(range(NSIMS))

    # Use historical data for crude birth rate (constant value otherwise)
    P_VAR['variable_birthrate'] = [p_levels[0][val] for val in rand_lev]

    # Use historical data for age initialization (equilibrium otherwise)
    P_VAR['modified_age_init'] = [p_levels[1][val] for val in rand_lev]

    # Log of age-independent multiplier for mortality rates
    P_VAR['log_mort_mult03'] = [p_levels[2][val] for val in rand_lev]

    # Log of age-dependent multiplier for mortality rates
    P_CON['log_mort_mult01'] = 0.0
    P_CON['log_mort_mult02'] = 0.0

    # Number of agents for simulation
    P_CON['num_agents'] = 50000

    # Write parameter dictionary
    with open('param_dict.json', 'w') as fid01:
        json.dump(param_dict, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
