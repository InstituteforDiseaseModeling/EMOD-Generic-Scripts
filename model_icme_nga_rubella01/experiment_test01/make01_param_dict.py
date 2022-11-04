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

param_dict['EXP_NAME']     = 'ExampleRubella01-NGA_admin02'
param_dict['NUM_SIMS']     =   250
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']          =  list(range(NSIMS))

# Gamma distribution: mean = shape*scale; variance = shape*scale^2
param_dict['EXP_VARIABLE']['R0']                  = np.random.gamma(30.0, scale=0.133, size=NSIMS).tolist()

# Use measles RI starting in 2025
param_dict['EXP_VARIABLE']['use_RI']              = np.random.choice([True,False], size=NSIMS).tolist()



# ***** Constants for this experiment *****

# Initial number of agents 
param_dict['EXP_CONSTANT']['num_agents']           = 200000

# Number of simulated years (start year is 2015)
param_dict['EXP_CONSTANT']['num_years']            =     30

# Name of Nigerian state
# e.g., KANO, JIGAWA
param_dict['EXP_CONSTANT']['nga_state_name']       =  'KANO'



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
