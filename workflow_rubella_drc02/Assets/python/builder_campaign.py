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
  SCHEMA_PATH   =  gdata.schema_path
  ALL_NODES     =  gdata.demog_object.node_ids
  TIME_START    =  gdata.start_time
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****

  RI_RATE      = gdata.var_params['RI_rate']

  BR_MULT_X    = gdata.brate_mult_x
  BR_MULT_Y    = gdata.brate_mult_y


  # ***** Events *****

  # Add MCV RI
  start_ri  = TIME_START + 20*365.0
  pdict     = {'startday':       start_ri   ,
               'nodes':          ALL_NODES  ,
               'coverage':       RI_RATE    }

  camp_module.add(IV_MCV1(pdict))


  # Add time varying birth rate
  start_brm = TIME_START
  br_vec_x  = (np.array(BR_MULT_X)*365 - 2000*365.0).tolist()
  pdict     = {'startday':       start_brm ,
               'nodes':          ALL_NODES ,
               'x_vals':         br_vec_x  ,
               'y_vals':         BR_MULT_Y }

  camp_module.add(IV_BR_FORCE(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************

# Routine immunization for MCV1
def IV_MCV1(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',               SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',    SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeLevelHealthTriggeredIV',  SCHEMA_PATH)
  camp_iv02  = s2c.get_class_with_defaults('DelayedIntervention',         SCHEMA_PATH)
  camp_iv03  = s2c.get_class_with_defaults('Vaccine',                     SCHEMA_PATH)
  camp_wane  = s2c.get_class_with_defaults('WaningEffectConstant',        SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config                 = camp_coord
  camp_event.Start_Day                                = params['startday']
  camp_event.Nodeset_Config                           = node_set

  camp_coord.Intervention_Config                      = camp_iv01

  camp_iv01.Actual_IndividualIntervention_Config      = camp_iv02
  camp_iv01.Demographic_Coverage                      = params['coverage']
  camp_iv01.Trigger_Condition_List                    = ['Births']

  camp_iv02.Actual_IndividualIntervention_Configs     = [camp_iv03]
  camp_iv02.Delay_Period_Distribution                 = "GAUSSIAN_DISTRIBUTION"
  camp_iv02.Delay_Period_Gaussian_Mean                =  300.0
  camp_iv02.Delay_Period_Gaussian_Std_Dev             =   90.0

  camp_iv03.Acquire_Config                            = camp_wane

  camp_wane.Initial_Effect                            =    1.0

  return camp_event

#********************************************************************************

# Birth rate time dependency
def IV_BR_FORCE(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('NodeBirthRateMult',         SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv

  camp_iv.Multiplier_By_Duration.Times      = params['x_vals'] + [365.0*100.0]
  camp_iv.Multiplier_By_Duration.Values     = params['y_vals'] + [params['y_vals'][-1]]

  return camp_event

#********************************************************************************