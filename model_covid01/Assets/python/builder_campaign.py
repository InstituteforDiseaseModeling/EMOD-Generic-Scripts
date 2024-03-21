# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import global_data as gdata

import emod_api.campaign as camp_module

from aux_matrix_calc import mat_magic

from emod_camp_events import ce_import_pressure, ce_vax_AMT, ce_quarantine, \
                             ce_matrix_swap
from emod_constants import CAMP_FILE

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

    AGE_ACQ = gdata.var_params['age_effect_a']
    AGE_TRN = gdata.var_params['age_effect_t']

    HCW_PPE = gdata.var_params['HCW_PPE']

    # Rural visits by HCW not currently used
    # HCW_WALK = gdata.var_params['HCW_Walk']
    # HCW_FRAC = gdata.var_params['HCW_Frac']
    # HCW_START = gdata.var_params['HCW_Walk_Start']
    # HCW_END = gdata.var_params['HCW_Walk_End']

    # Rural visits by volunteers not currently used
    # BOB_WALK = gdata.var_params['Bob_Walk']
    # BOB_FRAC = gdata.var_params['Bob_Frac']
    # BOB_START = gdata.var_params['Bob_Walk_Start']
    # BOB_END = gdata.var_params['Bob_Walk_End']

    # Active case finding; not currently used
    # AF_START = gdata.var_params['active_finding_start_day']
    # AF_COVER = gdata.var_params['active_finding_coverage']
    # AF_QUAL = gdata.var_params['active_finding_effectiveness']
    # AF_DELAY = gdata.var_params['active_finding_delay']

    # Note: campaign module itself is the file object; no Campaign class
    ALL_NODES = list(range(1, NUM_NODES+1))

    # Contact pattern revisions
    for k1 in range(1, 999):
        tmat_key = 'trans_mat{:02d}'.format(k1)
        tday_key = 'start_mat{:02d}'.format(k1)

        if (tmat_key not in gdata.var_params):
            break

        arg_dist = gdata.var_params[tmat_key]
        day_start = gdata.var_params[tday_key]
        mat_spike = False
        mat_nudge = False
        hce_h2h = False

        (_, _, numpy_mat) = mat_magic(CTEXT_VAL, arg_dist,
                                      mat_spike, mat_nudge, hce_h2h)

        mlist = numpy_mat.tolist()
        itime = 120*365 + day_start
        camp_event = ce_matrix_swap(ALL_NODES, PROP, mlist, start_day=itime)
        camp_module.add(camp_event)

    # PPE for HCW
    itime = 120*365 + 20
    camp_event = ce_vax_AMT(ALL_NODES, start_day=itime, only_group=HCW_GROUP,
                            acq_eff=HCW_PPE, trn_eff=HCW_PPE)
    camp_module.add(camp_event)

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
    # itime = 120*365 + AF_START
    # camp_event = ce_quarantine(ALL_NODES, 'NewInfection',
    #                            start_day=itime, coverage=AF_COVER,
    #                            delay=3.0+AF_DELAY, effect=AF_QUAL)
    # camp_module.add(camp_event)

    # Outreach for HCW
    # if (HCW_WALK):
    #     len_visit = 2
    #     node_orig = 1
    #     for t_val in range(HCW_START, HCW_END, len_visit):
    #         itime = 120*365 + t_val
    #         for k2 in range(5):
    #             node_dest = np.random.randint(2, NUM_NODES)
    #             camp_event = ce_visit_nodes(node_orig, node_dest,
    #                                         start_day=itime,
    #                                         only_group=HCW_GROUP,
    #                                         fraction=HCW_FRAC,
    #                                         duration=len_visit)
    #             camp_module.add(camp_event)

    # Outreach for volunteers
    # if (BOB_WALK):
    #     len_visit = 2
    #     node_orig = 1
    #     for t_val in range(BOB_START, BOB_END, len_visit):
    #         itime = 120*365 + t_val
    #         for k2 in range(5):
    #             node_dest = np.random.randint(2, NUM_NODES)
    #             camp_event = ce_visit_nodes(node_orig, node_dest,
    #                                         start_day=itime,
    #                                         only_group=BOB_FRAC,
    #                                         fraction=BOB_GROUP,
    #                                         duration=len_visit)
    #             camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************
