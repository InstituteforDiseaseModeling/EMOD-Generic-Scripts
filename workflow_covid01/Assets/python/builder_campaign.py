#********************************************************************************
#
# Builds a campaign file for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

from aux_matrix_calc import mat_magic

ext_py_path = os.path.join('Assets','site-packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy as np

#********************************************************************************

def campaignBuilder(params=dict()):

  # Dictionary to be written
  json_set = dict()

  
  # ***** Campaign file *****
  json_set['Campaign_Name'] = 'COMMENT_FIELD'
  json_set['Events']        = []
  json_set['Use_Defaults']  = 1


  # ***** Super hacky for backwards compatibility; bite me *****
  if 'HCW_Frac' not in params:
    params['HCW_Frac'] = 0.1


  # ***** Events *****

  # Contact pattern revision
  for k1 in range(2,999):
    if('trans_mat{:02d}'.format(k1) not in params):
      break
    
    pdict = {'arg_dist':         params['trans_mat{:02d}'.format(k1)] ,
             'spike_mat':  params['spike_trans_mat{:02d}'.format(k1)] ,
             'nudge_mat':  params['nudge_trans_mat{:02d}'.format(k1)] ,
             'hcw_h2h':      params['household_sia{:02d}'.format(k1)] ,
             'ctext_val':                         params['ctext_val'] }
    (_, _, matblock) = mat_magic(pdict)
    pdict = {'startday':   params['start_day_trans_mat{:02d}'.format(k1)] ,
             'only_urb':              params['urb_targ{:02d}'.format(k1)] ,
             'only_rur':              params['rur_targ{:02d}'.format(k1)] ,
             'num_nodes':                             params['num_nodes'] ,
             'matblock':                                         matblock }
    json_set['Events'].extend(IV_MatrixSwap(pdict))


  # Infection importation
  pdict = {'startday':       params['importations_start_day'] ,
           'duration':        params['importations_duration'] ,
           'amount':        params['importations_daily_rate'] }
  json_set['Events'].extend(IV_ImportPressure(pdict))


  # Self-quarantine
  pdict = {'trigger':                      'NewlySymptomatic' ,
           'startday':                                     15 ,
           'coverage':    params['self_isolate_on_symp_frac'] ,
           'quality':    params['self_isolate_effectiveness'] ,
           'delay':                                      0.00 }
  json_set['Events'].extend(IV_Quarantine(pdict))


  # PPE for HCW
  pdict = {'startday':                                     20 ,
           'coverage':                                   1.00 ,
           'qual_acq':                      params['HCW_PPE'] ,
           'qual_trn':                      params['HCW_PPE'] ,
           'group_names': [{'Restrictions':
                                         ['Geographic:HCW']}] }
  json_set['Events'].extend(IV_MultiEffect(pdict))


  # Tour for HCW
  if('HCW_Walk' in params and params['HCW_Walk']):
    for k1 in range(params['HCW_Walk_Start'],params['HCW_Walk_End']):
      for k2 in range(5):
        pdict = {'startday':                                         k1 ,
                 'node_dest':  np.random.randint(2,params['num_nodes']) ,
                 'duration':                                          2 ,
                 'fraction':                         params['HCW_Frac'] ,
                 'group_names':       [{'Restrictions':
                                                   ['Geographic:HCW']}] }
        json_set['Events'].extend(IV_TakeAWalk(pdict))

  # Tour for Bob
  if('Bob_Walk' in params and params['Bob_Walk']):
    for k1 in range(params['Bob_Walk_Start'],params['Bob_Walk_End']):
      for k2 in range(5):
        pdict = {'startday':                                         k1 ,
                 'node_dest':  np.random.randint(2,params['num_nodes']) ,
                 'duration':                                          1 ,
                 'fraction':                         params['Bob_Frac'] ,
                 'group_names':       [{'Restrictions':
                                          ['Geographic:age25_riskMD']}] }
        json_set['Events'].extend(IV_TakeAWalk(pdict))

  # Age-dependent susceptibility
  pdict = {'startday':                                     10 ,
           'coverage':                                   1.00 ,
           'qual_acq':            params['age_effect_a']*0.95 ,
           'qual_trn':            params['age_effect_t']*0.95 ,
           'group_names':     [{'Restrictions':
                                ['Geographic:age00_riskLO']},
                               {'Restrictions':
                                ['Geographic:age00_riskMD']},
                               {'Restrictions':
                                ['Geographic:age00_riskHI']}] }
  json_set['Events'].extend(IV_MultiEffect(pdict))

  pdict = {'startday':                                     11 ,
           'coverage':                                   1.00 ,
           'qual_acq':            params['age_effect_a']*0.75 ,
           'qual_trn':            params['age_effect_t']*0.75 ,
           'group_names':     [{'Restrictions':
                                ['Geographic:age05_riskLO']},
                               {'Restrictions':
                                ['Geographic:age05_riskMD']},
                               {'Restrictions':
                                ['Geographic:age05_riskHI']}] }
  json_set['Events'].extend(IV_MultiEffect(pdict))

  pdict = {'startday':                                     12 ,
           'coverage':                                   1.00 ,
           'qual_acq':            params['age_effect_a']*0.60 ,
           'qual_trn':            params['age_effect_t']*0.60 ,
           'group_names':     [{'Restrictions':
                                ['Geographic:age10_riskLO']},
                               {'Restrictions':
                                ['Geographic:age10_riskMD']},
                               {'Restrictions':
                                ['Geographic:age10_riskHI']}] }
  json_set['Events'].extend(IV_MultiEffect(pdict))

  pdict = {'startday':                                     13 ,
           'coverage':                                   1.00 ,
           'qual_acq':            params['age_effect_a']*0.35 ,
           'qual_trn':            params['age_effect_t']*0.35 ,
           'group_names':     [{'Restrictions':
                                ['Geographic:age15_riskLO']},
                               {'Restrictions':
                                ['Geographic:age15_riskMD']},
                               {'Restrictions':
                                ['Geographic:age15_riskHI']}] }
  json_set['Events'].extend(IV_MultiEffect(pdict))


  # Active case finding
  pdict = {'trigger':                          'NewInfection' ,
           'startday':     params['active_finding_start_day'] ,
           'coverage':      params['active_finding_coverage'] ,
           'quality':  params['active_finding_effectiveness'] ,
           'delay':       2.00+params['active_finding_delay'] }
  json_set['Events'].extend(IV_Quarantine(pdict))


  #  ***** End file construction *****
  with open('campaign.json','w') as fid01:
    json.dump(json_set,fid01,sort_keys=True)


# end-campaignBuilder

#********************************************************************************

# Event observer
def IV_Quarantine(params=dict()):

  IVlist = list()

  IVdic = { 'class':                              'CampaignEvent' ,
             'Nodeset_Config':          { 'class': 'NodeSetAll' } ,
             'Start_Day':              120*365+params['startday'] ,
             'Event_Coordinator_Config':
             { 'class':   'CommunityHealthWorkerEventCoordinator' ,
               'Demographic_Coverage':                        1.0 ,
               'Target_Residents_Only':                         0 ,
               'Duration':                                   1000 ,
               'Max_Distributed_Per_Day':                     1e9 ,
               'Waiting_Period':                           1000.0 ,
               'Days_Between_Shipments':                     1000 ,
               'Amount_In_Shipment':                            0 ,
               'Max_Stock':                                   1e9 ,
               'Initial_Amount_Distribution':
                                          'CONSTANT_DISTRIBUTION' ,
               'Initial_Amount_Constant':                     1e9 ,
               'Target_Demographic':                   'Everyone' ,
               'Trigger_Condition_List':    [ params['trigger'] ] ,
               'Intervention_Config':
               { 'class':                               'Vaccine' ,
                 'Event_Trigger_Distributed':         'NoTrigger' ,
                 'Event_Trigger_Expired':             'NoTrigger' ,
                 'Dont_Allow_Duplicates':                       0 ,
                 'Cost_To_Consumer':                          0.0 ,
                 'Take_Reduced_By_Acquire_Immunity':          0.0 ,
                 'Intervention_Name':           'Self_Quarantine' ,
                 'Efficacy_Is_Multiplicative':                  1 ,
                 'Disqualifying_Properties':                   [] ,
                 'New_Property_Value':                         '' ,
                 'Vaccine_Take':               params['coverage'] ,
                 'Take_By_Age_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Initial_Acquire_By_Current_Effect_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Initial_Mortality_By_Current_Effect_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Initial_Transmit_By_Current_Effect_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Acquire_Config':
                 {
                   'class':                    'WaningEffectNull'
                 },
                 'Mortality_Config':
                 {
                   'class':                    'WaningEffectNull'
                 },
                 'Transmit_Config':
                 {
                   'class':            'WaningEffectMapPiecewise' ,
                   'Initial_Effect':                          1.0 ,
                   'Reference_Timer':                         0.0 ,
                   'Expire_At_Durability_Map_End':              0 ,
                   'Durability_Map':
                   {
                     'Times':        [ 0.0, 1.0+params['delay'] ] ,
                     'Values':       [ 0.0,     params['quality'] ]
                   }
                 }
               }
             }
           }

  IVlist.append(IVdic)

  return IVlist

#********************************************************************************

# Add protection
def IV_MultiEffect(params=dict()):

  IVlist = list()

  IVdic = {
             'class':                              'CampaignEvent' ,
             'Nodeset_Config':          { 'class': 'NodeSetAll' } ,
             'Start_Day':              120*365+params['startday'] ,
             'Event_Coordinator_Config':
             {
               'class':
               'StandardInterventionDistributionEventCoordinator' ,
               'Demographic_Coverage':                        1.0 ,
               'Property_Restrictions_Within_Node':
                                            params['group_names'] ,
               'Number_Repetitions':                            1 ,
               'Timesteps_Between_Repetitions':                 0 ,
               'Target_Demographic':                   'Everyone' ,
               'Target_Residents_Only':                         0 ,
               'Intervention_Config':
               {
                 'class':                               'Vaccine' ,
                 'Event_Trigger_Distributed':         'NoTrigger' ,
                 'Event_Trigger_Expired':             'NoTrigger' ,
                 'Dont_Allow_Duplicates':                       0 ,
                 'Cost_To_Consumer':                          0.0 ,
                 'Take_Reduced_By_Acquire_Immunity':          0.0 ,
                 'Intervention_Name':                       'IPC' ,
                 'Efficacy_Is_Multiplicative':                  1 ,
                 'Disqualifying_Properties':                   [] ,
                 'New_Property_Value':                         '' ,
                 'Vaccine_Take':               params['coverage'] ,
                 'Take_By_Age_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Initial_Acquire_By_Current_Effect_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Initial_Mortality_By_Current_Effect_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Initial_Transmit_By_Current_Effect_Multiplier':
                 {
                   'Times':                               [ 0.0 ] ,
                   'Values':                              [ 1.0 ]
                 },
                 'Acquire_Config':
                 {
                   'class':                'WaningEffectConstant' ,
                   'Initial_Effect':           params['qual_acq'] 
                 },
                 'Mortality_Config':
                 {
                   'class':                'WaningEffectConstant' ,
                   'Initial_Effect':                         1.00 
                 },
                 'Transmit_Config':
                 {
                   'class':                'WaningEffectConstant' ,
                   'Initial_Effect':           params['qual_trn'] 
                 }
               }
             }
           }

  IVlist.append(IVdic)

  return IVlist

#********************************************************************************

# Contagion import
def IV_ImportPressure(params=dict()):

  IVlist = list()

  IVdic = {
             'class':                             'CampaignEvent' ,
             'Nodeset_Config':      { 'class': 'NodeSetNodeList',
                                      'Node_List':          [1] } ,
             'Start_Day':              120*365+params['startday'] ,
             'Event_Coordinator_Config':
             {
               'class':
               'StandardInterventionDistributionEventCoordinator' ,
               'Demographic_Coverage':                        1.0 ,
               'Number_Repetitions':                            1 ,
               'Timesteps_Between_Repetitions':                 0 ,
               'Target_Demographic':                   'Everyone' ,
               'Target_Residents_Only':                         0 ,
               'Intervention_Config':
               {
                 'class':                        'ImportPressure' ,
                 'Clade':                                       0 ,
                 'Genome':                                      0 ,
                 'Number_Cases_Per_Node':                       0 ,
                 'Durations':                [params['duration']] ,
                 'Import_Age':                              12775 ,
                 'Import_Agent_MC_Weight':                    1.0 ,
                 'Import_Female_Prob':                        0.5 ,
                 'Daily_Import_Pressures':     [params['amount']]
               }
             }
           }
    
  IVlist.append(IVdic)

  return IVlist

#********************************************************************************

# HINT revision
def IV_MatrixSwap(params=dict()):

  IVlist = list()

  if(params['only_urb']):
    nodsetdic = { 'class': 'NodeSetNodeList',
                  'Node_List': [1] }
  elif(params['only_rur']):
    nodsetdic = { 'class': 'NodeSetNodeList',
                  'Node_List': list(range(2,params['num_nodes']+1)) }
  else:
    nodsetdic = { 'class': 'NodeSetAll' }

  IVdic = {
             'class':                             'CampaignEvent' ,
             'Nodeset_Config':                          nodsetdic ,
             'Start_Day':              120*365+params['startday'] ,
             'Event_Coordinator_Config':
             {
               'class':
               'StandardInterventionDistributionEventCoordinator' ,
               'Demographic_Coverage':                        1.0 ,
               'Number_Repetitions':                            1 ,
               'Timesteps_Between_Repetitions':                 0 ,
               'Target_Demographic':                   'Everyone' ,
               'Target_Residents_Only':                         0 ,
               'Intervention_Config':
               {
                 'class':                        'ChangeIPMatrix' ,
                 'Property_Name':                    'Geographic' ,
                 'New_Matrix':        params['matblock'].tolist()
               }
             }
           }
    
  IVlist.append(IVdic)

  return IVlist

#********************************************************************************

# HINT revision
def IV_TakeAWalk(params=dict()):

  IVlist = list()

  IVdic = {
             'class':                             'CampaignEvent' ,
             'Nodeset_Config':      { 'class': 'NodeSetNodeList',
                                      'Node_List':          [1] } ,
             'Start_Day':              120*365+params['startday'] ,
             'Event_Coordinator_Config':
             {
               'class':
               'StandardInterventionDistributionEventCoordinator' ,
               'Demographic_Coverage':         params['fraction'] ,
               'Property_Restrictions_Within_Node':
                                            params['group_names'] ,
               'Number_Repetitions':                            1 ,
               'Timesteps_Between_Repetitions':                 0 ,
               'Target_Demographic':                   'Everyone' ,
               'Target_Residents_Only':                         0 ,
               'Intervention_Config':
               {
                 'class':                    'MigrateIndividuals' ,
                 'Intervention_Name':             'COMMENT_FIELD' ,
                 'Disqualifying_Properties':                   [] ,
                 'New_Property_Value':                         '' ,
                 'NodeID_To_Migrate_To':      params['node_dest'] ,
                 'Dont_Allow_Duplicates':                       1 ,
                 'Duration_Before_Leaving_Distribution':
                                          'CONSTANT_DISTRIBUTION' ,
                 'Duration_At_Node_Distribution':
                                          'CONSTANT_DISTRIBUTION' ,
                 'Is_Moving':                                   0 ,
                 'Duration_Before_Leaving_Constant':            0 ,
                 'Duration_At_Node_Constant':  params['duration']
               }
             }
           }
    
  IVlist.append(IVdic)

  return IVlist

#********************************************************************************