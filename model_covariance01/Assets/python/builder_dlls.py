# *****************************************************************************
#
# Configuration file for custom reporters.
#
# *****************************************************************************

import json

import global_data as gdata

# *****************************************************************************


def dllcBuilder():

    REPORTS_FILENAME = gdata.reports_file

    # Get variables for this simulation
    # N/A

    # Dictionary to be written
    json_set = dict()

    # Custom reports object
    json_set['Custom_Reports'] = dict()

    # Configurations
    # N/A

    #  Write file
    with open(REPORTS_FILENAME, 'w') as fid01:
        json.dump(json_set, fid01, sort_keys=True, indent=4)

    return None

# *****************************************************************************
