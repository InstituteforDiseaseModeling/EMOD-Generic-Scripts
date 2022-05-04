#********************************************************************************
#
# Builds a campaign for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

import emod_api.campaign as camp_module

from builder_demographics     import br_force_xval, br_force_yval

from emod_api                 import schema_to_class   as   s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  SCHEMA_PATH   =  gdata.schema_path
  ALL_NODES     =  gdata.demog_object.node_ids
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  USE_BR_FORCE  = gdata.var_params['variable_birthrate']


  # ***** Events *****

  # Birth rate time dependency
  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('NodeBirthRateMult',         SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, ALL_NODES)

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = 0
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv

  xval = np.array(br_force_xval)*365.0
  yval = np.array(br_force_yval)

  if(not USE_BR_FORCE):
    yval = 1.0 + 0.0*yval

  camp_iv.Multiplier_By_Duration.Times      = xval.tolist()
  camp_iv.Multiplier_By_Duration.Values     = yval.tolist()

  camp_module.add(camp_event)


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************