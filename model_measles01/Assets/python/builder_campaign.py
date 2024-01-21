#********************************************************************************
#
# Builds a campaign for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

import emod_api.campaign     as     camp_module

from emod_api                 import schema_to_class as s2c
from emod_api.interventions   import utils

VEC_AGE  = [0/12*365, 3/12*365, 5/12*365, 7/12*365, 9/12*365]
VEC_TAKE = [     0.0,      0.0,     0.65,     0.92,      1.0]

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  CAMP_FILENAME =  'campaign.json'

  ALL_NODES     = gdata.demog_object.node_ids
  BASE_YEAR     = gdata.base_year
  BR_MULT_X     = gdata.brate_mult_x
  BR_MULT_Y     = gdata.brate_mult_y
  RUN_YEARS     = gdata.run_years


  # ***** Get variables for this simulation *****
  MCV1_RATE     = gdata.var_params['MCV1']
  MCV2_FRAC     = gdata.var_params['MCV2']
  MCV1_AGE      = gdata.var_params['MCV1_age']
  MCV2_AGE      = gdata.var_params['MCV2_age']
  START_YEAR    = gdata.var_params['start_year']
  SIA_START     = gdata.var_params['sia_start_year']
  SIA_MIN_AGE   = gdata.var_params['sia_min_age']
  SIA_COVERAGE  = gdata.var_params['sia_coverage']
  MAT_FACTOR    = gdata.var_params['mat_factor']


  # ***** Events *****

  # Add MCV
  start_day = 365.0*(START_YEAR-BASE_YEAR)
  pdict     = {'startday':        start_day ,
               'nodes':           ALL_NODES ,
               'ri_rate':         MCV1_RATE ,
               'frac_MCV2':       MCV2_FRAC ,
               'age_MCV1':         MCV1_AGE ,
               'age_MCV2':         MCV2_AGE ,
               'take_fac':       MAT_FACTOR }

  camp_module.add(IV_MCV(pdict))


  # Add time varying birth rate
  start_day = 365.0*(START_YEAR-BASE_YEAR)
  pdict     = {'startday':       start_day ,
               'nodes':          ALL_NODES ,
               'x_vals':         BR_MULT_X ,
               'y_vals':         BR_MULT_Y }

  camp_module.add(IV_BR_FORCE(pdict))


  # Add SIAs
  start_day = 365.0*(START_YEAR-BASE_YEAR)
  sia_year  = SIA_START
  sia_rate  = 1.0/(1.0-MCV1_RATE+0.001)

  while (sia_year < RUN_YEARS):
      sia_year = sia_year + max(2.0, np.random.poisson(sia_rate))
      pdict     = {'startday': 365.0*sia_year+start_day ,
                   'nodes':                   ALL_NODES ,
                   'agemin':                SIA_MIN_AGE ,
                   'agemax':                       5.00 ,
                   'coverage':             SIA_COVERAGE ,
                   'take_fac':               MAT_FACTOR }

      camp_module.add(IV_SIA(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************

# Routine immunization for MCV
def IV_MCV(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',                            SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',                 SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeLevelHealthTriggeredIVScaleUpSwitch',  SCHEMA_PATH)
  camp_iv02  = s2c.get_class_with_defaults('MultiInterventionDistributor',             SCHEMA_PATH)

  camp_iv03A = s2c.get_class_with_defaults('DelayedIntervention',                      SCHEMA_PATH)
  camp_iv04A = s2c.get_class_with_defaults('Vaccine',                                  SCHEMA_PATH)

  camp_iv03B = s2c.get_class_with_defaults('DelayedIntervention',                      SCHEMA_PATH)
  camp_iv04B = s2c.get_class_with_defaults('Vaccine',                                  SCHEMA_PATH)


  camp_event.Event_Coordinator_Config                   = camp_coord
  camp_event.Start_Day                                  = params['startday']
  camp_event.Nodeset_Config                             = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_coord.Intervention_Config                        = camp_iv01

  camp_iv01.Actual_IndividualIntervention_Config        = camp_iv02
  camp_iv01.Demographic_Coverage                        =    1.0              # Required, not used
  camp_iv01.Trigger_Condition_List                      = ['Births']
  camp_iv01.Demographic_Coverage_Time_Profile           = 'InterpolationMap'
  camp_iv01.Coverage_vs_Time_Interpolation_Map.Times    = [        365.0*0.0,        365.0*100.0]
  camp_iv01.Coverage_vs_Time_Interpolation_Map.Values   = [params['ri_rate'],  params['ri_rate']]
  camp_iv01.Not_Covered_IndividualIntervention_Configs  = []                  # Breaks if not present

  camp_iv02.Intervention_List                           = [camp_iv03A, camp_iv03B]

  camp_iv03A.Actual_IndividualIntervention_Configs      = [camp_iv04A]
  camp_iv03A.Delay_Period_Distribution                  = "GAUSSIAN_DISTRIBUTION"
  camp_iv03A.Delay_Period_Gaussian_Mean                 =  params['age_MCV1']
  camp_iv03A.Delay_Period_Gaussian_Std_Dev              =   90.0

  camp_iv04A.Acquire_Config.Initial_Effect              = 1.0
  camp_iv04B.Vaccine_Take                               = 0.95
  camp_iv04A.Take_Reduced_By_Acquire_Immunity           = params['take_fac']/2.0
  camp_iv04A.Take_By_Age_Multiplier.Times               = VEC_AGE
  camp_iv04A.Take_By_Age_Multiplier.Values              = VEC_TAKE

  camp_iv03B.Actual_IndividualIntervention_Configs      = [camp_iv04A]
  camp_iv03B.Coverage                                   = params['frac_MCV2']
  camp_iv03B.Delay_Period_Distribution                  = "GAUSSIAN_DISTRIBUTION"
  camp_iv03B.Delay_Period_Gaussian_Mean                 =  params['age_MCV2']
  camp_iv03B.Delay_Period_Gaussian_Std_Dev              =   90.0

  camp_iv04B.Acquire_Config.Initial_Effect              = 1.0
  camp_iv04B.Vaccine_Take                               = 0.95
  camp_iv04B.Take_Reduced_By_Acquire_Immunity           = params['take_fac']/2.0
  camp_iv04B.Take_By_Age_Multiplier.Times               = VEC_AGE
  camp_iv04B.Take_By_Age_Multiplier.Values              = VEC_TAKE


  return camp_event

#********************************************************************************

# Birth rate time dependency
def IV_BR_FORCE(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('NodeBirthRateMult',         SCHEMA_PATH)


  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_coord.Intervention_Config            = camp_iv

  camp_iv.Multiplier_By_Duration.Times      = params['x_vals']
  camp_iv.Multiplier_By_Duration.Values     = params['y_vals']

  return camp_event

#********************************************************************************

# SIAs for MCV
def IV_SIA(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('DelayedIntervention',       SCHEMA_PATH)
  camp_iv02  = s2c.get_class_with_defaults('Vaccine',                   SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv01
  camp_coord.Target_Demographic             = 'ExplicitAgeRanges'
  camp_coord.Demographic_Coverage           = params['coverage']
  camp_coord.Target_Age_Min                 = params['agemin']
  camp_coord.Target_Age_Max                 = params['agemax']

  camp_iv01.Actual_IndividualIntervention_Configs      = [camp_iv02]
  camp_iv01.Delay_Period_Distribution                  = "UNIFORM_DISTRIBUTION"
  camp_iv01.Delay_Period_Min                           =   0.0
  camp_iv01.Delay_Period_Max                           =  14.0

  camp_iv02.Acquire_Config.Initial_Effect              = 1.0
  camp_iv02.Vaccine_Take                               = 0.95
  camp_iv02.Take_Reduced_By_Acquire_Immunity           = params['take_fac']/2.0
  camp_iv02.Take_By_Age_Multiplier.Times               = VEC_AGE
  camp_iv02.Take_By_Age_Multiplier.Values              = VEC_TAKE


  return camp_event

#********************************************************************************