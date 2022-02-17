#********************************************************************************
#
# Builds a config file for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

from emod_api.config import default_from_schema_no_validation as dfs

#********************************************************************************

def update_config_obj(config):

  # ***** Get variables for this simulation *****
  RUN_NUM        = gdata.var_params['run_number']
  TIME_DELTA     = gdata.var_params['num_tsteps']

  R0             = gdata.var_params['R0']
  R0_VAR         = gdata.var_params['R0_variance']

  CORR_ACQ_TRANS = gdata.var_params['correlation_acq_trans']


  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     =    0.0
  config.parameters.Simulation_Duration                            = TIME_DELTA

  config.parameters.Enable_Termination_On_Zero_Total_Infectivity   =    1
  config.parameters.Minimum_End_Time                               =   50.0


  # ***** Intrahost *****
  inf_prd_mean   = 8.0

  inf_ln_mean    = R0/inf_prd_mean
  inf_ln_var     = R0_VAR/inf_prd_mean/inf_prd_mean
  inf_ln_sig     = np.sqrt(np.log(inf_ln_var/inf_ln_mean/inf_ln_mean+1.0))
  inf_ln_mu      = np.log(inf_ln_mean) - 0.5*inf_ln_sig*inf_ln_sig

  config.parameters.Base_Infectivity_Distribution                  = 'LOG_NORMAL_DISTRIBUTION'
  config.parameters.Base_Infectivity_Log_Normal_Mu                 = inf_ln_mu
  config.parameters.Base_Infectivity_Log_Normal_Sigma              = inf_ln_sig

  config.parameters.Incubation_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean                =    3.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev             =    0.8

  config.parameters.Infectious_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Infectious_Period_Gaussian_Mean                = inf_prd_mean
  config.parameters.Infectious_Period_Gaussian_Std_Dev             =    0.8

  config.parameters.Enable_Disease_Mortality                       =    0

  config.parameters.Acquisition_Transmission_Correlation           = CORR_ACQ_TRANS


  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    1
  config.parameters.Enable_Immune_Decay                            =    0

  config.parameters.Post_Infection_Acquisition_Multiplier          =    0.0
  config.parameters.Post_Infection_Transmission_Multiplier         =    0.0
  config.parameters.Post_Infection_Mortality_Multiplier            =    0.0


  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'TRACK_ALL'


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    0
  config.parameters.Age_Initialization_Distribution_Type           = 'DISTRIBUTION_OFF'
  config.parameters.Enable_Vital_Dynamics                          =    0
  config.parameters.Enable_Acquisition_Heterogeneity               =    1
  config.parameters.Demographics_Filenames                         = gdata.demog_files


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting                       =    1

  config.parameters.Custom_Reports_Filename                        = gdata.reports_file


  return config

#********************************************************************************

def configBuilder():

  FILE_CONFIG  =  'config.json'
  SCHEMA_PATH  =  gdata.schema_path

  default_conf = dfs.get_default_config_from_schema(SCHEMA_PATH,as_rod=True)

  # Probably ought to be an emod-api call
  config_obj = update_config_obj(default_conf);
  config_obj.parameters.finalize()
  with open(FILE_CONFIG, 'w') as fid01:
    json.dump(config_obj, fid01, sort_keys=True, indent=4)


  return FILE_CONFIG

#********************************************************************************