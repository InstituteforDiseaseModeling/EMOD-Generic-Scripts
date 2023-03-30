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
  START_YEAR    = gdata.start_year
  RCV_YEAR      = gdata.rcv_year
  BR_MULT_X     = gdata.brate_mult_x
  BR_MULT_Y     = gdata.brate_mult_y


  # ***** Get variables for this simulation *****
  USE_RI        = gdata.var_params['use_RI']

  CHANGE_RI     = 0.0
  if('change_RI' in gdata.var_params):
    CHANGE_RI     = gdata.var_params['change_RI']


  # ***** Events *****

  node_dict = gdata.demog_node
  node_opts = list(node_dict.keys())


  # Add time varying birth rate
  start_day = 365.0*(START_YEAR-BASE_YEAR)
  pdict     = {'startday':       start_day ,
               'nodes':          ALL_NODES ,
               'x_vals':         BR_MULT_X ,
               'y_vals':         BR_MULT_Y }

  camp_module.add(IV_BR_FORCE(pdict))


  # Add MCV1 RI
  start_day = 365.0*(START_YEAR-BASE_YEAR)
  mcv1_dat  = np.loadtxt(os.path.join('Assets','data', 'NGA_MCV1.csv'), delimiter=',')
  with open(os.path.join('Assets','data', 'NGA_MCV1.json')) as fid01:
    mcv1_dict = json.load(fid01)

  time_vec  = np.array(mcv1_dict['timevec']) - start_day
  for k1 in range(len(mcv1_dict['namevec'])):
    reg_name  = mcv1_dict['namevec'][k1]
    mcv1_vec  = mcv1_dat[k1,:]
    node_list = list()

    for node_name in node_opts:
      if((node_name == reg_name) or (node_name.startswith(reg_name+':'))):
          node_list.append(node_dict[node_name])

    if(not node_list):
      continue

    ri_start  = (RCV_YEAR-START_YEAR)*365.0
    ri_rate   = 0.0
    if(USE_RI):
      ri_rate   = np.mean(mcv1_vec[-3:])

    time_list = [0.0] + [ri_start, ri_start+1.0]
    mcv1_list = [0.0] + [0.0,      ri_rate]

    if(USE_RI):
      for k2 in range(1,100):
        new_time = time_list[-1] + 365.0
        new_rate = max((1.0 - (1.0-mcv1_list[-1]) * (1.0-CHANGE_RI)),0.0)
        time_list.append(new_time)
        mcv1_list.append(new_rate)

    pdict     = {'startday':       start_day ,
                 'nodes':          node_list ,
                 'x_vals':         time_list ,
                 'y_vals':         mcv1_list }

    camp_module.add(IV_MCV1(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

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

  camp_iv.Multiplier_By_Duration.Times      = params['x_vals']
  camp_iv.Multiplier_By_Duration.Values     = params['y_vals']

  return camp_event

#********************************************************************************

# Routine immunization for MCV1
def IV_MCV1(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',                            SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',                 SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeLevelHealthTriggeredIVScaleUpSwitch',  SCHEMA_PATH)
  camp_iv02  = s2c.get_class_with_defaults('DelayedIntervention',                      SCHEMA_PATH)
  camp_iv03  = s2c.get_class_with_defaults('Vaccine',                                  SCHEMA_PATH)
  camp_wane  = s2c.get_class_with_defaults('WaningEffectConstant',                     SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config                   = camp_coord
  camp_event.Start_Day                                  = params['startday']
  camp_event.Nodeset_Config                             = node_set

  camp_coord.Intervention_Config                        = camp_iv01

  camp_iv01.Actual_IndividualIntervention_Config        = camp_iv02
  camp_iv01.Demographic_Coverage                        = 1.0                 # Required, not used
  camp_iv01.Trigger_Condition_List                      = ['Births']
  camp_iv01.Demographic_Coverage_Time_Profile           = 'InterpolationMap'
  camp_iv01.Coverage_vs_Time_Interpolation_Map.Times    = params['x_vals']
  camp_iv01.Coverage_vs_Time_Interpolation_Map.Values   = params['y_vals']
  camp_iv01.Not_Covered_IndividualIntervention_Configs  = []                  # Breaks if not present

  camp_iv02.Actual_IndividualIntervention_Configs       = [camp_iv03]
  camp_iv02.Delay_Period_Distribution                   = "GAUSSIAN_DISTRIBUTION"
  camp_iv02.Delay_Period_Gaussian_Mean                  =  300.0
  camp_iv02.Delay_Period_Gaussian_Std_Dev               =   90.0

  camp_iv03.Acquire_Config                              = camp_wane

  camp_wane.Initial_Effect                              =    1.0

  return camp_event

#********************************************************************************