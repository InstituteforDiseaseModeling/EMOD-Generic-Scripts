# *****************************************************************************
#
# *****************************************************************************

import global_data as gdata

from emod_api import schema_to_class as s2c
from emod_api.interventions import utils

from emod_constants import YR_DAYS

# *****************************************************************************


def ce_import_pressure(node_list,
                       start_day=0.0, duration=1.0,
                       magnitude=1.0, age_yrs=40.0):

    SPATH = gdata.schema_path

    # Import pressure
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SPATH)
    camp_iv = s2c.get_class_with_defaults('ImportPressure', SPATH)

    node_set = utils.do_nodes(SPATH, node_list)

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv

    camp_iv.Durations = [duration]
    camp_iv.Daily_Import_Pressures = [magnitude]
    camp_iv.Import_Age = age_yrs*YR_DAYS

    return camp_event

# *****************************************************************************
