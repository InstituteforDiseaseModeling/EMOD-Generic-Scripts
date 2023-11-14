#********************************************************************************
#
#********************************************************************************

import json
import itertools
import numpy as np

#*******************************************************************************

# This script makes a json dictionary that is used by the pre-processing script
# in EMOD. Variable names defined here will be available to use in creating
# the input files. Please don't change the variable name for 'EXP_NAME' or
# for 'NUM_SIMS' because those are also used in scripts outside of EMOD.

# The pre-process script will open the json dict created by this method. For
# everything in the 'EXP_VARIABLE' key, that script will assume a list and
# get a value from that list based on the sim index. For everything in the 
# 'EXP_CONSTANT' key, it will assume a single value and copy that value.



# ***** Setup *****
param_dict = dict()

param_dict['EXP_NAME']     = 'Measles01-SweepAAV-Vxmodel'
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming



# ***** Specify sim-variable parameters *****


MCV1Covs = [i/10 for i in range(11)]
MCV1Ages = [90.0, 121.0, 151.0, 182.0, 212.0, 242.0, 273.0, 303.0, 334.0, 365.0, 396.0, 426.0, 457.0]
mat_durations = [90.0, 120.0, 150.0, 180.0]
NRuns = 5
myparams = [i for i in itertools.product(MCV1Covs, MCV1Ages, mat_durations, [i for i in range(NRuns)])]

param_dict['NUM_SIMS']     =  len(myparams)
NSIMS = param_dict['NUM_SIMS']
param_dict['EXP_VARIABLE']['run_number']   =  list(range(NSIMS))
# Infectivity

# RI params
param_dict['EXP_VARIABLE']['MCV1']         = [x[0] for x in myparams]
param_dict['EXP_VARIABLE']['MCV1_age']     = [x[1] for x in myparams]
param_dict['EXP_VARIABLE']['Ageind_vx_model'] = [True]*NSIMS
param_dict['EXP_VARIABLE']['mat_factor_vx']   = [1.0]*NSIMS
param_dict['EXP_VARIABLE']['mat_duration'] = [x[2] for x in myparams]

# Maternal protection effectiveness

# ***** Constants for this experiment *****
param_dict['EXP_CONSTANT']['R0']           = 16.0

# Reference year for population: [2020, 2040, 2060]
param_dict['EXP_CONSTANT']['start_year']            =   2040
param_dict['EXP_CONSTANT']['mat_factor_inf']        =   1.0

# Log10 of multiplier on exogeneous case importation
param_dict['EXP_CONSTANT']['log10_import_mult']     =      1.0

# Initial number of agents 
param_dict['EXP_CONSTANT']['num_agents']            = 500000

# RI params
param_dict['EXP_CONSTANT']['MCV2']                  =      0.0
param_dict['EXP_CONSTANT']['MCV2_age']              =      1.25*365.0



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
