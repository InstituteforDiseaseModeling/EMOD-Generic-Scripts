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

from emod_camp_events import ce_outbreak, ce_OPV_SIA
from emod_constants import CAMP_FILE

# *****************************************************************************


def campaignBuilder():

    # Variables for this simulation
    TIME_START = gdata.var_params['start_time']
    SIA_CALENDAR = gdata.var_params['sia_calendar']
    SIA_STOP = gdata.var_params['sia_cutoff']
    SIA_ADDLIST = gdata.var_params['sia_sets']
    NODE_DICT = gdata.demog_node

    node_opts = list(NODE_DICT.keys())

    # Use SIA calendar for OPV2 schedule
    if (SIA_CALENDAR):
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
                    if ((node_name == targ_val) or
                       (node_name.startswith(targ_val+':'))):
                        node_list.append(NODE_DICT[node_name])

            camp_event = ce_OPV_SIA(node_list, start_day=startday,
                                    coverage=gdata.sia_coverage,
                                    clade=clade, genome=genome)
            camp_module.add(camp_event)

    # Use custom spec for intervention schedule
    for sia_obj in SIA_ADDLIST:
        node_list = list()
        node_name_list = list()
        for targ_val in sia_obj['targ_list']:
            for node_name in node_opts:
                if ((node_name == targ_val) or
                   (node_name.startswith(targ_val+':'))):
                    node_list.append(NODE_DICT[node_name])
                    node_name_list.append(node_name)

        # Preserve size of outbreak; select random single node for location
        node_list = [node_list[np.random.randint(low=0, high=len(node_list))]]
        startday = gdata.start_off + TIME_START + sia_obj['day_offset']

        camp_event = ce_outbreak(node_list, start_day=startday,
                                 num_cases=sia_obj['num_cases'],
                                 genome=gdata.boxes_nopv2+gdata.boxes_sabin2)
        camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************
