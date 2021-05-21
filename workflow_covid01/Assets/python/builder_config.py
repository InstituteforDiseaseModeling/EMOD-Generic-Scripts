#********************************************************************************
#
# Builds a config.json file to be used as input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

ext_py_path = os.path.join('Assets','site-packages')
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
  TIME_DELTA     = gdata.var_params['nTsteps']


  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     =    365.0*(2020-1900)+1
  config.parameters.Simulation_Duration                            = TIME_DELTA


  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'EXPONENTIAL_DISTRIBUTION'
  config.parameters.Base_Infectivity_Exponential                   =   R0/8.0

  config.parameters.Incubation_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean                =    4.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev             =    1.0

  config.parameters.Infectious_Period_Distribution                 = 'GAMMA_DISTRIBUTION'
  config.parameters.Infectious_Period_Shape                        =    2.0
  config.parameters.Infectious_Period_Scale                        =    4.0

  config.parameters.Symptomatic_Infectious_Offset                  =    2.0

  config.parameters.Enable_Disease_Mortality                       =    0


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
  config.parameters.Individual_Sampling_Type                       = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'
  config.parameters.Base_Individual_Sample_Rate                    =    1.0
  config.parameters.Relative_Sample_Rate_Immune                    =    0.1
  config.parameters.Immune_Threshold_For_Downsampling              =    1.0e-5
  config.parameters.Immune_Downsample_Min_Age                      =    0.0


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    0

  config.parameters.Age_Initialization_Distribution_Type           = 'DISTRIBUTION_OFF'
  config.parameters.Enable_Vital_Dynamics                          =    0
  config.parameters.Enable_Infection_Rate_Overdispersion           =    1
  config.parameters.Demographics_Filenames                         = gdata.demog_files

  config.parameters.Enable_Heterogeneous_Intranode_Transmission    =    1


  #  ***** Migration / Spatial parameters *****
  config.parameters.Migration_Model                                = 'FIXED_RATE_MIGRATION'
  config.parameters.Migration_Pattern                              = 'SINGLE_ROUND_TRIPS'
  config.parameters.Enable_Regional_Migration                      =    1
  config.parameters.Regional_Migration_Filename                    = 'regional_migration.bin'
  config.parameters.Regional_Migration_Roundtrip_Duration          =    0.01
  config.parameters.Regional_Migration_Roundtrip_Probability       =    1.0


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting                       =    1
  config.parameters.Enable_Property_Output                         =    1


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