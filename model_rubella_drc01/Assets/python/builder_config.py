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

  # ***** Get variables for this simulation *****
  RUN_NUM        = gdata.var_params['run_number']
  TIME_START     = gdata.var_params['start_time']
  TIME_DELTA     = gdata.var_params['num_tsteps']

  R0             = gdata.var_params['R0']

  MAX_CLOCK      = gdata.var_params['max_clock_minutes']


  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     = TIME_START
  config.parameters.Simulation_Duration                            = TIME_DELTA

  config.parameters.Enable_Termination_On_Total_Wall_Time          =   1
  config.parameters.Wall_Time_Maximum_In_Minutes                   = MAX_CLOCK


  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'CONSTANT_DISTRIBUTION'
  config.parameters.Base_Infectivity_Constant                      =    R0/6.0

  config.parameters.Incubation_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean                =   17.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev             =    2.0

  config.parameters.Infectious_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Infectious_Period_Gaussian_Mean                =    6.0
  config.parameters.Infectious_Period_Gaussian_Std_Dev             =    2.0

  config.parameters.Enable_Disease_Mortality                       =    0

  config.parameters.Symptomatic_Infectious_Offset                  =    3.0


  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    1
  config.parameters.Enable_Immune_Decay                            =    0

  config.parameters.Post_Infection_Acquisition_Multiplier          =    0.0
  config.parameters.Post_Infection_Mortality_Multiplier            =    0.0
  config.parameters.Post_Infection_Transmission_Multiplier         =    0.0

  config.parameters.Enable_Maternal_Protection                     =    1
  config.parameters.Susceptibility_Type                            = 'BINARY'
  config.parameters.Maternal_Protection_Type                       = 'SIGMOID'
  config.parameters.Maternal_Sigmoid_HalfMaxAge                    =   90.0
  config.parameters.Maternal_Sigmoid_SteepFac                      =   30.0
  config.parameters.Maternal_Sigmoid_SusInit                       =    0.0

  config.parameters.Enable_Initial_Susceptibility_Distribution     =    1
  config.parameters.Susceptibility_Initialization_Distribution_Type= 'DISTRIBUTION_COMPLEX'


  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file

  # ***** Infectivity *****
  config.parameters.Enable_Acquisition_Heterogeneity               =    1
  config.parameters.Acquisition_Transmission_Correlation           =    0.0

  config.parameters.Enable_Infection_Rate_Overdispersion           =    1
  config.parameters.Enable_Infectivity_Reservoir                   =    1


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'
  config.parameters.Min_Node_Population_Samples                    =  20.0
  config.parameters.Base_Individual_Sample_Rate                    =   1.0
  config.parameters.Relative_Sample_Rate_Immune                    =   0.01
  config.parameters.Immune_Threshold_For_Downsampling              =   1.0e-5
  config.parameters.Immune_Downsample_Min_Age                      = 365.0


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