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

# Function for setting config parameters 
def update_config_obj(config):

  MAX_CLOCK      = gdata.max_clock
  INIT_POP       = gdata.init_pop
  BASE_YEAR      = gdata.base_year

  # ***** Get variables for this simulation *****
  RUN_NUM        = gdata.var_params['run_number']
  START_YEAR     = gdata.var_params['start_year']
  TIME_YEARS     = gdata.var_params['num_years']
  INIT_AGENT     = gdata.var_params['num_agents']


  # ***** Random number seed *****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     = 365.0*(START_YEAR-BASE_YEAR)
  config.parameters.Simulation_Duration                            = 365.0*TIME_YEARS

  config.parameters.Enable_Termination_On_Total_Wall_Time          =   1
  config.parameters.Wall_Time_Maximum_In_Minutes                   = MAX_CLOCK


  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'CONSTANT_DISTRIBUTION'
  config.parameters.Base_Infectivity_Constant                      =    0.0

  config.parameters.Incubation_Period_Distribution                 = 'CONSTANT_DISTRIBUTION'
  config.parameters.Incubation_Period_Constant                     =    0.0

  config.parameters.Infectious_Period_Distribution                 = 'CONSTANT_DISTRIBUTION'
  config.parameters.Infectious_Period_Constant                     =    0.0

  config.parameters.Enable_Disease_Mortality                       =    0

  config.parameters.Symptomatic_Infectious_Offset                  =    0.0


  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    0


  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file


  # ***** Infectivity *****
  config.parameters.Enable_Acquisition_Heterogeneity               =    0
  config.parameters.Enable_Infection_Rate_Overdispersion           =    0
  config.parameters.Enable_Infectivity_Reservoir                   =    0


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'FIXED_SAMPLING'
  config.parameters.Base_Individual_Sample_Rate                    = INIT_AGENT/INIT_POP


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    0

  config.parameters.Enable_Vital_Dynamics                          =    1

  config.parameters.Enable_Birth                                   =    1
  config.parameters.Birth_Rate_Dependence                          = 'POPULATION_DEP_RATE'
  config.parameters.Enable_Aging                                   =    1
  config.parameters.Age_Initialization_Distribution_Type           = 'DISTRIBUTION_COMPLEX'
  config.parameters.Enable_Natural_Mortality                       =    1
  config.parameters.Death_Rate_Dependence                          = 'NONDISEASE_MORTALITY_BY_YEAR_AND_AGE_FOR_EACH_GENDER'

  config.parameters.Demographics_Filenames                         = gdata.demog_files


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting                       =    1
  config.parameters.Enable_Demographics_Reporting                  =    1

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