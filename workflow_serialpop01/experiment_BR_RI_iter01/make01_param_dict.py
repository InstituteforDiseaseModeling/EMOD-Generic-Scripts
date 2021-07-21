'''
Look at impact of forcing needed to remove exinction
'''
#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import json
import itertools
import numpy as np
from collections import OrderedDict

#*******************************************************************************

# This script makes a json dictionary that is used by the pre-processing script
# in EMOD. Variable names defined here will be available to use in creating
# the input files. Please don't change the variable name for 'exp_name' or
# for 'num_sims' because those are also used outside of EMOD.

# The pre-process script will open the json dict created by this method. For
# everything under the 'EXP_VARIABLE' heading, that script will assume a list and
# get a value from that list based on the sim index. For everything under the 
# 'EXP_CONSTANT' heading, it will assume a single value and copy that value.

# Random number consistency
np.random.seed(2)

# number of samples for "RANGE" variables
n_rand = 4

# set range and value of sweep
sweep_dict = OrderedDict()
sweep_dict['INF_FORCE_SIN_AMP_RANGE'] = [0.0, 0.50]
sweep_dict['BIRTH_RATE_RANGE'] = [15, 30]
sweep_dict['RANGE_IDX_VALS'] = np.arange(n_rand).tolist()

# pre-construct the range values
range_vals = {}
for k,v in sweep_dict.items():
    if k.endswith('RANGE'):
        range_vals.update({k: (v[0] + np.random.rand(n_rand)*np.ptp(v)).tolist()})

# This function generates the sweep parameters for its index.  We would like the range samples to be the same
def generate_sim_params(index, sweep_dict):
    val_dims = OrderedDict({k: len(v) for k,v in sweep_dict.items() if (k.split('_')[-1] == 'VALS')})
    val_idxs = OrderedDict(zip(list(val_dims.keys()), np.unravel_index(index % np.prod(list(val_dims.values())), list(val_dims.values()))))

    # initialize sim_param
    sim_param = {}
    # Run through VALS
    for k,v in sweep_dict.items():
        if k.endswith('VALS'):
            sim_param[k] = v[val_idxs[k]]
    # Run through RANGE
    for k,v in sweep_dict.items():
        if k.endswith('RANGE'):
            sim_param[k] = range_vals[k][sim_param['RANGE_IDX_VALS']]
    return sim_param

val_dims = [len(v) for k,v in sweep_dict.items() if k.endswith('VALS')]
num_sims = int(np.prod(val_dims))

# Generate the simulation parameters
sim_params = {k:[] for k in sweep_dict.keys()}
for idx in range(num_sims):
    for k,v in generate_sim_params(idx, sweep_dict).items():
        sim_params[k].append(v)

# ***** Setup *****
param_dict = dict()

param_dict['exp_name']     = 'serialpop01'
param_dict['num_sims']     =  num_sims
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Convenience naming
NSIMS = param_dict['num_sims']

# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']           =    sim_params['RANGE_IDX_VALS']
param_dict['EXP_VARIABLE']['inf_force_sin_amp']    =  sim_params['INF_FORCE_SIN_AMP_RANGE']
param_dict['EXP_VARIABLE']['birth_rate'] = sim_params['BIRTH_RATE_RANGE']

# ***** Constants for this experiment *****

# Length of burn-in
param_dict['EXP_CONSTANT']['inf_res_end'] = 5

# Infectivity Reservoir size for initial seeding
param_dict['EXP_CONSTANT']['inf_res_size']           = 1.0

# Constant seasonality params
param_dict['EXP_CONSTANT']['inf_force_sin_phase'] = 0.0

# Acquision-transmission correlation;
param_dict['EXP_CONSTANT']['corr_acq_trans']       = 0.5

# Number of days for simulation;
param_dict['EXP_CONSTANT']['num_tsteps']           =  365.0 * 15

# R0 values for tranmssion
param_dict['EXP_CONSTANT']['R0']                   =   14.0

# Individual level acquisition variance; (mean = 1.0; log-normal distribution)
param_dict['EXP_CONSTANT']['ind_variance_risk']    =    0.25

# Time for SIAs to start
param_dict['EXP_CONSTANT']['sia_start']    =    7*365.0

# SIA Coverage
param_dict['EXP_CONSTANT']['sia_coverage']    =   0.90

# Time to serialize file (<0 do not serialize)
param_dict['EXP_CONSTANT']['serial_time']    =    7*365.0

# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
