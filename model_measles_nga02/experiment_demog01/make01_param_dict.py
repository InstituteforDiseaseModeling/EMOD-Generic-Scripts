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

param_dict['EXP_NAME']     = 'Measles-NGA-adm01-demog01'
param_dict['NUM_SIMS']     =   37*50
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']

ADM01 = ['ABIA','ADAMAWA','AKWA_IBOM','ANAMBRA','BAUCHI','BAYELSA','BENUE',
         'BORNO','CROSS_RIVER','DELTA','EBONYI','EDO','EKITI','ENUGU',
         'FCT_ABUJA','GOMBE','IMO','JIGAWA','KADUNA','KANO','KATSINA','KEBBI',
         'KOGI','KWARA','LAGOS','NASARAWA','NIGER','OGUN','ONDO','OSUN','OYO',
         'PLATEAU','RIVERS','SOKOTO','TARABA','YOBE','ZAMFARA']


# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']           =  list(range(NSIMS))

# Name of Nigerian state
# e.g., KANO, JIGAWA
param_dict['EXP_VARIABLE']['nga_state_name']       =  np.random.choice(ADM01,size=NSIMS).tolist()


# ***** Constants for this experiment *****

# Initial number of agents 
param_dict['EXP_CONSTANT']['num_agents']           =  50000

# Timing of test SIAs
param_dict['EXP_CONSTANT']['test_sias']            =     []

# Number of simulated years (start year is 2015)
param_dict['EXP_CONSTANT']['num_years']            =     30

# Infectivity
param_dict['EXP_CONSTANT']['R0']                   =     14.0

# Annual relative change in RI rates
param_dict['EXP_CONSTANT']['change_RI']            =      0.00


# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
