# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import global_data as gdata

import numpy as np

import emod_api.campaign as camp_module

from builder_demographics import br_force_xval, br_force_yval

from emod_camp_events import ce_br_force
from emod_constants import CAMP_FILE

# *****************************************************************************


def campaignBuilder():

    # Variables for this simulation
    USE_BR_FORCE = gdata.var_params['variable_birthrate']

    # Note: campaign module itself is the file object; no Campaign class
    ALL_NODES = gdata.demog_object.node_ids

    # Time varying birth rate
    start_day = 365.0*(gdata.start_year-gdata.base_year)
    xval = np.array(br_force_xval)*365.0
    yval = np.array(br_force_yval)

    if (not USE_BR_FORCE):
        yval = 1.0 + 0.0*yval

    camp_event = ce_br_force(ALL_NODES, xval.tolist(), yval.tolist(), start_day)
    camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************
