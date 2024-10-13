# *****************************************************************************
#
# Configuration file for custom reporters.
#
# *****************************************************************************

import json

from emod_constants import REPORTS_FILE, RST_FILE

# *****************************************************************************


def dllcBuilder():

    # Get variables for this simulation
    # N/A

    # Dictionary to be written
    json_set = dict()

    # Custom reports object
    cr_str = 'Custom_Reports'
    json_set[cr_str] = dict()

    # Strain reporting
    rst_str = RST_FILE.split('.')[0]
    json_set[cr_str][rst_str] = {'Enabled': 1,
                                 'Reports': list()}

    repDic = {'Report_Name': RST_FILE}

    json_set[cr_str][rst_str]['Reports'].append(repDic)

    #  Write file
    with open(REPORTS_FILE, 'w') as fid01:
        json.dump(json_set, fid01, sort_keys=True, indent=4)

    return None

# *****************************************************************************
