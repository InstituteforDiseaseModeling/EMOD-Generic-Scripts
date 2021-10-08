#********************************************************************************
#
# Builds a campaign file for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

from refdat_sias          import data_dict   as dict_sia
from refdat_sias_nopv     import data_dict   as dict_sia_nopv


import numpy as np

import emod_api.campaign     as     camp_module

from emod_api                 import schema_to_class as s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  TIME_START   = gdata.var_params['start_time']

  SIAS_SABIN   = gdata.var_params['sia_calendar']
  SIAS_NOPV    = gdata.var_params['sia_calendar_nopv']
  SIA_COVER    = gdata.var_params['sia_coverage']

  SIAS_ETC     = gdata.var_params['sia_other']
  SIA_ADDLIST  = gdata.var_params['sia_sets']

  OPV_BOXES    = gdata.var_params['OPV_compartments']
  NOPV_BOXES   = gdata.var_params['nOPV_compartments']

  SIA_STOP = 1.0e9
  if('sia_cutoff' in gdata.var_params):
    SIA_STOP     = gdata.var_params['sia_cutoff']

  # ***** Events *****

  node_dict = gdata.demog_node
  node_opts = list(node_dict.keys())


  # Use SIA calendar for Sabin intervention schedule
  if(SIAS_SABIN):
    for sia_name in dict_sia:
      sia_obj = dict_sia[sia_name]

      node_list = list()
      for targ_val in sia_obj['nodes']:
        for node_name in node_opts:
          if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
            node_list.append(node_dict[node_name])
      start_val  = sia_obj['date']

      if(start_val > SIA_STOP):
        continue

      pdict     = {'startday':                                start_val ,
                   'nodes':                                   node_list ,
                   'coverage':                                SIA_COVER ,
                   'vaccine_type':                                    0 ,
                   'strain_type':                            NOPV_BOXES ,
                   'immune_override':                                 0 }

      camp_module.add(IV_OPV2(pdict))


  # Use SIA calendar for nOPV intervention schedule
  if(SIAS_NOPV):
    for sia_name in dict_sia_nopv:
      sia_obj = dict_sia_nopv[sia_name]

      node_list = list()
      for targ_val in sia_obj['nodes']:
        for node_name in node_opts:
          if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
            node_list.append(node_dict[node_name])
      start_val  = sia_obj['date']

      if(start_val > SIA_STOP):
        continue

      pdict     = {'startday':                                start_val ,
                   'nodes':                                   node_list ,
                   'coverage':                                SIA_COVER ,
                   'vaccine_type':                                    1 ,
                   'strain_type':                                     0 ,
                   'immune_override':                                 0 }

      camp_module.add(IV_OPV2(pdict))


  # Use custom spec for intervention schedule
  if(SIAS_ETC):
    for sia_obj in SIA_ADDLIST:

      node_list = list()
      for targ_val in sia_obj['targ_list']:
        for node_name in node_opts:
          if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
            node_list.append(node_dict[node_name])
      start_val  = gdata.start_off + TIME_START + sia_obj['day_offset']
      num_agents = sia_obj['num_cases']
      agent_wght = sia_obj['agent_wght']
      node_list  = [node_list[np.random.randint(low=0,high=len(node_list))]]

      pdict     = {'startday':                                start_val ,
                   'nodes':                                   node_list ,
                   'num_cases':                              num_agents ,
                   'ind_wght':                               agent_wght ,
                   'strain_type':                  NOPV_BOXES+OPV_BOXES }
      camp_module.add(IV_cVDPV2(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************

# Distribute vaccines using OutbreakIndividual infections
def IV_OPV2(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('OutbreakIndividual',        SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv
  camp_coord.Demographic_Coverage           = params['coverage']
  camp_coord.Target_Demographic             = 'ExplicitAgeRanges'
  camp_coord.Target_Age_Min                 =  0.75
  camp_coord.Target_Age_Max                 =  5.00

  camp_iv.Clade                             = params['vaccine_type']
  camp_iv.Genome                            = params['strain_type']
  camp_iv.Ignore_Immunity                   = params['immune_override']
  camp_iv.Cost_To_Consumer                  = 1.0

  return camp_event

#********************************************************************************

# Distribute seed infections using Oubreak
def IV_cVDPV2(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('Outbreak',                  SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv

  camp_iv.Genome                            = params['strain_type']
  camp_iv.Number_Cases_Per_Node             = params['num_cases']
  camp_iv.Import_Age                        =  7300.0
  camp_iv.Import_Female_Prob                =     0.0
  camp_iv.Import_Agent_MC_Weight            = params['ind_wght']

  return camp_event

#********************************************************************************