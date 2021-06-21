#********************************************************************************
#
# Builds a config file for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

from emod_api.config import default_from_schema_no_validation as dfs

#********************************************************************************

# Function for setting config parameters 
def configParamFunction(config):

  # ***** Get variables for this simulation *****
  RUN_NUM        = gdata.var_params['run_number']
  TIME_DELTA     = gdata.var_params['num_tsteps']


  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     =    0.0
  config.parameters.Simulation_Duration                            = TIME_DELTA



  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'CONSTANT_DISTRIBUTION'
  config.parameters.Base_Infectivity_Constant                      =    0.0

  config.parameters.Incubation_Period_Distribution                 = 'CONSTANT_DISTRIBUTION'
  config.parameters.Incubation_Period_Constant                     =    0.0

  config.parameters.Infectious_Period_Distribution                 = 'CONSTANT_DISTRIBUTION'
  config.parameters.Infectious_Period_Constant                     =    0.0

  config.parameters.Enable_Disease_Mortality                       =    0

  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    0


  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'TRACK_ALL'


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    0

  config.parameters.Enable_Vital_Dynamics                          =    1

  config.parameters.Enable_Birth                                   =    1
  config.parameters.Birth_Rate_Dependence                          = 'POPULATION_DEP_RATE'
  config.parameters.Enable_Aging                                   =    1
  config.parameters.Age_Initialization_Distribution_Type           = 'DISTRIBUTION_COMPLEX'
  config.parameters.Enable_Natural_Mortality                       =    1
  config.parameters.Death_Rate_Dependence                          = 'NONDISEASE_MORTALITY_BY_AGE_AND_GENDER'


  config.parameters.Demographics_Filenames                         = gdata.demog_files


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting                       =    1
  config.parameters.Enable_Demographics_Reporting                  =    1

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