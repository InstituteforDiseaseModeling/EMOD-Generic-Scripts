#********************************************************************************
#
# Builds a campaign file for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

from aux_matrix_calc import mat_magic

import numpy as np

import emod_api.campaign     as     camp_module

from emod_api                 import schema_to_class as s2c
from emod_api.interventions   import utils

#********************************************************************************

def campaignBuilder():

  # Note: campaign module itself is the file object; no Campaign class right now
  CAMP_FILENAME =  'campaign.json'


  # ***** Get variables for this simulation *****
  CTEXT_VAL    = gdata.var_params['ctext_val']
  NUM_NODES    = gdata.var_params['num_nodes']

  SIOS_FRAC    = gdata.var_params['self_isolate_on_symp_frac']
  SIOS_EFFECT  = gdata.var_params['self_isolate_effectiveness']

  HCW_PPE      = gdata.var_params['HCW_PPE']

  IP_START     = gdata.var_params['importations_start_day']
  IP_DURATION  = gdata.var_params['importations_duration']
  IP_RATE      = gdata.var_params['importations_daily_rate']

  HCW_WALK     = gdata.var_params['HCW_Walk']
  HCW_FRAC     = 0.1
  HCW_START    = gdata.var_params['HCW_Walk_Start']
  HCW_END      = gdata.var_params['HCW_Walk_End']

  BOB_WALK     = gdata.var_params['Bob_Walk']
  BOB_FRAC     = gdata.var_params['Bob_Frac']
  BOB_START    = gdata.var_params['Bob_Walk_Start']
  BOB_END      = gdata.var_params['Bob_Walk_End']

  AGE_ACQ      = gdata.var_params['age_effect_a']
  AGE_TRN      = gdata.var_params['age_effect_t']

  AF_START     = gdata.var_params['active_finding_start_day']
  AF_COVER     = gdata.var_params['active_finding_coverage']
  AF_QUAL      = gdata.var_params['active_finding_effectiveness']
  AF_DELAY     = gdata.var_params['active_finding_delay']

  TRANS_RANGE  = range(2,14)

  DICT_TRANS   = {k1: gdata.var_params[          'trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}
  DICT_SPIKE   = {k1: gdata.var_params[    'spike_trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}
  DICT_NUDGE   = {k1: gdata.var_params[    'nudge_trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}
  DICT_H2H     = {k1: gdata.var_params[      'household_sia{:02d}'.format(k1)] for k1 in TRANS_RANGE}
  DICT_START   = {k1: gdata.var_params['start_day_trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}

  NODES_ALL    = list(range(1,NUM_NODES+1))


  # ***** Events *****

  # Contact pattern revision
  for k1 in TRANS_RANGE:
    pdict = {'arg_dist':               DICT_TRANS[k1] ,
             'spike_mat':              DICT_SPIKE[k1] ,
             'nudge_mat':              DICT_NUDGE[k1] ,
             'hcw_h2h':                  DICT_H2H[k1] ,
             'ctext_val':                   CTEXT_VAL }
    (_, _, matblock) = mat_magic(pdict)
    pdict = {'startday':               DICT_START[k1] ,
             'nodes':                       NODES_ALL ,
             'matblock':                     matblock }
    camp_module.add(IV_MatrixSwap(pdict))


  # Tour for HCW
  if(HCW_WALK):
    for k1 in range(HCW_START,HCW_END):
      for k2 in range(5):
        pdict = {'startday':                                                   k1 ,
                 'node_dest':                      np.random.randint(2,NUM_NODES) ,
                 'duration':                                                    2 ,
                 'fraction':                                             HCW_FRAC ,
                 'group_names':            [{'Restrictions': ['Geographic:HCW']}] }
        camp_module.add(IV_TakeAWalk(pdict))


  # Tour for Bob
  if(BOB_WALK):
    for k1 in range(BOB_START,BOB_END):
      for k2 in range(5):
        pdict = {'startday':                                                   k1 ,
                 'node_dest':                      np.random.randint(2,NUM_NODES) ,
                 'duration':                                                    1 ,
                 'fraction':                                             BOB_FRAC ,
                 'group_names':  [{'Restrictions':  ['Geographic:age25_riskMD']}] }
        camp_module.add(IV_TakeAWalk(pdict))


  # Infection importation
  pdict = {'startday':                                            IP_START ,
           'duration':                                         IP_DURATION ,
           'amount':                                               IP_RATE }
  camp_module.add(IV_ImportPressure(pdict))


  # Age-dependent susceptibility
  pdict = {'startday':                                                  10 ,
           'coverage':                                                1.00 ,
           'nodes':                                              NODES_ALL ,
           'qual_acq':                                        AGE_ACQ*0.95 ,
           'qual_trn':                                        AGE_TRN*0.95 ,
           'group_names':  [{'Restrictions': ['Geographic:age00_riskLO']},
                            {'Restrictions': ['Geographic:age00_riskMD']},
                            {'Restrictions': ['Geographic:age00_riskHI']}] }
  camp_module.add(IV_MultiEffect(pdict))

  pdict = {'startday':                                                  11 ,
           'coverage':                                                1.00 ,
           'nodes':                                              NODES_ALL ,
           'qual_acq':                                        AGE_ACQ*0.75 ,
           'qual_trn':                                        AGE_TRN*0.75 ,
           'group_names':  [{'Restrictions': ['Geographic:age05_riskLO']},
                            {'Restrictions': ['Geographic:age05_riskMD']},
                            {'Restrictions': ['Geographic:age05_riskHI']}] }
  camp_module.add(IV_MultiEffect(pdict))

  pdict = {'startday':                                                  12 ,
           'coverage':                                                1.00 ,
           'nodes':                                              NODES_ALL ,
           'qual_acq':                                        AGE_ACQ*0.60 ,
           'qual_trn':                                        AGE_TRN*0.60 ,
           'group_names':  [{'Restrictions': ['Geographic:age10_riskLO']},
                            {'Restrictions': ['Geographic:age10_riskMD']},
                            {'Restrictions': ['Geographic:age10_riskHI']}] }
  camp_module.add(IV_MultiEffect(pdict))

  pdict = {'startday':                                                  13 ,
           'coverage':                                                1.00 ,
           'nodes':                                              NODES_ALL ,
           'qual_acq':                                        AGE_ACQ*0.35 ,
           'qual_trn':                                        AGE_TRN*0.35 ,
           'group_names':  [{'Restrictions': ['Geographic:age15_riskLO']},
                            {'Restrictions': ['Geographic:age15_riskMD']},
                            {'Restrictions': ['Geographic:age15_riskHI']}] }
  camp_module.add(IV_MultiEffect(pdict))


  # Self-quarantine
  pdict = {'trigger':                                   'NewlySymptomatic' ,
           'startday':                                                  15 ,
           'nodes':                                              NODES_ALL ,
           'coverage':                                           SIOS_FRAC ,
           'quality':                                          SIOS_EFFECT ,
           'delay':                                                   0.00 }
  camp_module.add(IV_Quarantine(pdict))


  # PPE for HCW
  pdict = {'startday':                                                  20 ,
           'coverage':                                                1.00 ,
           'nodes':                                              NODES_ALL ,
           'qual_acq':                                             HCW_PPE ,
           'qual_trn':                                             HCW_PPE ,
           'group_names':  [{'Restrictions':          ['Geographic:HCW']}] }
  camp_module.add(IV_MultiEffect(pdict))


  # Active case finding
  pdict = {'trigger':                                       'NewInfection' ,
           'startday':                                            AF_START ,
           'nodes':                                              NODES_ALL ,
           'coverage':                                            AF_COVER ,
           'quality':                                              AF_QUAL ,
           'delay':                                          2.00+AF_DELAY }
  camp_module.add(IV_Quarantine(pdict))


  #  ***** End file construction *****
  camp_module.save(filename=CAMP_FILENAME)

  # Save filename to global data for use in other functions
  gdata.camp_file = CAMP_FILENAME


  return None

#********************************************************************************

# Event for quarantine
def IV_Quarantine(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event    = s2c.get_class_with_defaults('CampaignEvent',                          SCHEMA_PATH)
  camp_coord    = s2c.get_class_with_defaults('CommunityHealthWorkerEventCoordinator',  SCHEMA_PATH)
  camp_iv       = s2c.get_class_with_defaults('Vaccine',                                SCHEMA_PATH)
  camp_wane_trn = s2c.get_class_with_defaults('WaningEffectMapPiecewise',               SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config            = camp_coord
  camp_event.Start_Day                           = 120*365+params['startday']
  camp_event.Nodeset_Config                      = node_set

  camp_coord.Intervention_Config                 = camp_iv
  camp_coord.Trigger_Condition_List              = [ params['trigger'] ]
  camp_coord.Duration                            = 1000
  camp_coord.Waiting_Period                      = 1000
  camp_coord.Max_Distributed_Per_Day             = 1e9
  camp_coord.Days_Between_Shipments              = 1000
  camp_coord.Amount_In_Shipment                  = 0
  camp_coord.Initial_Amount_Distribution         = 'CONSTANT_DISTRIBUTION'
  camp_coord.Initial_Amount_Constant             = 1e9

  camp_iv.Vaccine_Take                           = params['coverage']
  camp_iv.Transmit_Config                        = camp_wane_trn

  camp_wane_trn.Initial_Effect                   = 1.0
  camp_wane_trn.Reference_Timer                  = 0.0
  camp_wane_trn.Durability_Map.Times             = [ 0.0, 1.0+params['delay']   ]
  camp_wane_trn.Durability_Map.Values            = [ 0.0,     params['quality'] ]


  return camp_event


#********************************************************************************

# IPC measures
def IV_MultiEffect(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event    = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord    = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv       = s2c.get_class_with_defaults('Vaccine',                   SCHEMA_PATH)
  camp_wane_acq = s2c.get_class_with_defaults('WaningEffectConstant',      SCHEMA_PATH)
  camp_wane_trn = s2c.get_class_with_defaults('WaningEffectConstant',      SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config            = camp_coord
  camp_event.Start_Day                           = 120*365+params['startday']
  camp_event.Nodeset_Config                      = node_set

  camp_coord.Intervention_Config                 = camp_iv
  camp_coord.Property_Restrictions_Within_Node   = params['group_names']

  camp_iv.Vaccine_Take                           = params['coverage']
  camp_iv.Acquire_Config                         = camp_wane_acq
  camp_iv.Transmit_Config                        = camp_wane_trn

  camp_wane_acq.Initial_Effect                   = params['qual_acq']

  camp_wane_trn.Initial_Effect                   = params['qual_trn']


  return camp_event


#********************************************************************************

# Contagion import
def IV_ImportPressure(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('ImportPressure',            SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, [1])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = 120*365+params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv

  camp_iv.Daily_Import_Pressures            = [params['amount']]
  camp_iv.Durations                         = [params['duration']]
  camp_iv.Import_Age                        = 12775


  return camp_event


#********************************************************************************

# HINT revision
def IV_MatrixSwap(params=dict()):
 
  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('ChangeIPMatrix',            SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

  camp_event.Event_Coordinator_Config       = camp_coord
  camp_event.Start_Day                      = 120*365+params['startday']
  camp_event.Nodeset_Config                 = node_set

  camp_coord.Intervention_Config            = camp_iv

  camp_iv.Property_Name                     = 'Geographic'
  camp_iv.New_Matrix                        = params['matblock'].tolist()

  return camp_event


#********************************************************************************

# Forced movement for HCW and others
def IV_TakeAWalk(params=dict()):

  SCHEMA_PATH   =  gdata.schema_path

  camp_event = s2c.get_class_with_defaults('CampaignEvent',             SCHEMA_PATH)
  camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator',  SCHEMA_PATH)
  camp_iv    = s2c.get_class_with_defaults('MigrateIndividuals',        SCHEMA_PATH)

  node_set   = utils.do_nodes(SCHEMA_PATH, [1])

  camp_event.Event_Coordinator_Config            = camp_coord
  camp_event.Start_Day                           = 120*365+params['startday']
  camp_event.Nodeset_Config                      = node_set

  camp_coord.Intervention_Config                 = camp_iv
  camp_coord.Demographic_Coverage                = params['fraction']
  camp_coord.Property_Restrictions_Within_Node   = params['group_names']

  camp_iv.NodeID_To_Migrate_To                   = params['node_dest']
  camp_iv.Duration_Before_Leaving_Distribution   = 'CONSTANT_DISTRIBUTION'
  camp_iv.Duration_Before_Leaving_Constant       = 0
  camp_iv.Duration_At_Node_Distribution          = 'CONSTANT_DISTRIBUTION'
  camp_iv.Duration_At_Node_Constant              = params['duration']


  return camp_event

#********************************************************************************