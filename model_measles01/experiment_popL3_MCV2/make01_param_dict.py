#********************************************************************************
#
#********************************************************************************

import json

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

param_dict['EXP_NAME']     = 'Measles01-DemogL3_MCV2'
param_dict['NUM_SIMS']     =  1200
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']   =  list(range(NSIMS))

# Infectivity
param_dict['EXP_VARIABLE']['R0']           = (10.0 + np.random.gamma(30.0, scale=0.133, size=NSIMS)).tolist()

# RI params
param_dict['EXP_VARIABLE']['MCV1']         =        np.random.choice(np.arange(0.2,1.01,0.04), size=NSIMS).tolist()
param_dict['EXP_VARIABLE']['MCV1_age']     = (365.0*np.random.choice([0.50, 0.75, 1.00],       size=NSIMS)).tolist()



# ***** Constants for this experiment *****

# Reference year for population: [2020, 2040, 2060]
param_dict['EXP_CONSTANT']['start_year']            =   2020

# Number of years to wait before starting SIAs
param_dict['EXP_CONSTANT']['sia_start_year']        =   1000

# Other SIA parameters
param_dict['EXP_CONSTANT']['sia_min_age']           =      0.75
param_dict['EXP_CONSTANT']['sia_coverage']          =      0.80

# Log10 of multiplier on exogeneous case importation
param_dict['EXP_CONSTANT']['log10_import_mult']     =      1.0

# Initial number of agents 
param_dict['EXP_CONSTANT']['num_agents']            = 250000

# RI params
param_dict['EXP_CONSTANT']['MCV2']                  =      1.0
param_dict['EXP_CONSTANT']['MCV2_age']              =      1.25*365.0

# Maternal protection effectiveness
param_dict['EXP_CONSTANT']['mat_factor']            =      1.0



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
