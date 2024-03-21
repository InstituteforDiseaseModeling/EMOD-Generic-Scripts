# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import global_data as gdata

import emod_api.campaign as camp_module

from aux_matrix_calc import mat_magic

import numpy as np

from emod_api import schema_to_class as s2c
from emod_api.interventions import utils

from emod_camp_events import ce_import_pressure, ce_vax_AMT, ce_quarantine, \
                             ce_matrix_swap

# *****************************************************************************

PROP = 'Geographic'

HCW_GROUP = [{'Restrictions': ['Geographic:HCW']}]
BOB_GROUP = [{'Restrictions': ['Geographic:age25_riskMD']}]

AGE00_GRP = [{'Restrictions': ['Geographic:age00_riskLO']},
             {'Restrictions': ['Geographic:age00_riskMD']},
             {'Restrictions': ['Geographic:age00_riskHI']}]

AGE05_GRP = [{'Restrictions': ['Geographic:age05_riskLO']},
             {'Restrictions': ['Geographic:age05_riskMD']},
             {'Restrictions': ['Geographic:age05_riskHI']}]

AGE10_GRP = [{'Restrictions': ['Geographic:age10_riskLO']},
             {'Restrictions': ['Geographic:age10_riskMD']},
             {'Restrictions': ['Geographic:age10_riskHI']}]

AGE15_GRP = [{'Restrictions': ['Geographic:age15_riskLO']},
             {'Restrictions': ['Geographic:age15_riskMD']},
             {'Restrictions': ['Geographic:age15_riskHI']}]

# *****************************************************************************


def campaignBuilder():

    # Variables for this simulation
    CTEXT_VAL = gdata.var_params['ctext_val']
    NUM_NODES = gdata.var_params['num_nodes']

    SIOS_FRAC = gdata.var_params['self_isolate_on_symp_frac']
    SIOS_EFFECT = gdata.var_params['self_isolate_effectiveness']

    IP_START = gdata.var_params['importations_start_day']
    IP_DURATION = gdata.var_params['importations_duration']
    IP_RATE = gdata.var_params['importations_daily_rate']

    HCW_PPE = gdata.var_params['HCW_PPE']
    HCW_WALK = gdata.var_params['HCW_Walk']
    HCW_FRAC = 0.1
    HCW_START = gdata.var_params['HCW_Walk_Start']
    HCW_END = gdata.var_params['HCW_Walk_End']

    BOB_WALK = gdata.var_params['Bob_Walk']
    BOB_FRAC = gdata.var_params['Bob_Frac']
    BOB_START = gdata.var_params['Bob_Walk_Start']
    BOB_END = gdata.var_params['Bob_Walk_End']

    AGE_ACQ = gdata.var_params['age_effect_a']
    AGE_TRN = gdata.var_params['age_effect_t']

    AF_START = gdata.var_params['active_finding_start_day']
    AF_COVER = gdata.var_params['active_finding_coverage']
    AF_QUAL = gdata.var_params['active_finding_effectiveness']
    AF_DELAY = gdata.var_params['active_finding_delay']

    # Note: campaign module itself is the file object; no Campaign class
    ALL_NODES = list(range(1, NUM_NODES+1))
    CAMP_FILE = gdata.camp_file

    TRANS_RANGE  = range(2,14)

    DICT_TRANS   = {k1: gdata.var_params[          'trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}
    DICT_SPIKE   = {k1: gdata.var_params[    'spike_trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}
    DICT_NUDGE   = {k1: gdata.var_params[    'nudge_trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}
    DICT_H2H     = {k1: gdata.var_params[      'household_sia{:02d}'.format(k1)] for k1 in TRANS_RANGE}
    DICT_START   = {k1: gdata.var_params['start_day_trans_mat{:02d}'.format(k1)] for k1 in TRANS_RANGE}

    # Contact pattern revision
    for k1 in TRANS_RANGE:
        pdict = {'arg_dist':               DICT_TRANS[k1] ,
                 'spike_mat':              DICT_SPIKE[k1] ,
                 'nudge_mat':              DICT_NUDGE[k1] ,
                 'hcw_h2h':                  DICT_H2H[k1] ,
                 'ctext_val':                   CTEXT_VAL }

        (_, _, numpy_mat) = mat_magic(pdict)
        mlist = numpy_mat.tolist()
        itime = 120*365 + DICT_START[k1]
        camp_event = ce_matrix_swap(ALL_NODES, PROP, mlist, start_day=itime)
        camp_module.add(camp_event)

    # PPE for HCW
    itime = 120*365 + 20
    camp_event = ce_vax_AMT(ALL_NODES, start_day=itime, only_group=HCW_GROUP,
                            acq_eff=HCW_PPE, trn_eff=HCW_PPE)
    camp_module.add(camp_event)

    # Tour for HCW
    if (HCW_WALK):
        for k1 in range(HCW_START,HCW_END):
            for k2 in range(5):
                pdict = {'startday': k1,
                         'node_dest': np.random.randint(2,NUM_NODES),
                         'duration': 2,
                         'fraction': HCW_FRAC,
                         'group_names': HCW_GROUP}
                camp_module.add(IV_TakeAWalk(pdict))

    # Tour for Bob
    if (BOB_WALK):
        for k1 in range(BOB_START,BOB_END):
            for k2 in range(5):
                pdict = {'startday': k1,
                         'node_dest': np.random.randint(2,NUM_NODES),
                         'duration': 1,
                         'fraction': BOB_FRAC,
                         'group_names': BOB_GROUP}
                camp_module.add(IV_TakeAWalk(pdict))

    # Infection importation
    nlist = [1]
    itime = 120*365 + IP_START
    camp_event = ce_import_pressure(nlist, start_day=itime, age_yrs=35.0,
                                    duration=IP_DURATION, magnitude=IP_RATE)
    camp_module.add(camp_event)

    # Age-dependent susceptibility
    itime = 120*365 + 10
    e_frac = 0.95
    camp_event = ce_vax_AMT(ALL_NODES, start_day=itime, only_group=AGE00_GRP,
                            acq_eff=e_frac*AGE_ACQ, trn_eff=e_frac*AGE_TRN)
    camp_module.add(camp_event)

    itime = 120*365 + 11
    e_frac = 0.75
    camp_event = ce_vax_AMT(ALL_NODES, start_day=itime, only_group=AGE05_GRP,
                            acq_eff=e_frac*AGE_ACQ, trn_eff=e_frac*AGE_TRN)
    camp_module.add(camp_event)

    itime = 120*365 + 12
    e_frac = 0.60
    camp_event = ce_vax_AMT(ALL_NODES, start_day=itime, only_group=AGE10_GRP,
                            acq_eff=e_frac*AGE_ACQ, trn_eff=e_frac*AGE_TRN)
    camp_module.add(camp_event)

    itime = 120*365 + 13
    e_frac = 0.35
    camp_event = ce_vax_AMT(ALL_NODES, start_day=itime, only_group=AGE15_GRP,
                            acq_eff=e_frac*AGE_ACQ, trn_eff=e_frac*AGE_TRN)
    camp_module.add(camp_event)

    # Self-quarantine
    itime = 120*365 + 15
    camp_event = ce_quarantine(ALL_NODES, 'NewlySymptomatic',
                               start_day=itime, coverage=SIOS_FRAC,
                               delay=1.0, effect=SIOS_EFFECT)
    camp_module.add(camp_event)

    # Active case finding
    itime = 120*365 + AF_START
    camp_event = ce_quarantine(ALL_NODES, 'NewInfection',
                               start_day=itime, coverage=AF_COVER,
                               delay=3.0+AF_DELAY, effect=AF_QUAL)
    camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************

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