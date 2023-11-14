#********************************************************************************
#
# Builds a campaign for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

import numpy as np

import emod_api.campaign     as     camp_module

from emod_api                 import schema_to_class as s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  CAMP_FILENAME =  'campaign.json'

  ALL_NODES     = gdata.demog_object.node_ids
  BASE_YEAR     = gdata.base_year
  BR_MULT_X     = gdata.brate_mult_x
  BR_MULT_Y     = gdata.brate_mult_y


  # ***** Get variables for this simulation *****
  MCV1_RATE     = gdata.var_params['MCV1']
  MCV2_FRAC     = gdata.var_params['MCV2']
  MCV1_AGE      = gdata.var_params['MCV1_age']
  MCV2_AGE      = gdata.var_params['MCV2_age']
  START_YEAR    = gdata.var_params['start_year']
  if 'mat_factor_vx' in gdata.var_params.keys():
    MAT_FACTOR = gdata.var_params['mat_factor_vx']
  else:
    MAT_FACTOR = gdata.var_params['mat_factor']
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

  if gdata.var_params.get('timeliness_distribution') is not None:
    pdict['timeliness'] = gdata.var_params['timeliness_distribution']

  if gdata.varparams.get('Ageind_vx_model') is not None:
    pdict['Ageind_vx_model'] = gdata.var_params['Ageind_vx_model']

  camp_module.add(IV_MCV(pdict))


  # Add time varying birth rate
  start_day = 365.0*(START_YEAR-BASE_YEAR)
  pdict     = {'startday':       start_day ,
               'nodes':          ALL_NODES ,
               'x_vals':         BR_MULT_X ,
               'y_vals':         BR_MULT_Y }

  camp_module.add(IV_BR_FORCE(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************

# Routine immunization for MCV
def IV_MCV(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  VEC_AGE  = [0/12*365, 3/12*365, 5/12*365, 7/12*365, 9/12*365]
  VEC_TAKE = [     0.0,      0.0,     0.65,     0.92,      1.0]

  if params.get('Ageind_vx_model'):
    VEC_TAKE = [1.0]*len(VEC_AGE)

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
  if params.get('timeliness') is False:
    camp_iv03A.Delay_Period_Gaussian_Std_Dev            = 0.25
  else:
    camp_iv03A.Delay_Period_Gaussian_Std_Dev            =  params['age_MCV1']/3.0


  camp_iv04A.Acquire_Config.Initial_Effect              = 1.0
  camp_iv04B.Vaccine_Take                               = 0.95
  camp_iv04A.Take_Reduced_By_Acquire_Immunity           = params['take_fac']
  camp_iv04A.Take_By_Age_Multiplier.Times               = VEC_AGE
  camp_iv04A.Take_By_Age_Multiplier.Values              = VEC_TAKE

  camp_iv03B.Actual_IndividualIntervention_Configs      = [camp_iv04A]
  camp_iv03B.Coverage                                   = params['frac_MCV2']
  camp_iv03B.Delay_Period_Distribution                  = "GAUSSIAN_DISTRIBUTION"
  camp_iv03B.Delay_Period_Gaussian_Mean                 =  params['age_MCV2']
  if params.get('timeliness') is False:
    camp_iv03B.Delay_Period_Gaussian_Std_Dev = 0.25
  else:
    camp_iv03B.Delay_Period_Gaussian_Std_Dev = 90.0

  camp_iv04B.Acquire_Config.Initial_Effect              = 1.0
  camp_iv04B.Vaccine_Take                               = 0.95
  camp_iv04B.Take_Reduced_By_Acquire_Immunity           = params['take_fac']
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