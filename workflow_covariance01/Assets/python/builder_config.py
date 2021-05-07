#********************************************************************************
#
# Builds a config file for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

ext_py_path = os.path.join('Assets','site_packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy as np

from emod_api.config import default_from_schema_no_validation as dfs

#********************************************************************************

# Function for setting config parameters 
def configParamFunction(config):

  # ***** Get variables for this simulation *****
  R0             = gdata.var_params['R0']
  RUN_NUM        = gdata.var_params['run_number']
  TIME_DELTA     = gdata.var_params['num_tsteps']
  CORR_ACQ_TRANS = gdata.var_params['correlation_acq_trans']


  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     =    0.0
  config.parameters.Simulation_Duration                            = TIME_DELTA

  config.parameters.Enable_Termination_On_Zero_Total_Infectivity   =    1
  config.parameters.Minimum_End_Time                               =   50.0


  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'EXPONENTIAL_DISTRIBUTION'
  config.parameters.Base_Infectivity_Exponential                   =   R0/8.0

  config.parameters.Incubation_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean                =   10.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev             =    2.0

  config.parameters.Infectious_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Infectious_Period_Gaussian_Mean                =    8.0
  config.parameters.Infectious_Period_Gaussian_Std_Dev             =    2.0

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

  FILE_CONFIG  =  'config_useful.json'
  FILE_DEFAULT =  'default_config.json'
  SCHEMA_PATH  =  gdata.schema_path


  dfs.write_default_from_schema(SCHEMA_PATH)
  dfs.write_config_from_default_and_params(FILE_DEFAULT, configParamFunction, FILE_CONFIG)

  return FILE_CONFIG

#********************************************************************************