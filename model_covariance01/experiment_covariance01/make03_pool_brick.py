# *****************************************************************************
#
# *****************************************************************************

import json
import os
import sys

from idmtools.core.id_file import read_id_file

# Ought to go in emodpy
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'local_python')))
from py_assets_common.emod_constants import D_FILE

# *****************************************************************************


def get_data_brick():

    # Iterate
    data_brick = dict()
    suite_id = '633a1f31-ba49-44a5-9792-8aaf2363926f'
    ed = os.path.join('docker_test01', suite_id)
    for sdir1 in os.listdir(ed):
        sjdir1 = os.path.join(ed, sdir1)
        if (os.path.isdir(sjdir1)):
            for sdir2 in os.listdir(sjdir1):
                sjdir2 = os.path.join(ed, sdir1, sdir2)
                if (os.path.isdir(sjdir2)):
                    tfile = os.path.join(ed, sdir1, sdir2, 'parsed_out.json')
                    if (os.path.exists(tfile)):
                        with open(tfile) as fid01:
                            pdata = json.load(fid01)
                        data_brick.update(pdata)

    # Reduce output and write data brick
    with open(D_FILE, 'w') as fid01:
        json.dump(data_brick, fid01)

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    get_data_brick()

# *****************************************************************************
