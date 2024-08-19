# *****************************************************************************
#
# *****************************************************************************

import json
import os
import sys

import numpy as np

# Ought to go in emodpy
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'local_python')))
sys.path.insert(0, os.path.abspath(os.path.join('..', 'Assets', 'python')))
from py_assets_common.emod_constants import EXP_C, EXP_V, EXP_NAME, NUM_SIMS, \
                                            P_FILE
from ref_dat import R0_xval, R0_ycdf, RI_2013, pop_2019, CBR_val

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

    param_dict[EXP_NAME] = 'Rubella01-DRC-Demog:EQL-RI-CU90'
    param_dict[NUM_SIMS] = 13000
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

    # Label
    P_VAR['adm01'] = np.random.choice(list(RI_2013.keys()),
                                      size=NSIMS).tolist()

    # Infectivity
    P_VAR['R0'] = [np.interp(np.random.rand(), R0_ycdf[adm01], R0_xval)
                   for adm01 in P_VAR['adm01']]

    # RI rate for MR
    P_VAR['RI_rate'] = [RI_2013[adm01] for adm01 in P_VAR['adm01']]

    # Crude birth rate target
    P_VAR['CBR_val'] = [CBR_val[adm01] for adm01 in P_VAR['adm01']]

    # Context
    P_CON['demog_set'] = 'COD'
    P_CON['num_nodes'] = 1

    # RI rate multiplier for MR
    P_CON['RI_rate_mult_yvals'] = [1.0, 1.0]
    P_CON['RI_rate_mult_xvals'] = [2025.0, 2060.0]

    # Log10 of multiplier on exogeneous case importation
    P_VAR['log10_import_mult'] = [np.log10(pop_2019[adm01]/1.0e6)
                                  for adm01 in P_VAR['adm01']]

    # Use constant vital dynamics
    P_CON['steady_state_demog'] = True

    # Use SIAs
    P_CON['add_campaigns'] = True
    P_CON['SIA_coverage'] = 0.9
    P_CON['SIA_followups'] = False

    # Initial number of agents
    P_CON['num_agents'] = 100000

    # Write parameter dictionary
    with open(P_FILE, 'w') as fid01:
        json.dump(param_dict, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
