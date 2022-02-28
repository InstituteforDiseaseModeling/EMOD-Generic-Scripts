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

param_dict['EXP_NAME']     = 'Rubella-DRC-DemogTransition03'
param_dict['NUM_SIMS']     =   700
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']          =  list(range(NSIMS))

# Infectivity
param_dict['EXP_VARIABLE']['R0']                  = np.random.gamma(30.0, scale=0.133, size=NSIMS).tolist()

# RI rate for MR
#param_dict['EXP_VARIABLE']['RI_rate']             = np.random.choice([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], p=[0.167, 0.167, 0.166, 0.167, 0.167, 0.166], size=NSIMS).tolist()



# ***** Constants for this experiment *****

# RI rate for MR
param_dict['EXP_CONSTANT']['RI_rate']               =      0.0
param_dict['EXP_CONSTANT']['RI_rate_mult_yvals']    =  [   1.0,    1.0,     1.0,    1.0,     1.0,    1.0]   # Multiplier for the rate above; same length as xvals below
param_dict['EXP_CONSTANT']['RI_rate_mult_xvals']    =  [2020.0, 2029.99, 2030.0, 2030.99, 2040.0, 2050.0]   # Year; first value is 2020; last value is 2050;
                                                                                                            # as many other values as needed; linear interpolation;

# Initial number of agents 
param_dict['EXP_CONSTANT']['num_agents']            =  40000

# Log10 of multiplier on exogeneous case importation
param_dict['EXP_CONSTANT']['log10_import_mult']     =      0.0

# Name of data file for population pyramid (formatted as 'pop_data_{:s}.csv')
param_dict['EXP_CONSTANT']['pop_dat_file']          =  'median'

# Number of days for simulation
param_dict['EXP_CONSTANT']['num_tsteps']            =    365.0*50.0



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
