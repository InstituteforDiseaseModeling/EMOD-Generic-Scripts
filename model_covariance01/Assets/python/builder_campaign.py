# *****************************************************************************
#
# Campaign file.
#
# *****************************************************************************

import global_data as gdata

import emod_api.campaign as camp_module

from emod_camp_events import ce_import_pressure

# *****************************************************************************


def campaignBuilder():

    # Variables for this simulation
    # N/A

    # Note: campaign module itself is the file object; no Campaign class
    ALL_NODES = gdata.demog_object.node_ids
    CAMP_FILE = gdata.camp_file

    # Events
    camp_event = ce_import_pressure(ALL_NODES, duration=5.0)
    camp_module.add(camp_event)

    # End file construction
    camp_module.save(filename=CAMP_FILE)

    return None

# *****************************************************************************
