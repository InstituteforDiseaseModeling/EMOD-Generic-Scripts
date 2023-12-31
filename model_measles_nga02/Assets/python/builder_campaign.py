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
  BR_MULT_X     = gdata.brate_mult_x
  BR_MULT_Y     = gdata.brate_mult_y


  # ***** Get variables for this simulation *****
  SIA_ADDLIST   = gdata.var_params['test_sias']

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

    if(np.amin(time_vec) <= 0.0):
      init_mcv1 = np.interp(0.0, time_vec, mcv1_vec)
    else:
      init_mcv1 = np.mean(mcv1_vec[:3])

    time_list = [0.0]       + (time_vec[time_vec>0.0]).tolist()
    time_list.append(time_list[-1] + 365.0)
    mcv1_list = [init_mcv1] + (mcv1_vec[time_vec>0.0]).tolist() + [np.mean(mcv1_vec[-3:])]

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


  # Add MCV SIAs
  with open(os.path.join('Assets','data','NGA_MCV_SIA.json')) as fid01:
    dict_sia = json.load(fid01)

  for sia_name in dict_sia:
    sia_obj    = dict_sia[sia_name]
    start_val  = sia_obj['date']
    if(start_val < start_day):
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
  pdict      = {'startday':       start_day ,
                'nodes':          all_nodes ,
                'peak_size':            1.3 ,
                'peak_wide':           45.0 ,
                'peak_time':           65.0 }

  camp_module.add(IV_BumpR0(pdict))


  # Use custom spec for intervention schedule
  for year_val in SIA_ADDLIST:
    start_val  = (year_val-BASE_YEAR)*365.0

    # Create and add intervention
    pdict      = {'startday':       start_val ,
                  'nodes':          all_nodes }
    camp_module.add(IV_SIA_ALT(pdict))



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
  camp_iv02.Event_Trigger_Distributed                   = "GP_EVENT_000"
  camp_iv02.Delay_Period_Distribution                   = "GAUSSIAN_DISTRIBUTION"
  camp_iv02.Delay_Period_Gaussian_Mean                  =  300.0
  camp_iv02.Delay_Period_Gaussian_Std_Dev               =   90.0

  camp_iv03.Acquire_Config                              = camp_wane
  camp_iv03.Cost_To_Consumer                            = 0.0

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
  camp_iv01.Cost_To_Consumer                = 0.0

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

# Distribute vaccines using OutbreakIndividual infections
def IV_SIA_ALT(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('OutbreakIndividual',        SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv
  camp_coord.Demographic_Coverage           =  0.75
  camp_coord.Target_Demographic             = 'ExplicitAgeRanges'
  camp_coord.Target_Age_Min                 =  0.75
  camp_coord.Target_Age_Max                 =  5.00

  camp_iv.Clade                             = 0
  camp_iv.Genome                            = 1
  camp_iv.Ignore_Immunity                   = 0
  camp_iv.Cost_To_Consumer                  = 1.0

  return camp_event

#********************************************************************************