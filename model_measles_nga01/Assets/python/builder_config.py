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

def max_coeff_ref(exp_vals):

  if(np.min(exp_vals)<0.0 or np.max(exp_vals)>8.0):
    raise Exception('Network exponent out of range.')

  x_ref = np.array([ 0.0,    0.25,   0.50,   0.75,
                     1.0,    2.0,    3.0,    4.0,
                     5.0,    6.0,    7.0,    8.0 ])
  y_ref = np.array([-2.794, -1.298,  0.155,  1.528,
                     2.797,  6.924,  9.774, 12.22,
                    14.44,  16.56,  18.65,  20.75])

  max_coeffs = np.interp(exp_vals, x_ref, y_ref).tolist()

  return max_coeffs

#********************************************************************************

def update_config_obj(config):

  MAX_CLOCK      = gdata.max_clock
  BASE_YEAR      = gdata.base_year
  TIME_STEP      = gdata.t_step_days


  # ***** Get variables for this simulation *****
  R0              = gdata.var_params['R0']

  NI_LN_MULT      = gdata.var_params['net_inf_ln_mult']
  NI_POWER        = gdata.var_params['net_inf_power']
  NI_MAXFRAC      = gdata.var_params['net_inf_maxfrac']

  RUN_NUM         = gdata.var_params['run_number']

  START_YEAR      = gdata.var_params['start_year']
  RUN_YEARS       = gdata.var_params['run_years']

  AGENT_RATE      = gdata.var_params['agent_rate']

  CORR_ACQ_TRANS  = gdata.var_params['corr_acq_trans']


  # ***** Random number seed ****
  config.parameters.Run_Number                               = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                               = 365.0*(START_YEAR-BASE_YEAR)
  config.parameters.Simulation_Duration                      = 365.0*RUN_YEARS + 1.0
  config.parameters.Simulation_Timestep                      = TIME_STEP

  config.parameters.Enable_Termination_On_Total_Wall_Time    =   1
  config.parameters.Wall_Time_Maximum_In_Minutes             = MAX_CLOCK


  # ***** Intrahost *****
  MEAN_INF_DUR = 18.0
  config.parameters.Base_Infectivity_Distribution                  = 'GAMMA_DISTRIBUTION'
  config.parameters.Base_Infectivity_Scale                         =  R0/MEAN_INF_DUR
  config.parameters.Base_Infectivity_Shape                         =    1.0

  config.parameters.Incubation_Period_Distribution                 = 'GAMMA_DISTRIBUTION'
  config.parameters.Incubation_Period_Scale                        =    1.0
  config.parameters.Incubation_Period_Shape                        =    3.5

  config.parameters.Infectious_Period_Distribution                 = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Infectious_Period_Gaussian_Mean                =   MEAN_INF_DUR
  config.parameters.Infectious_Period_Gaussian_Std_Dev             =    2.0

  config.parameters.Enable_Nonuniform_Shedding                     =    1.0
  config.parameters.Shedding_Distribution_Alpha                    =   10.0
  config.parameters.Shedding_Distribution_Beta                     =   10.0

  config.parameters.Symptomatic_Infectious_Offset                  =   11.0

  config.parameters.Enable_Disease_Mortality                       =    0

  config.parameters.Acquisition_Transmission_Correlation           = CORR_ACQ_TRANS


  # ***** Immunity *****
  config.parameters.Enable_Immunity                                =    1
  config.parameters.Enable_Immune_Decay                            =    0

  config.parameters.Post_Infection_Acquisition_Multiplier          =    0.0
  config.parameters.Post_Infection_Mortality_Multiplier            =    0.0
  config.parameters.Post_Infection_Transmission_Multiplier         =    0.0

  config.parameters.Maternal_Acquire_Config.Initial_Effect                    =   1.0
  config.parameters.Maternal_Acquire_Config.Enable_Box_Duration_Distribution  =   1
  config.parameters.Maternal_Acquire_Config.Box_Duration_Distribution         = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Maternal_Acquire_Config.Box_Duration_Gaussian_Mean        = 120.0
  config.parameters.Maternal_Acquire_Config.Box_Duration_Gaussian_Std_Dev     =  67.0

  config.parameters.Enable_Initial_Susceptibility_Distribution     =    1
  config.parameters.Susceptibility_Initialization_Distribution_Type= 'DISTRIBUTION_COMPLEX'


  # ***** Interventions *****
  config.parameters.Enable_Interventions                     =   1
  config.parameters.Campaign_Filename                        = gdata.camp_file


  # ***** Network Infectivity *****
  ni_coeff  = np.exp(max_coeff_ref(NI_POWER) + NI_LN_MULT)

  config.parameters.Enable_Network_Infectivity               =   1

  config.parameters.Network_Infectivity_Coefficient          =   [ni_coeff]
  config.parameters.Network_Infectivity_Exponent             =   [NI_POWER]
  config.parameters.Network_Infectivity_Max_Export_Frac      =   NI_MAXFRAC
  config.parameters.Network_Infectivity_Min_Distance         =   1

  config.parameters.Enable_Infectivity_Reservoir             =   1


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type                 = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'
  config.parameters.Min_Node_Population_Samples              = gdata.demog_min_pop
  config.parameters.Base_Individual_Sample_Rate              =   1.0/AGENT_RATE
  config.parameters.Relative_Sample_Rate_Immune              =   0.01
  config.parameters.Immune_Threshold_For_Downsampling        =   1.0e-5
  config.parameters.Immune_Downsample_Min_Age                = 365.0


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin              =   0

  config.parameters.Enable_Vital_Dynamics                    =   1
  config.parameters.Enable_Birth                             =   1
  config.parameters.Birth_Rate_Dependence                    = 'POPULATION_DEP_RATE'
  config.parameters.Enable_Aging                             =   1
  config.parameters.Age_Initialization_Distribution_Type     = 'DISTRIBUTION_COMPLEX'
  config.parameters.Enable_Natural_Mortality                 =   1
  config.parameters.Death_Rate_Dependence                    = 'NONDISEASE_MORTALITY_BY_AGE_AND_GENDER'

  config.parameters.Enable_Acquisition_Heterogeneity         =   1

  config.parameters.Demographics_Filenames                   = gdata.demog_files


  # ***** Reporting *****
  START_LOG_TIME       = 365.0*(START_YEAR-BASE_YEAR+3.0)
  gdata.start_log_time = START_LOG_TIME

  config.parameters.Enable_Default_Reporting                 =   1
  config.parameters.Enable_Demographics_Reporting            =   1
  config.parameters.Enable_Event_DB                          =   1
  config.parameters.SQL_Start_Time                           = START_LOG_TIME
  config.parameters.SQL_Events                               =   ["NewlySymptomatic"]

  config.parameters.Enable_Spatial_Output                    =   0

  config.parameters.Custom_Reports_Filename                  = gdata.reports_file


  return config

#********************************************************************************

def configBuilder():

  FILE_CONFIG  =  'config.json'
  SCHEMA_PATH  =  gdata.schema_path

  default_conf = dfs.get_default_config_from_schema(SCHEMA_PATH,as_rod=True)

  # Probably ought to be an emod-api call
  config_obj = update_config_obj(default_conf);
  config_obj.parameters.finalize()

  # Need to get these listed in the schema
  #config_obj.parameters['logLevel_Memory']                   = 'DEBUG'
  config_obj.parameters['logLevel_StandardEventCoordinator'] = 'WARNING'
  config_obj.parameters['logLevel_SimulationEventContext']   = 'WARNING'

  with open(FILE_CONFIG, 'w') as fid01:
    json.dump(config_obj, fid01, sort_keys=True, indent=4)


  return FILE_CONFIG

#********************************************************************************