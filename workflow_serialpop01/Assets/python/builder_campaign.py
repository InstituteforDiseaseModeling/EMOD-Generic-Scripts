#********************************************************************************
#
# Builds a campaign for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

import emod_api.campaign     as     camp_module

from emod_api                 import schema_to_class as s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  SCHEMA_PATH   =  gdata.schema_path
  DEMOG_OBJ     =  gdata.demog_object
  #ALL_NODES     =  DEMOG_OBJ.node_ids()    #Currently bugged
  ALL_NODES     = [1]
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  INF_PHASE             = gdata.var_params['inf_force_sin_phase']
  INF_AMP               = gdata.var_params['inf_force_sin_amp']
  INF_RES_END   = gdata.var_params['inf_res_end']
  SIA_START_DAY   = gdata.var_params['sia_start']
  SIA_COVERAGE   = gdata.var_params['sia_coverage']
  if 'final_sia_coverage' in gdata.var_params:
    FINAL_SIA_COVERAGE = gdata.var_params['final_sia_coverage']
  else:
    FINAL_SIA_COVERAGE = SIA_COVERAGE

  # ***** Events *****

  # Sinusoidal seasonal infectivity forcing
  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('NodeInfectivityMult',       SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, ALL_NODES)

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = 0
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv
  camp_coord.Number_Repetitions             =  -1       # Repeat forever
  camp_coord.Timesteps_Between_Repetitions  = 365.0

  xval = np.arange(0.0,365.0)
  yval = 1.0 + INF_AMP*np.sin(2.0*np.pi*(xval-INF_PHASE)/365.0)

  camp_iv.Multiplier_By_Duration.Times      = xval.tolist()
  camp_iv.Multiplier_By_Duration.Values     = yval.tolist()

  camp_module.add(camp_event)

  # Daily importation pressure
  camp_event = s2c.get_class_with_defaults('CampaignEvent',               SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',    SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('ImportPressure',       SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, ALL_NODES)

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = INF_RES_END * 365
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv

  camp_iv.Durations = [100*365]
  camp_iv.Daily_Import_Pressures = [0.03]
  camp_iv.Import_Age = 40*365

  camp_module.add(camp_event)

  if not isinstance(SIA_START_DAY, list):
    SIA_START_DAY = [SIA_START_DAY]

  for ix, this_sia_day in enumerate(SIA_START_DAY):
    # SIAs
    camp_event = s2c.get_class_with_defaults('CampaignEvent',               SCHEMA_PATH)
    camp_coord = s2c.get_class_with_defaults('StandardInterventionDistributionEventCoordinator',    SCHEMA_PATH)
    camp_iv01  = s2c.get_class_with_defaults("Vaccine", SCHEMA_PATH)
    camp_wane1 = s2c.get_class_with_defaults('WaningEffectConstant',        SCHEMA_PATH)

    node_set   = utils.do_nodes(SCHEMA_PATH, ALL_NODES)

    camp_event.Event_Coordinator_Config                 = camp_coord
    camp_event.Start_Day                                = this_sia_day
    camp_event.Nodeset_Config                           = node_set

    camp_coord.Intervention_Config                      = camp_iv01
    camp_coord.Target_Age_Max = 5.0
    camp_coord.Target_Age_Min = 0.75
    if ix != (len(SIA_START_DAY) - 1):
      camp_coord.Demographic_Coverage                      = SIA_COVERAGE
    else:
      camp_coord.Demographic_Coverage = FINAL_SIA_COVERAGE
    camp_iv01.Acquire_Config                            = camp_wane1

    camp_wane1.Initial_Effect                           =    1.0     # Binary; if vaccinated get

    camp_module.add(camp_event)

  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************