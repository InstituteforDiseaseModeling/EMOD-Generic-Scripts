# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import global_data as gdata

import emod_api.campaign as camp_module

from emod_camp_events import ce_br_force
from emod_constants import CAMP_FILE

# *****************************************************************************


def campaignBuilder():

    # Variables for this simulation
    USE_BR_FORCE = gdata.var_params['variable_birthrate']

    # Note: campaign module itself is the file object; no Campaign class
    ALL_NODES = gdata.demog_object.node_ids

    # Time varying birth rate
    BR_MULT_X = gdata.brate_mult_x
    BR_MULT_Y = gdata.brate_mult_y
    start_day = 365.0*(gdata.start_year-gdata.base_year)

    if (not USE_BR_FORCE):
        BR_MULT_Y = len(BR_MULT_Y)*[1.0]

    camp_event = ce_br_force(ALL_NODES, BR_MULT_X, BR_MULT_Y, start_day)
    camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************
