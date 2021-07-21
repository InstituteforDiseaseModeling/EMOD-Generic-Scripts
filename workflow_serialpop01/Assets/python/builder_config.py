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
  R0             = gdata.var_params['R0']
  RUN_NUM        = gdata.var_params['run_number']
  TIME_DELTA     = gdata.var_params['num_tsteps']
  CORR_ACQ_TRANS = gdata.var_params['corr_acq_trans']
  SERIAL_TIME    = gdata.var_params['serial_time']

  # ***** Random number seed ****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     =    0.0
  config.parameters.Simulation_Duration                            = TIME_DELTA

  config.parameters.Enable_Termination_On_Zero_Total_Infectivity   =    0
  # config.parameters.Minimum_End_Time                               =   50.0

  config.parameters.Enable_Infectivity_Reservoir                   =    1

  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'EXPONENTIAL_DISTRIBUTION'
  config.parameters.Base_Infectivity_Exponential                   =   R0/8.0      # R0 divided by mean infectious
                                                                                   # duration to get daily value

  config.parameters.Incubation_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean                =   10.0        # Incubation period is misnamed; it
  config.parameters.Incubation_Period_Gaussian_Std_Dev             =    2.0        # ought to be latent period

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

  config.parameters.Enable_Maternal_Protection                     =    1
  config.parameters.Susceptibility_Type                            = 'BINARY'
  config.parameters.Maternal_Protection_Type                       = 'SIGMOID'
  config.parameters.Maternal_Sigmoid_SteepFac                      =   50.0
  config.parameters.Maternal_Sigmoid_HalfMaxAge                    =  150.0
  config.parameters.Maternal_Sigmoid_SusInit                       =    0.0

  config.parameters.Enable_Initial_Susceptibility_Distribution     =    1
  config.parameters.Susceptibility_Initialization_Distribution_Type= 'DISTRIBUTION_COMPLEX'

  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'

  config.parameters.Base_Individual_Sample_Rate                    =  1.0
  config.parameters.Relative_Sample_Rate_Immune                    =  1.0/20.0
  config.parameters.Immune_Threshold_For_Downsampling              =  1.0e-5
  config.parameters.Immune_Downsample_Min_Age                      =  365.0*5.0


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    0
  config.parameters.Age_Initialization_Distribution_Type           = 'DISTRIBUTION_OFF'
  config.parameters.Enable_Vital_Dynamics                          =    0
  config.parameters.Enable_Acquisition_Heterogeneity               =    1
  config.parameters.Demographics_Filenames                         = gdata.demog_files


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin                    =    0

  config.parameters.Enable_Vital_Dynamics                          =    1

  config.parameters.Enable_Birth                                   =    1
  config.parameters.Birth_Rate_Dependence                          = 'POPULATION_DEP_RATE'
  config.parameters.Enable_Aging                                   =    1
  config.parameters.Age_Initialization_Distribution_Type           = 'DISTRIBUTION_COMPLEX'
  config.parameters.Enable_Natural_Mortality                       =    1
  config.parameters.Death_Rate_Dependence                          = 'NONDISEASE_MORTALITY_BY_AGE_AND_GENDER'

  config.parameters.Enable_Acquisition_Heterogeneity               =    1

  config.parameters.Demographics_Filenames                         = gdata.demog_files

  # ***** Serialization options *****
  if SERIAL_TIME >= 0:
    serial_params = dict()
    serial_params['Serialized_Population_Writing_Type'] = "TIMESTEP"
    serial_params['Serialization_Time_Steps'] = [SERIAL_TIME]
    config.parameters.update(serial_params)

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