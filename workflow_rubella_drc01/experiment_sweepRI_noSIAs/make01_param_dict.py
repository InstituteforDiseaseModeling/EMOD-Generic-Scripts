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

param_dict['EXP_NAME']     = 'Rubella-DRC-DemogSteadyState01'
param_dict['NUM_SIMS']     =  250
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



# ***** Constants for this experiment *****

# Start day for simulation
param_dict['EXP_CONSTANT']['start_time']          =  365.0*(2000-1900)

# Number of days for simulation
param_dict['EXP_CONSTANT']['num_tsteps']          =  365.0*50.0

# Maximum wall-time for simulation
param_dict['EXP_CONSTANT']['max_clock_minutes']   = 180.0

# Rate of exogeneous case importation - TO DO
#param_dict['EXP_CONSTANT']['log10_import_rate']   =   -1.682

# RI rate for measles
param_dict['EXP_CONSTANT']['RI_rate']             =    0.00



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
