# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import global_data as gdata

import emod_api.campaign as camp_module

from emod_camp_events import ce_br_force

# *****************************************************************************


def campaignBuilder():

    # Variables for this simulation
    START_YEAR = gdata.var_params['start_year']

    # Note: campaign module itself is the file object; no Campaign class
    ALL_NODES = gdata.demog_object.node_ids
    CAMP_FILE = gdata.camp_file

    # Add time varying birth rate
    BASE_YEAR = gdata.base_year
    BR_MULT_X = gdata.brate_mult_x
    BR_MULT_Y = gdata.brate_mult_y
    start_day = 365.0*(START_YEAR-BASE_YEAR)
    camp_event = ce_br_force(ALL_NODES, BR_MULT_X, BR_MULT_Y, start_day)
    camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************
