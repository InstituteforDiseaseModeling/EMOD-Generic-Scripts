#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import json

import numpy as np

#*******************************************************************************

# This script makes a json dictionary that is used by the pre-processing script
# in EMOD. Variable names defined here will be available to use in creating
# the input files. Please don't change the variable name for 'exp_name' or
# for 'num_sims' because those are also used in scripts outside of EMOD.

# The pre-process script will open the json dict created by this method. For
# everything in the 'EXP_VARIABLE' key, that script will assume a list and
# get a value from that list based on the sim index. For everything in the 
# 'EXP_CONSTANT' key, it will assume a single value and copy that value.



# ***** Setup *****
param_dict = dict()

param_dict['exp_name']     = 'covariance01'
param_dict['num_sims']     =  1000
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['num_sims']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']             =     list(range(NSIMS))

# R0 values for tranmssion
param_dict['EXP_VARIABLE']['R0']                     =     np.random.uniform(low= 0.25,high= 1.75, size=NSIMS).tolist()

# Individual level acquisition variance; (mean = 1.0; log-normal distribution)
param_dict['EXP_VARIABLE']['indiv_variance_acq']     =     np.random.choice([0.0, 0.5, 1.0], p=[0.25, 0.75, 0.00], size=NSIMS).tolist()

# Acquision-transmission correlation;
param_dict['EXP_VARIABLE']['correlation_acq_trans']  =     np.random.choice([0.0, 0.5, 1.0], p=[0.50, 0.25, 0.25], size=NSIMS).tolist()



# ***** Constants for this experiment *****

# Number of days for simulation;
param_dict['EXP_CONSTANT']['num_tsteps']           =  1000.0



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
