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

    param_dict[EXP_NAME] = 'Rubella01-DRC-Demog:EQL-Avg-RI-CU'
    param_dict[NUM_SIMS] = 500
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
    P_CON['adm01'] = 'DRC'

    # Infectivity
    tpop = sum([pop_2019[val] for val in pop_2019])
    wycdf = np.stack([np.array(R0_ycdf[val])*pop_2019[val] for val in pop_2019])
    wycdf = np.sum(wycdf, axis=0)/tpop
    P_VAR['R0'] = [np.interp(np.random.rand(), wycdf, R0_xval)
                   for rnum in P_VAR['run_number']]

    # RI rate for MR
    w_vec = [RI_2013[val]*pop_2019[val] for val in pop_2019]
    P_CON['RI_rate'] = np.sum(w_vec)/tpop

    # Crude birth rate target
    w_vec = [CBR_val[val]*pop_2019[val] for val in pop_2019]
    P_CON['CBR_val'] = np.sum(w_vec)/tpop

    # Context
    P_CON['demog_set'] = 'COD'
    P_CON['num_nodes'] = 1

    # RI rate multiplier for MR
    P_CON['RI_rate_mult_yvals'] = [1.0, 1.0]
    P_CON['RI_rate_mult_xvals'] = [2025.0, 2060.0]

    # Log10 of multiplier on exogeneous case importation
    w_vec = [pop_2019[val]*pop_2019[val]/1.0e6 for val in pop_2019]
    P_CON['log10_import_mult'] = np.log10(np.sum(w_vec)/tpop)

    # Use constant vital dynamics
    P_CON['steady_state_demog'] = True

    # Use SIAs
    P_CON['add_campaigns'] = True
    P_CON['SIA_coverage'] = 0.6
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
