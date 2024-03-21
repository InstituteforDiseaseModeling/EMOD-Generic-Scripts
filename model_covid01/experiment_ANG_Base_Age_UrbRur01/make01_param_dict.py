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

    param_dict[EXP_NAME] = 'SARS-CoV-2-ANG-UrbRur01'
    param_dict[NUM_SIMS] = 700
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

    # Population structure
    node_opts = [100, 150, 200, 250]
    P_VAR['num_nodes'] = (np.random.choice(node_opts, NSIMS)).tolist()

    # Simulation duration
    P_CON['nTsteps'] = 730

    # Setting (defines age structure)
    P_CON['ctext_val'] = 'AFRO:ANG'

    # Total population
    P_CON['totpop'] = 1e6

    # Migration intensity
    P_CON['migration_coeff'] = 1e-3
    P_CON['pop_power'] = 1.00

    # Fraction of population in rural nodes
    P_CON['frac_rural'] = 0.33

    # Acquire and transmit multiplier for childern
    P_CON['age_effect_a'] = 0.70
    P_CON['age_effect_t'] = 0.20

    # Self-isolation on symptoms behavior
    P_CON['self_isolate_on_symp_frac'] = 0.1
    P_CON['self_isolate_effectiveness'] = 0.8

    # Infectivity
    P_CON['R0'] = 3.60

    # Start day for importations
    P_CON['importations_start_day'] = 60
    P_CON['importations_daily_rate'] = 1.2
    P_CON['importations_duration'] = 365

    # Effectiveness of PPE for health workers
    P_CON['HCW_PPE'] = 0.95

    # Contact pattern revisions
    P_CON['trans_mat01'] = [1.00, 0.00, 0.50, 0.75]
    P_CON['start_mat01'] = 75

    # Write parameter dictionary
    with open('param_dict.json', 'w') as fid01:
        json.dump(param_dict, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
