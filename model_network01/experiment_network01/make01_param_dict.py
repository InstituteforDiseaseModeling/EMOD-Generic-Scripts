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

param_dict['EXP_NAME']     = 'NetworkInfectivityDemo01'
param_dict['NUM_SIMS']     =   100
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']          =  list(range(NSIMS))

# Gravity model - network coefficeint
param_dict['EXP_VARIABLE']['network_coefficient'] =  np.random.choice([1.0e1, 1.0e2, 1.0e3, 1.0e4], p=[0.25, 0.25, 0.25, 0.25], size=NSIMS).tolist()



# ***** Constants for this experiment *****

# Number of days for simulation
param_dict['EXP_CONSTANT']['num_tsteps']          =  2000.0

# Gravity model - network power
param_dict['EXP_CONSTANT']['network_exponent']    =     4.0

# Max node export fraction
param_dict['EXP_CONSTANT']['max_export']          =     0.1


# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
