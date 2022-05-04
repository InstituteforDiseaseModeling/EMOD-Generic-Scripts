#********************************************************************************
#
# Builds a campaign for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

import emod_api.campaign as camp_module

from emod_api                 import schema_to_class   as   s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  SCHEMA_PATH   =  gdata.schema_path
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  # N/A


  # ***** Events *****

  # Import pressure
  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('ImportPressure',            SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, [1])

  camp_event.Event_Coordinator_Config = camp_coord
  camp_event.Start_Day                = 0
  camp_event.Nodeset_Config           = node_set

  camp_coord.Intervention_Config      = camp_iv

  camp_iv.Durations                   = [5.0]
  camp_iv.Daily_Import_Pressures      = [1.0]
  camp_iv.Import_Age                  = 40*365

  camp_module.add(camp_event)


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME



  return None

#********************************************************************************