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

param_dict['exp_name']     = 'cVDPV2_NGA_100km_noSIAs'
param_dict['num_sims']     = 350
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
NSIMS = param_dict['num_sims']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']       =     list(range(NSIMS))



# ***** Constants for this experiment *****

# Parameters for gravity model for network connections
param_dict['EXP_CONSTANT']['net_inf_power']        =  [ 2.0  ]
param_dict['EXP_CONSTANT']['net_inf_ln_mult']      =  [-2.424]

# Number of days to run simulation
param_dict['EXP_CONSTANT']['num_tsteps']           =   365.0*2.0

# Days after May 1, 2016 (Sabin2 cessation) to start simulation
param_dict['EXP_CONSTANT']['start_time']           =   365.0*0.0

# Abort sim if running for more than specified time in minutes
param_dict['EXP_CONSTANT']['max_clock_minutes']    =   120.0

# Node level overdispersion; 0.0 = Poisson
param_dict['EXP_CONSTANT']['proc_overdispersion']  =     0.8

# Correlation between acqusition and transmission heterogeneity
param_dict['EXP_CONSTANT']['corr_acq_trans']       =     1.0

# Network maximum export fraction
param_dict['EXP_CONSTANT']['net_inf_maxfrac']      =     0.1

# Base agent weight; less than 10 may have memory issues
param_dict['EXP_CONSTANT']['agent_rate']           =    25.0

# Paramaters of beta distribution for HINT group fraction of infectable agents
# Values less than 0.01 are re-drawn from the distribution (zero group muzt be <99%)
param_dict['EXP_CONSTANT']['use_zero_group']                       = False
param_dict['EXP_CONSTANT']['nonzero_group_beta_dist_param_alpha']  =  1.0
param_dict['EXP_CONSTANT']['nonzero_group_beta_dist_param_beta']   =  1.0
param_dict['EXP_CONSTANT']['nonzero_group_scale']                  =  1.0

# R0 values for cVDPV and Sabin; linear interpolation; requires R0 > R0_OPV
param_dict['EXP_CONSTANT']['R0']                   =    10.0
param_dict['EXP_CONSTANT']['R0_OPV']               =     2.5

# Transmissibility of nOPV with respect to Sabin
param_dict['EXP_CONSTANT']['R0_nOPV_mult']         =     0.5

# Mean duration of infectious period
param_dict['EXP_CONSTANT']['inf_duration_mean']    =    24.0

# Dispersion for base infectivity and infectious duration (multiplier; 1.0 = exponential)
param_dict['EXP_CONSTANT']['base_inf_stddev_mult'] =     1.0
param_dict['EXP_CONSTANT']['inf_dur_stddev_mult']  =     0.4708333

# Subdivide LGAs into 100km^2 regions
param_dict['EXP_CONSTANT']['use_10k_res']          =    True

# Immunity mapper with 50% coverage SIAs (80% coverage otherwise)
param_dict['EXP_CONSTANT']['use_50pct_init']       =    True

# Apply the historic SIA calendar; coverage for SIAs in calendar
# SIAs may not occur with large value of 'burnin_time'
param_dict['EXP_CONSTANT']['sia_calendar']         =    False
param_dict['EXP_CONSTANT']['sia_calendar_nopv']    =    False
param_dict['EXP_CONSTANT']['sia_coverage']         =     0.5

# Optional timestamp cutoff for SIA calendar; absolute time
param_dict['EXP_CONSTANT']['sia_cutoff']           = 42825.0

# Direct introduction of cVDPV2
# day_offset -> days after sim start, NOT ABSOLUTE TIME
param_dict['EXP_CONSTANT']['sia_other']            =     True
param_dict['EXP_CONSTANT']['sia_sets']             =  [ {"targ_list":   ["AFRO:NIGERIA:KANO:KANO_MUNICIPAL"] ,
                                                         "day_offset":                     1.0*365.0 +   5.0 ,
                                                         "num_cases":                                  100   ,
                                                         "agent_wght":                                   1.0 } ]

# Node level R0 variance (infectivity multiplier; mean = 1.0; log-normal distribution)
param_dict['EXP_CONSTANT']['node_variance_R0']     =     0.0

# Individual level risk variance (risk of acquisition multiplier; mean = 1.0; log-normal distribution)
param_dict['EXP_CONSTANT']['ind_variance_risk']    =     3.0

# Rate of mutation / infectivity scaling for nOPV; transition to Sabin after nOPV
param_dict['EXP_CONSTANT']['nOPV_rev_prob']        =     0.0
param_dict['EXP_CONSTANT']['nOPV_compartments']    =     2

# Rate of mutation / infectivity scaling for Sabin; transition to cVDPV after Sabin
param_dict['EXP_CONSTANT']['OPV_rev_prob']         =     0.0
param_dict['EXP_CONSTANT']['OPV_compartments']     =     7

# Uniquely labels infections (with the agent ID) on mutation; CAN SLOW DOWN SIMS
param_dict['EXP_CONSTANT']['label_by_mutator']     =    False

# Timestamps for conducting serosurveys; absolute time; survey <10yrs, 1yr age bins
param_dict['EXP_CONSTANT']['serosurvey_timestamps']=     [ 42825.0 ]



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
