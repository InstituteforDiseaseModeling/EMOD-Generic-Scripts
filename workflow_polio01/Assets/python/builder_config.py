#********************************************************************************
#
# Builds a config.json file to be used as input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

from emod_api.config        import default_from_schema_no_validation as dfs

#********************************************************************************

def maxCoeff(exp_vals):

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

# Function for setting config parameters 
def configParamFunction(config):

  # ***** Get variables for this simulation *****
  R0              = gdata.var_params['R0']
  R0_OPV          = gdata.var_params['R0_OPV']
  NOPV_R0_MULT    = gdata.var_params['R0_nOPV_mult']

  BI_STD          = gdata.var_params['ind_stddev_mult']

  ID_MEAN         = gdata.var_params['inf_duration_mean']
  ID_STD          = gdata.var_params['inf_duration_stddev']

  NI_LN_MULT      = gdata.var_params['net_inf_ln_mult']
  NI_POWER        = gdata.var_params['net_inf_power']
  NI_MAXFRAC      = gdata.var_params['net_inf_maxfrac']

  OPV_REV         = gdata.var_params['OPV_rev_prob']

  NOPV_REV        = gdata.var_params['nOPV_rev_prob']
  NOPV_BOXES      = gdata.var_params['nOPV_compartments']

  CVDPV_TRAK      = gdata.var_params['Emergence_Tracking']

  RUN_NUM         = gdata.var_params['run_number']

  TIME_START      = gdata.var_params['start_time']
  TIME_DELTA      = gdata.var_params['num_tsteps']

  AGENT_RATE      = gdata.var_params['agent_rate']

  CORR_ACQ_TRANS  = gdata.var_params['corr_acq_trans']

  MAX_CLOCK       = gdata.var_params['max_clock_minutes']

  # ***** Random number seed ****
  config.parameters.Run_Number                               = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                               = 365.0*(2016-1900)+gdata.start_off+TIME_START
  config.parameters.Simulation_Duration                      = TIME_DELTA

  config.parameters.Enable_Termination_On_Total_Wall_Time    =   1
  config.parameters.Wall_Time_Maximum_In_Minutes             = MAX_CLOCK

  # ***** Intrahost *****
  config.parameters.Base_Infectivity_Distribution            = 'GAMMA_DISTRIBUTION'
  config.parameters.Base_Infectivity_Scale                   =   R0/ID_MEAN*BI_STD*BI_STD
  config.parameters.Base_Infectivity_Shape                   =          1.0/BI_STD/BI_STD

  config.parameters.Incubation_Period_Distribution           = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean          =   3.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev       =   1.0

  config.parameters.Infectious_Period_Distribution           = 'GAMMA_DISTRIBUTION'
  config.parameters.Infectious_Period_Scale                  =       1.0/ID_MEAN*ID_STD*ID_STD
  config.parameters.Infectious_Period_Shape                  =   ID_MEAN*ID_MEAN/ID_STD/ID_STD

  config.parameters.Enable_Infection_Rate_Overdispersion     =   1
  config.parameters.Enable_Infectivity_Scaling               =   1

  config.parameters.Enable_Disease_Mortality                 =   0

  config.parameters.Acquisition_Transmission_Correlation     = CORR_ACQ_TRANS


  # ***** Network Infectivity *****
  max_k     = maxCoeff(NI_POWER)
  ni_coeff  = [np.exp(max_k[k1]+NI_LN_MULT[k1]) for k1 in range(len(max_k))]

  config.parameters.Enable_Network_Infectivity               =   1

  config.parameters.Network_Infectivity_Coefficient          =   ni_coeff
  config.parameters.Network_Infectivity_Exponent             =   NI_POWER
  config.parameters.Network_Infectivity_Max_Export_Frac      =   NI_MAXFRAC
  config.parameters.Network_Infectivity_Min_Distance         =   1


  # ***** Immunity *****
  config.parameters.Enable_Immunity                          =   1
  config.parameters.Enable_Immune_Decay                      =   0

  config.parameters.Post_Infection_Acquisition_Multiplier    =   0.0
  config.parameters.Post_Infection_Transmission_Multiplier   =   0.0
  config.parameters.Post_Infection_Mortality_Multiplier      =   0.0

  config.parameters.Enable_Initial_Susceptibility_Distribution      = 1
  config.parameters.Susceptibility_Initialization_Distribution_Type = 'DISTRIBUTION_COMPLEX'

  config.parameters.Enable_Maternal_Protection    =            1
  config.parameters.Susceptibility_Type           =  'FRACTIONAL'
  config.parameters.Maternal_Protection_Type      =     'SIGMOID'
  # BASE *= 1/(1+EXP((HALFMAXAGE-AGE_IN_DAYS)/STEEPFAC))
  config.parameters.Maternal_Sigmoid_SteepFac     =   45.0
  config.parameters.Maternal_Sigmoid_HalfMaxAge   =   90.0
  config.parameters.Maternal_Sigmoid_SusInit      =    0.2


  # ***** Interventions *****
  config.parameters.Enable_Interventions               = 1
  config.parameters.Campaign_Filename                  = gdata.camp_file


  # ***** Adapted sampling *****
  config.parameters.Individual_Sampling_Type           = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'
  config.parameters.Min_Node_Population_Samples        =  100.0
  config.parameters.Base_Individual_Sample_Rate        =    1/AGENT_RATE
  config.parameters.Relative_Sample_Rate_Immune        =    0.05
  config.parameters.Immune_Threshold_For_Downsampling  =    1.0e-5
  config.parameters.Immune_Downsample_Min_Age          =  365.0


  # ***** Multistrain *****
  log2_num_strains = 3
  num_strains      = 2**log2_num_strains

  config.parameters.Enable_Strain_Tracking                 =  1
  if(CVDPV_TRAK):
    config.parameters.Enable_Emergence_Tracking            =  1
  config.parameters.Number_of_Clades                       =  3
  config.parameters.Log2_Number_of_Genomes_per_Clade       =  log2_num_strains
  config.parameters.Enable_Strain_Dependent_Transmission   =  1
  config.parameters.Strain_Transmission_Multipliers        = (np.linspace(R0_OPV/R0, 1.0, num = num_strains)).tolist()
  config.parameters.Clade_Multiplier                       =  NOPV_R0_MULT
  config.parameters.Enable_Strain_Evolution                =  1
  config.parameters.Strain_Evolution_Rate                  =  OPV_REV
  config.parameters.nOPV_Evolution_Rate                    =  NOPV_REV
  config.parameters.nOPV_Compartments                      =  NOPV_BOXES


  # ***** Demographic parameters *****
  config.parameters.Enable_Demographics_Builtin           = 0
  config.parameters.Enable_Acquisition_Heterogeneity      = 1
  config.parameters.Demographics_Filenames                = gdata.demog_files
  config.parameters.Enable_Vital_Dynamics                 = 1
  config.parameters.Enable_Birth                          = 1
  config.parameters.Birth_Rate_Dependence                 = 'POPULATION_DEP_RATE'
  config.parameters.Enable_Aging                          = 1
  config.parameters.Enable_Natural_Mortality              = 1
  config.parameters.Death_Rate_Dependence                 = 'NONDISEASE_MORTALITY_BY_AGE_AND_GENDER'
  config.parameters.Age_Initialization_Distribution_Type  = 'DISTRIBUTION_COMPLEX'


  # ***** HINT *****
  config.parameters.Enable_Heterogeneous_Intranode_Transmission = 1


  # ***** Reporting *****
  config.parameters.Enable_Default_Reporting           = 1
  config.parameters.Enable_Demographics_Reporting      = 0
  config.parameters.Enable_Event_DB                    = 0
  config.parameters.Enable_Property_Output             = 0
  config.parameters.Enable_Spatial_Output              = 0
  config.parameters.Enable_Report_Event_Recorder       = 1
  config.parameters.Report_Event_Recorder_Events       = ["NewSevereCase", "NewClinicalCase"]

  config.parameters.Custom_Reports_Filename            = gdata.reports_file

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