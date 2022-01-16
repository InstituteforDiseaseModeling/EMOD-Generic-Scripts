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

param_dict['EXP_NAME']     = 'MEAS-GHA-Calib02'
param_dict['NUM_SIMS']     =   1050
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['NUM_SIMS']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']       =     list(range(NSIMS))

# R0 seasonality
param_dict['EXP_VARIABLE']['R0_peak_magnitude']    = np.random.uniform(low=  1.0, high=   1.5, size=NSIMS).tolist()
param_dict['EXP_VARIABLE']['R0_peak_day']          = np.random.uniform(low= 20.0, high= 180.0, size=NSIMS).tolist()

# Importation rate per-100k per-day
param_dict['EXP_VARIABLE']['log10_import_rate']    = np.random.uniform(low= -1.0, high=   2.0, size=NSIMS).tolist()

# Individual level risk variance (risk of acquisition multiplier; mean = 1.0; log-normal distribution)
param_dict['EXP_VARIABLE']['ind_variance_risk']    = np.random.uniform(low=  0.1, high=   1.0, size=NSIMS).tolist()


param_dict['EXP_VARIABLE']['net_inf_ln_mult']      = np.random.uniform(low= -3.0, high=   0.0, size=NSIMS).tolist()


# ***** Constants for this experiment *****

# Time stamp for sim start (Jan 1, 2010 = 40150)
param_dict['EXP_CONSTANT']['start_time']           =   40150-2*365

# Number of days to run simulation
param_dict['EXP_CONSTANT']['num_tsteps']           =   365.0*12.0

# Coverage of SIAs in WHO calendar
param_dict['EXP_CONSTANT']['SIA_cover_GHA-2006']   =     0.90

# Coverage of SIAs in WHO calendar
param_dict['EXP_CONSTANT']['SIA_cover_GHA-2010']   =     0.85
param_dict['EXP_CONSTANT']['SIA_cover_GHA-2013']   =     0.70
param_dict['EXP_CONSTANT']['SIA_cover_GHA-2018']   =     0.62

# R0 value
param_dict['EXP_CONSTANT']['R0']                   =    14.0

# Parameters for gravity model for network connections
param_dict['EXP_CONSTANT']['net_inf_power']        =     2.0

param_dict['EXP_CONSTANT']['net_inf_maxfrac']      =     0.1

# Correlation between acqusition and transmission heterogeneity
param_dict['EXP_CONSTANT']['corr_acq_trans']       =     0.9

# Base agent weight; less than 10 may have memory issues
param_dict['EXP_CONSTANT']['agent_rate']           =    25.0

# Abort sim if running for more than specified time in minutes
param_dict['EXP_CONSTANT']['max_clock_minutes']    =   120.0

# Node level overdispersion; 0.0 = Poisson
param_dict['EXP_CONSTANT']['proc_overdispersion']  =     0.2



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
