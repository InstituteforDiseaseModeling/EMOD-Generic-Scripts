#********************************************************************************
#
# Builds a campaign file for input to the DTK.
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
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  TIME_START   = gdata.start_time
  PEAK_SIZE    = gdata.var_params['R0_peak_magnitude']
  PEAK_TIME    = gdata.var_params['R0_peak_day']
  PEAK_WIDE    = gdata.var_params['R0_peak_width']


  # ***** Events *****

  node_dict = gdata.demog_node
  node_opts = list(node_dict.keys())


  # Add MCV1 RI
  mcv1_dat = np.loadtxt(os.path.join('Assets','data', 'NGA_MCV1.csv'), delimiter=',')
  with open(os.path.join('Assets','data', 'NGA_MCV1.json')) as fid01:
    mcv1_dict = json.load(fid01)

  time_vec  = np.array(mcv1_dict['timevec']) - TIME_START
  for k1 in range(len(mcv1_dict['namevec'])):
    reg_name  = mcv1_dict['namevec'][k1]
    mcv1_vec  = mcv1_dat[k1,:]
    node_list = list()

    for node_name in node_opts:
      if((node_name == reg_name) or (node_name.startswith(reg_name+':'))):
          node_list.append(node_dict[node_name])

    if(not node_list):
      continue

    if(np.amin(time_vec) <= 0.0):
      init_mcv1 = np.interp(0.0, time_vec, mcv1_vec)
    else:
      init_mcv1 = np.mean(mcv1_vec[:3])

    time_list = [0.0]       + (time_vec[time_vec>0.0]).tolist() + [365.0*100]
    mcv1_list = [init_mcv1] + (mcv1_vec[time_vec>0.0]).tolist() + [np.mean(mcv1_vec[-3])]

    pdict     = {'startday':       TIME_START ,
                 'nodes':          node_list  ,
                 'x_vals':         time_list   ,
                 'y_vals':         mcv1_list   }

    camp_module.add(IV_MCV1(pdict))


  # Add MCV SIAs
  with open(os.path.join('Assets','data','NGA_MCV_SIA.json')) as fid01:
    dict_sia = json.load(fid01)

  for sia_name in dict_sia:
    sia_obj    = dict_sia[sia_name]
    start_val  = sia_obj['date']
    if(start_val < TIME_START):
      continue

    SIA_COVER  = 0.50
    age_min    = sia_obj['age_min']
    age_max    = sia_obj['age_max']
    targ_frac  = sia_obj['targ_frac']
    node_list  = list()
    for targ_val in sia_obj['nodes']:
      for node_name in node_opts:
        if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
          node_list.append(node_dict[node_name])

    if(not node_list):
      continue

    pdict     = {'startday':       start_val ,
                 'nodes':          node_list ,
                 'agemin':         age_min ,
                 'agemax':         age_max ,
                 'coverage':       SIA_COVER*targ_frac }

    camp_module.add(IV_SIA(pdict))


  # Add infectivity seasonality
  all_nodes  = [node_dict[val] for val in node_opts]
  pdict      = {'startday':       TIME_START ,
                'nodes':          all_nodes ,
                'peak_size':      PEAK_SIZE ,
                'peak_wide':      PEAK_WIDE ,
                'peak_time':      PEAK_TIME }

  camp_module.add(IV_BumpR0(pdict))


  # Add infectivity trough
  #all_nodes  = [node_dict[val] for val in node_opts]
  #pdict      = {'nodes':          all_nodes }

  camp_module.add(IV_ReduceR0(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

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

# SIAs for MCV
def IV_SIA(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('Vaccine',                   SCHEMA_PATH)
  camp_wane  = s2c.get_class_with_defaults('WaningEffectConstant',      SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv01
  camp_coord.Target_Demographic             = 'ExplicitAgeRanges'
  camp_coord.Demographic_Coverage           = params['coverage']
  camp_coord.Target_Age_Min                 = params['agemin']/365.0
  camp_coord.Target_Age_Max                 = params['agemax']/365.0

  camp_iv01.Acquire_Config                  = camp_wane

  camp_wane.Initial_Effect                  = 1.0

  return camp_event

#********************************************************************************

# Seasonal infectivity forcing; boxcar
def IV_BumpR0(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeInfectivityMult',       SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv01
  camp_coord.Number_Repetitions             =  -1       # Repeat forever
  camp_coord.Timesteps_Between_Repetitions  = 365.0

  init_off =  params['startday']           %365.0
  peak_wid =  params['peak_wide']
  x_peak   = (params['peak_time']-init_off)%365.0
  y_peak   =  params['peak_size']
  x_init   = (x_peak             -peak_wid)%365.0
  x_ends   = (x_peak             +peak_wid)%365.0

  if(peak_wid > x_peak):
    dx_val = x_peak
  elif(peak_wid > 365.0-x_peak):
    dx_val = 365.0-x_peak
  else:
    dx_val = peak_wid

  #y_bound  = y_peak - (y_peak-1)/peak_wid * dx_val
  y_bound  = y_peak - (y_peak-1)*(dx_val>=peak_wid)

  xyvals   = set([(   0.0,     y_bound),
                  (x_init,         1.0),
                  (x_init+0.1,  y_peak),
                  (x_peak,      y_peak),
                  (x_ends-0.1,  y_peak),
                  (x_ends,         1.0),
                  ( 365.0,     y_bound)])
  xyvals   = sorted(list(xyvals), key=lambda val: val[0])

  camp_iv01.Multiplier_By_Duration.Times      = [val[0] for val in xyvals]
  camp_iv01.Multiplier_By_Duration.Values     = [val[1] for val in xyvals]

  return camp_event

#********************************************************************************

# Lower transmissibility during pandemic
def IV_ReduceR0(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv01  = s2c.get_class_with_defaults('NodeInfectivityMult',       SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = 120.0*365.0
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv01
  camp_coord.Number_Repetitions             =   1
  camp_coord.Timesteps_Between_Repetitions  =   0.0

  camp_iv01.Multiplier_By_Duration.Times      = [0.0*365.0, 2.0*365.0, 4.0*365.0]
  camp_iv01.Multiplier_By_Duration.Values     = [0.75,      0.75,      1.0]

  return camp_event

#********************************************************************************