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

    param_dict[EXP_NAME] = 'cVDPV2-NGA-100km-SIAs'
    param_dict[NUM_SIMS] = 350
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

    # Parameters for gravity model for network connections
    P_CON['net_inf_power'] = [2.0]
    P_CON['net_inf_ln_mult'] = [-2.424]

    # Days after May 1, 2016 (Sabin2 cessation) to start simulation
    P_CON['start_time'] = 365.0*0.0

    # Node level overdispersion; 0.0 = Poisson
    P_CON['proc_overdispersion'] = 0.8

    # Correlation between acqusition and transmission heterogeneity
    P_CON['corr_acq_trans'] = 0.9

    # Base agent weight; less than 10 may have memory issues
    P_CON['agent_rate'] = 25.0

    # R0 values for cVDPV and Sabin; linear interpolation;
    # requires R0 > R0_OPV
    P_CON['R0'] = 16.0
    P_CON['R0_OPV'] = 4.0

    # Transmissibility of nOPV with respect to Sabin
    P_CON['R0_nOPV_mult'] = 0.5

    # Mean duration of infectious period
    P_CON['inf_duration_mean'] = 24.0

    # Dispersion for base infectivity and infectious duration
    # (multiplier; 1.0 = exponential)
    P_CON['base_inf_stddev_mult'] = 1.0
    P_CON['inf_dur_stddev_mult'] = 0.4708333

    # Subdivide LGAs into 100km^2 regions
    P_CON['use_10k_res'] = True

    # Immunity mapper with 50% coverage SIAs (80% coverage otherwise)
    P_CON['use_50pct_init'] = True

    # Apply the historic SIA calendar; events prior to sim start ignored
    P_CON['sia_calendar'] = True
    P_CON['sia_coverage'] = 0.5

    # Cutoff time for SIA calendar
    P_CON['sia_cutoff'] = 42825.0

    # Direct introduction of cVDPV2
    # day_offset -> days after sim start, NOT ABSOLUTE TIME
    P_CON['sia_sets'] = [{"targ_list": ["AFRO:NIGERIA:KANO:KANO_MUNICIPAL"],
                          "day_offset": 1.0*365.0 + 5.0,
                          "num_cases": 100}]

    # Node level R0 variance (infectivity multiplier;
    # mean = 1.0; log-normal distribution)
    P_CON['node_variance_R0'] = 0.0

    # Individual level risk variance (risk of acquisition multiplier;
    # mean = 1.0; log-normal distribution)
    P_CON['ind_variance_risk'] = 3.0

    # Write parameter dictionary
    with open(P_FILE, 'w') as fid01:
        json.dump(param_dict, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    write_param_dict()

# *****************************************************************************
