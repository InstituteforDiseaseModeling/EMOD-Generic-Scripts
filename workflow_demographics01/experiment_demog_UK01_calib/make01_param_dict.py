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

param_dict['EXP_NAME']     = 'DemogExample-UK01-Calibration'
param_dict['NUM_SIMS']     =   720
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']          =  list(range(NSIMS))

# Log of age-independent multiplier for mortality rates
param_dict['EXP_VARIABLE']['log_mortality_mult']  =  np.random.uniform(low=-2.0, high=2.0, size=NSIMS).tolist()



# ***** Constants for this experiment *****

# Number of days for simulation
param_dict['EXP_CONSTANT']['num_tsteps']          =  365.0*30

# Use historical data for crude birth rate (constant value otherwise)
param_dict['EXP_CONSTANT']['variable_birthrate']  =  True

# Use historical data for age initialization (equilibrium otherwise)
param_dict['EXP_CONSTANT']['modified_age_init']   =  True


# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
