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

    param_dict[EXP_NAME] = 'Measles01-Interruption01'
    param_dict[NUM_SIMS] = 720
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

    # Log10 of multiplier on exogeneous case importation
    P_VAR['log10_import_mult'] = (np.random.choice([-1.0, -0.5, 0.0],
                                  size=NSIMS)).tolist()

    # Infectivity
    P_VAR['R0'] = (10.0 + np.random.gamma(30.0, scale=0.133,
                                          size=NSIMS)).tolist()

    # RI params
    P_CON['MCV1'] = 0.70
    P_CON['MCV1_age'] = 270.0

    # Reference year for population; uses UN WPP DRC
    P_CON['ref_year'] = 2040

    # Number of years to wait before starting SIAs
    P_CON['sia_start_year'] = 1000

    # Other SIA parameters
    P_CON['sia_min_age'] = 0.75
    P_CON['sia_coverage'] = 0.80



    # RI params
    P_CON['Age_Take'] = True
    P_CON['MCV2'] = 0.0

    # Maternal protection effectiveness
    P_CON['mat_factor'] = 1.0

    # Write parameter dictionary
    with open('param_dict.json', 'w') as fid01:
        json.dump(param_dict, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
