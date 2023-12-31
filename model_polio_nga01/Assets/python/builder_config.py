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

  START_DAY       = gdata.start_off


  # ***** Get variables for this simulation *****
  R0              = gdata.var_params['R0']
  R0_OPV          = gdata.var_params['R0_OPV']
  NOPV_R0_MULT    = gdata.var_params['R0_nOPV_mult']

  BI_STD          = gdata.var_params['base_inf_stddev_mult']

  ID_MEAN         = gdata.var_params['inf_duration_mean']
  ID_STD          = gdata.var_params['inf_dur_stddev_mult']

  NI_LN_MULT      = gdata.var_params['net_inf_ln_mult']
  NI_POWER        = gdata.var_params['net_inf_power']
  NI_MAXFRAC      = gdata.var_params['net_inf_maxfrac']

  OPV_REV         = gdata.var_params['OPV_rev_prob']
  OPV_BOXES       = gdata.var_params['OPV_compartments']

  NOPV_REV        = gdata.var_params['nOPV_rev_prob']
  NOPV_BOXES      = gdata.var_params['nOPV_compartments']

  RUN_NUM         = gdata.var_params['run_number']

  TIME_START      = gdata.var_params['start_time']
  TIME_DELTA      = gdata.var_params['num_tsteps']

  AGENT_RATE      = gdata.var_params['agent_rate']

  CORR_ACQ_TRANS  = gdata.var_params['corr_acq_trans']

  MAX_CLOCK       = gdata.var_params['max_clock_minutes']

  LABEL_MUTES     = gdata.var_params['label_by_mutator']


  # ***** Random number seed ****
  config.parameters.Run_Number                               = RUN_NUM


  # ***** Time *****
  config.parameters.Start_Time                               = START_DAY + TIME_START
  config.parameters.Simulation_Duration                      = TIME_DELTA

  config.parameters.Enable_Termination_On_Total_Wall_Time    =   1
  config.parameters.Wall_Time_Maximum_In_Minutes             = MAX_CLOCK


  # ***** Intrahost *****
  if(BI_STD > 0.01):
    config.parameters.Base_Infectivity_Distribution          = 'GAMMA_DISTRIBUTION'
    config.parameters.Base_Infectivity_Scale                 =   R0/ID_MEAN*BI_STD*BI_STD
    config.parameters.Base_Infectivity_Shape                 =          1.0/BI_STD/BI_STD
  else:
    config.parameters.Base_Infectivity_Distribution          = 'CONSTANT_DISTRIBUTION'
    config.parameters.Base_Infectivity_Constant              =   R0/ID_MEAN

  config.parameters.Incubation_Period_Distribution           = 'GAUSSIAN_DISTRIBUTION'
  config.parameters.Incubation_Period_Gaussian_Mean          =   3.0
  config.parameters.Incubation_Period_Gaussian_Std_Dev       =   1.0

  if(ID_STD > 0.01):
    config.parameters.Infectious_Period_Distribution         = 'GAMMA_DISTRIBUTION'
    config.parameters.Infectious_Period_Scale                =      ID_MEAN*ID_STD*ID_STD
    config.parameters.Infectious_Period_Shape                =          1.0/ID_STD/ID_STD
  else:
    config.parameters.Infectious_Period_Distribution         = 'CONSTANT_DISTRIBUTION'
    config.parameters.Infectious_Period_Constant             =      ID_MEAN

  config.parameters.Enable_Infection_Rate_Overdispersion     =   1
  config.parameters.Enable_Infectivity_Scaling               =   1

  config.parameters.Enable_Disease_Mortality                 =   0

  config.parameters.Acquisition_Transmission_Correlation     = CORR_ACQ_TRANS


  # ***** Network Infectivity *****
  max_k     = max_coeff_ref(NI_POWER)
  ni_coeff  = [np.exp(max_k[k1]+NI_LN_MULT[k1]) for k1 in range(len(max_k))]

  config.parameters.Enable_Network_Infectivity               =   1

  config.parameters.Network_Infectivity_Coefficient          =   ni_coeff
  config.parameters.Network_Infectivity_Exponent             =   NI_POWER
  config.parameters.Network_Infectivity_Max_Export_Frac      =   NI_MAXFRAC
  config.parameters.Network_Infectivity_Min_Connection       =   1.0e-8
  config.parameters.Network_Infectivity_Min_Distance         =   1


  # ***** Immunity *****
  config.parameters.Enable_Immunity                          =   1
  config.parameters.Enable_Immune_Decay                      =   0

  config.parameters.Post_Infection_Acquisition_Multiplier    =   0.0
  config.parameters.Post_Infection_Transmission_Multiplier   =   0.0
  config.parameters.Post_Infection_Mortality_Multiplier      =   0.0

  config.parameters.Enable_Initial_Susceptibility_Distribution      = 1
  config.parameters.Susceptibility_Initialization_Distribution_Type = 'DISTRIBUTION_COMPLEX'

  config.parameters.Maternal_Acquire_Config.Initial_Effect          =   1.0
  config.parameters.Maternal_Acquire_Config.Durability_Map.Times    =  [   0,   50,  100,  150,  200,  250]
  config.parameters.Maternal_Acquire_Config.Durability_Map.Values   =  [0.70, 0.57, 0.36, 0.17, 0.06, 0.00]


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

  num_strains      = NOPV_BOXES + OPV_BOXES + 1
  log2_num_strains = np.ceil(np.log2(num_strains))

  config.parameters.Enable_Strain_Tracking                 =  1
  config.parameters.Enable_Genome_Dependent_Infectivity    =  1
  config.parameters.Enable_Genome_Mutation                 =  1
  config.parameters.Enable_Label_By_Mutator                =  LABEL_MUTES

  config.parameters.Number_of_Clades                       =  3
  config.parameters.Log2_Number_of_Genomes_per_Clade       =  log2_num_strains

  list_multiply              = np.ones(num_strains)
  list_multiply[:NOPV_BOXES] = NOPV_R0_MULT * R0_OPV / R0
  list_multiply[NOPV_BOXES:] = np.linspace(R0_OPV/R0, 1.0, num = OPV_BOXES + 1)
  
  config.parameters.Genome_Infectivity_Multipliers         = list_multiply.tolist()

  list_mutate                = np.zeros(num_strains)
  list_mutate[:NOPV_BOXES]   = NOPV_REV
  list_mutate[NOPV_BOXES:-1] =  OPV_REV

  config.parameters.Genome_Mutation_Rates                  = list_mutate.tolist()

  list_mlabel                = np.zeros(num_strains)
  list_mlabel[-1]            = 1

  config.parameters.Genome_Mutations_Labeled               = list_mlabel.tolist()


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
  config.parameters.Enable_Report_Event_Recorder       = 0

  config.parameters.Custom_Reports_Filename            = gdata.reports_file


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