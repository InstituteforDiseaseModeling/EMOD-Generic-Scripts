# *****************************************************************************
#
# *****************************************************************************

import json
import os

from multiprocessing import Pool

from idmtools.core.id_file import read_id_file
from idmtools.core.platform_factory import Platform
from idmtools.assets import Asset
from idmtools_models.python.python_task import PythonTask
from idmtools_platform_comps.ssmt_work_items.comps_workitems \
                                        import SSMTWorkItem

from COMPS import Client
from COMPS.Data import Experiment
from COMPS.Data.Simulation import SimulationState

# *****************************************************************************

DOCK_PACK = r'docker-production-public.packages.idmod.org/emodpy/'
DOCK_PACK = DOCK_PACK + r'comps_ssmt_worker:latest'

PARAM_DICT = 'param_dict.json'
DATA_BRICK = 'data_brick.json'
FILENAME_PY = 'emod_reduce.py'
FILENAME_ID = 'COMPS_ID.id'
COMPS_URL = 'https://comps.idmod.org'

ID_OS = 'EMOD_OS.id'
ID_EXE = 'EMOD_EXE.id'
ID_ENV = 'EMOD_ENV.id'
ID_SCHEMA = 'EMOD_SCHEMA.id'

VE_PY_PATHS = ['/py_env/lib/python3.9/site-packages/',
               '/py_env/lib/python3.10/site-packages/',
               '/py_env/lib/python3.11/site-packages/',
               '/py_env/lib/python3.12/site-packages/']

# *****************************************************************************


def getter_worker(sim):

    Client.login(COMPS_URL)

    sim_obj = sim.retrieve_output_file_info(None)
    ret_val = None

    for file_info in sim_obj:
        if (file_info.friendly_name == 'parsed_out.json'):
            file_bytes = sim.retrieve_output_files_from_info([file_info])
            ret_val = file_bytes[0].decode()

    return ret_val

# *****************************************************************************


# Runs on cluster
def pool_manager(exp_id=None):

    Client.login(COMPS_URL)

    if (not exp_id):
        (exp_id, _, _, _) = read_id_file(os.path.join('Assets', FILENAME_ID))
        exp_obj = Experiment.get(exp_id)
        sims_all = exp_obj.get_simulations()
        sims_valid = [s for s in sims_all if s.state.value >=
                      SimulationState.Commissioned.value]

    with Pool() as pool_obj:
        resp_list = pool_obj.map(getter_worker, sims_valid)

    merged_dict = dict()
    for resp in resp_list:
        if (resp):
            merged_dict.update(json.loads(resp))

    with open(DATA_BRICK, 'w') as fid01:
        json.dump(merged_dict, fid01)

    return None

# *****************************************************************************


# Runs locally
def get_sim_files(exp_id='', LOCAL_PATH=''):

    # Connect to COMPS
    plat = Platform(block='COMPS',
                    endpoint=COMPS_URL,
                    environment='Calculon')

    # Create python task for SSMT work item
    task_obj = PythonTask(python_path='python3',
                          script_path=FILENAME_PY)

    # Add script for python task and exp id file to assets
    asset01 = Asset(filename=FILENAME_ID, content=exp_id)
    asset02 = Asset(filename=os.path.join(LOCAL_PATH, FILENAME_PY))
    task_obj.common_assets.add_asset(asset01)
    task_obj.common_assets.add_asset(asset02)

    # Reduce experiment output to single file
    wi_obj = SSMTWorkItem(name='ReduceExpOutput',
                          task=task_obj,
                          docker_image=DOCK_PACK)
    wi_obj.run(wait_on_done=True)

    # Download reduced output and delete work item
    resp_dict = plat.get_files(wi_obj, [DATA_BRICK])
    ret_val = json.loads(resp_dict[DATA_BRICK].decode())
    plat_obj = wi_obj.get_platform_object()
    plat_obj.delete()

    return ret_val

# *****************************************************************************


if (__name__ == "__main__"):

    pool_manager()

# *****************************************************************************
