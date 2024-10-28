# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import json
import os

import global_data as gdata

import numpy as np

import emod_api.campaign as camp_module

from emod_camp_events import ce_br_force
from emod_constants import CAMP_FILE

from emod_api import schema_to_class as s2c
from emod_api.interventions   import utils

#********************************************************************************


def campaignBuilder():

    # Variables for this simulation
    TIME_START   = gdata.var_params['start_time']

    SIA_CALENDAR = gdata.var_params['sia_calendar']
    SIA_COVERAGE = gdata.var_params['sia_coverage']
    SIA_STOP = gdata.var_params['sia_cutoff']

    SIA_ADDLIST  = gdata.var_params['sia_sets']

    NODE_DICT    = gdata.demog_node

    node_opts = list(NODE_DICT.keys())
    node_dict_inv = {NODE_DICT[nname_val]:nname_val for nname_val in NODE_DICT}

    # Use SIA calendar for OPV2 schedule
    if(SIA_CALENDAR):
        with open(os.path.join('Assets', 'data', 'sia_dat_NGA.json')) as fid01:
            dict_sia = json.load(fid01)

        for sia_name in dict_sia:
            sia_obj = dict_sia[sia_name]

            startday = sia_obj['date']
            if (startday > SIA_STOP):
                continue

            if (sia_obj['type'] == 'sabin2'):
                clade = 0
                genome = gdata.boxes_nopv2
            elif (sia_obj['type'] == 'nopv2'):
                clade = 1
                genome = 0

            node_list = list()
            for targ_val in sia_obj['nodes']:
                for node_name in node_opts:
                    if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
                        node_list.append(NODE_DICT[node_name])

            pdict = {'startday': startday,
                     'nodes': node_list,
                     'coverage': SIA_COVERAGE,
                     'clade': clade,
                     'genome': genome}

            camp_module.add(IV_OPV2(pdict))

    # Use custom spec for intervention schedule
    for sia_obj in SIA_ADDLIST:
        node_list      = list()
        node_name_list = list()
        for targ_val in sia_obj['targ_list']:
            for node_name in node_opts:
                if((node_name == targ_val) or (node_name.startswith(targ_val+':'))):
                    node_list.append(NODE_DICT[node_name])
                    node_name_list.append(node_name)

        # Set time of intervention
        startday  = gdata.start_off + TIME_START + sia_obj['day_offset']

        # Create and add intervention
        # Preserve size of outbreak; select random single node for location
        node_list = [node_list[np.random.randint(low=0, high=len(node_list))]]
        pdict = {'startday': startday,
                 'nodes': node_list,
                 'num_cases': sia_obj['num_cases'],
                 'genome': gdata.boxes_nopv2+gdata.boxes_sabin2 }
        camp_module.add(IV_cVDPV2(pdict))

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

#********************************************************************************


# Distribute vaccines using OutbreakIndividual infections
def IV_OPV2(params):

    SCHEMA_PATH   =  gdata.schema_path

    camp_event = s2c.get_class_with_defaults('CampaignEvent', SCHEMA_PATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SCHEMA_PATH)
    camp_iv = s2c.get_class_with_defaults('OutbreakIndividual', SCHEMA_PATH)

    node_set = utils.do_nodes(SCHEMA_PATH, params['nodes'])

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = params['startday']
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv
    camp_coord.Demographic_Coverage = params['coverage']
    camp_coord.Target_Demographic = 'ExplicitAgeRanges'
    camp_coord.Target_Age_Min = 0.75
    camp_coord.Target_Age_Max = 5.00

    camp_iv.Clade = params['clade']
    camp_iv.Genome = params['genome']
    camp_iv.Ignore_Immunity = 0
    camp_iv.Cost_To_Consumer = 1.0

    return camp_event

#********************************************************************************


# Distribute seed infections using Oubreak
def IV_cVDPV2(params):

    SCHEMA_PATH   =  gdata.schema_path

    camp_event = s2c.get_class_with_defaults('CampaignEvent', SCHEMA_PATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SCHEMA_PATH)
    camp_iv    = s2c.get_class_with_defaults('Outbreak', SCHEMA_PATH)

    node_set   = utils.do_nodes(SCHEMA_PATH, params['nodes'])

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = params['startday']
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config            = camp_iv

    camp_iv.Genome = params['genome']
    camp_iv.Number_Cases_Per_Node = params['num_cases']
    camp_iv.Import_Age = 7300.0
    camp_iv.Import_Female_Prob = 0.0
    camp_iv.Import_Agent_MC_Weight = 1.0

    return camp_event

#********************************************************************************