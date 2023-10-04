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
  BASE_YEAR      = gdata.base_year
  RUN_YEARS      = gdata.run_years


  # ***** Get variables for this simulation *****
  RUN_NUM        = gdata.var_params['run_number']
  R0             = gdata.var_params['R0']
  INIT_POP       = gdata.var_params['num_agents']
  START_YEAR     = gdata.var_params['start_year']


  # ***** Random number seed *****
  config.parameters.Run_Number                                     = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                                     = 365.0*(START_YEAR-BASE_YEAR)
  config.parameters.Simulation_Duration                            = 365.0*RUN_YEARS

  config.parameters.Enable_Termination_On_Total_Wall_Time          =   1
  config.parameters.Wall_Time_Maximum_In_Minutes                   = MAX_CLOCK


  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution                  = 'GAMMA_DISTRIBUTION'
  config.parameters.Base_Infectivity_Scale                         = R0/8.0
  config.parameters.Base_Infectivity_Shape                         =    1.0

  config.parameters.Incubation_Period_Distribution                 = 'GAMMA_DISTRIBUTION'
  config.parameters.Incubation_Period_Scale                        =    1.0
  config.parameters.Incubation_Period_Shape                        =    3.5

  config.parameters.Infectious_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Infectious_Period_Gaussian_Mean                =   18.0
  config.parameters.Infectious_Period_Gaussian_Std_Dev             =    2.0

  config.parameters.Enable_Nonuniform_Shedding                     =    1.0
  config.parameters.Shedding_Distribution_Alpha                    =   10.0
  config.parameters.Shedding_Distribution_Beta                     =   10.0

  config.parameters.Symptomatic_Infectious_Offset                  =   11.0

  config.parameters.Enable_Disease_Mortality                       =    0


  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    1
  config.parameters.Enable_Immune_Decay                            =    0

  config.parameters.Post_Infection_Acquisition_Multiplier          =    0.0
  config.parameters.Post_Infection_Mortality_Multiplier            =    0.0
  config.parameters.Post_Infection_Transmission_Multiplier         =    0.0

  config.parameters.Maternal_Acquire_Config.Initial_Effect                    =   1.0
  config.parameters.Maternal_Acquire_Config.Enable_Box_Duration_Distribution  =   1
  config.parameters.Maternal_Acquire_Config.Box_Duration_Distribution         = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Maternal_Acquire_Config.Box_Duration_Gaussian_Mean        = 150.0
  config.parameters.Maternal_Acquire_Config.Box_Duration_Gaussian_Std_Dev     =  80.0

  config.parameters.Enable_Initial_Susceptibility_Distribution     =    1
  config.parameters.Susceptibility_Initialization_Distribution_Type= 'DISTRIBUTION_COMPLEX'


  # ***** Interventions *****
  config.parameters.Enable_Interventions                           =    1
  config.parameters.Campaign_Filename                              = gdata.camp_file


  # ***** Infectivity *****
  config.parameters.Enable_Acquisition_Heterogeneity               =    0
  config.parameters.Enable_Infection_Rate_Overdispersion           =    0
  config.parameters.Enable_Infectivity_Reservoir                   =    1
  config.parameters.Enable_Infectivity_Scaling                     =    1


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                       = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'
  config.parameters.Min_Node_Population_Samples                    = gdata.demog_min_pop
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
  config.parameters.Death_Rate_Dependence                          = 'NONDISEASE_MORTALITY_BY_YEAR_AND_AGE_FOR_EACH_GENDER'


  config.parameters.Demographics_Filenames                         = gdata.demog_files


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting                       =    1
  config.parameters.Enable_Demographics_Reporting                  =    1
  config.parameters.Enable_Binned_Report                           =    0

  config.parameters.Enable_Event_DB                                =   1
  config.parameters.SQL_Events                                     =   ["NewInfection"]

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