# *****************************************************************************
#
# *****************************************************************************

import json
import os

from idmtools.assets import Asset, AssetCollection
from idmtools.builders import SimulationBuilder
from idmtools.entities.experiment import Experiment
from idmtools_models.python.python_task import PythonTask
from idmtools_platform_comps.ssmt_work_items.comps_workitems \
                                        import SSMTWorkItem

from emodpy.emod_task import EMODTask

from py_assets_common.emod_constants import ID_OS, ID_EXE, ID_ENV, ID_SCHEMA, \
                                            DOCK_PACK, VE_PY_PATHS

# *****************************************************************************


def sweep_func(simulation, arg_tuple):

    # Unpack tuple
    sim_idx = arg_tuple[0]
    vars_dict = arg_tuple[1]

    # Add tags for sim index and each variable parameter
    simulation.tags['sim_index'] = sim_idx
    for var_name in vars_dict:
        simulation.tags[var_name] = vars_dict[var_name][sim_idx]

    # Create index file as simulation level asset
    asset_obj = Asset(filename='idx_str_file.txt',
                      content='{:05d}'.format(sim_idx))
    simulation.task.transient_assets.add_asset(asset_obj)

    return None

# *****************************************************************************


def exp_from_def_file(path_param_dict, path_python, path_exe, path_data):

    # Create EMODTask
    task_obj = EMODTask.from_files(ep4_path=path_python)

    # Set singularity image for environment
    task_obj.set_sif(os.path.join(path_exe, ID_ENV))

    # Set path to python
    for py_path in VE_PY_PATHS:
        task_obj.add_py_path(py_path)

    # Get parameters from json file
    with open(path_param_dict) as fid01:
        param_dict = json.load(fid01)

    EXP_NAME = param_dict['EXP_NAME']
    NUM_SIMS = param_dict['NUM_SIMS']
    VAR_DICT = param_dict['EXP_VARIABLE']

    # Add the parameters dictionary to assets
    param_asset = Asset(absolute_path=path_param_dict)
    task_obj.common_assets.add_asset(param_asset)

    # Add the executable and schema
    f_targ = os.path.join(path_exe, ID_EXE)
    exe_asset = AssetCollection.from_id_file(f_targ)
    task_obj.common_assets.add_assets(exe_asset)
    f_targ = os.path.join(path_exe, ID_SCHEMA)
    schema_asset = AssetCollection.from_id_file(f_targ)
    task_obj.common_assets.add_assets(schema_asset)

    # Add everything in the data assets directory as assets;
    task_obj.common_assets.add_directory(path_data, relative_path='data')

    # Add everything in the common python scripts directory as assets;
    f_dir = os.path.dirname(os.path.abspath(__file__))
    PATH_COMMON = os.path.join(f_dir, 'py_assets_common')
    task_obj.common_assets.add_directory(PATH_COMMON, relative_path='python')

    # Create simulation sweep with builder
    #   Odd syntax; sweep definition needs two args: sweep function and a list.
    #   The sweep function is called once for each item in the list. Here, the
    #   list is of a 2-tuple created by the zip function. Can't just be any
    #   iterable, needs to be a list. First value for each tuple is the integer
    #   index of the simulation, second value is the dict of variables. All of
    #   those second-values are actually the SAME DICTIONARY (no deep copy) so
    #   don't make any changes in the sweep function.
    build_obj = SimulationBuilder()
    sim_id_list = list(range(NUM_SIMS))
    dict_list = NUM_SIMS*[VAR_DICT]
    arg_two = list(zip(sim_id_list, dict_list))
    build_obj.add_sweep_definition(sweep_func, arg_two)

    # Create an experiment from builder
    exp_obj = Experiment.from_builder(build_obj, task_obj, name=EXP_NAME)

    return exp_obj

# *****************************************************************************


def calib_from_def_file(pth_pdict, pth_python, pth_exe, pth_data, pth_local):

    # Create python task for SSMT work item
    file_dir = os.path.dirname(os.path.abspath(__file__))
    path_scr = os.path.join(file_dir, 'emod_calib.py')
    task_obj = PythonTask(python_path='python3', script_path=path_scr)

    # Get parameters from json file
    with open(pth_pdict) as fid01:
        param_dict = json.load(fid01)

    EXP_NAME = param_dict['EXP_NAME']

    # Add everything needed to run an experiment and ID from the initial sweep
    task_obj.common_assets.add_directory(pth_python, relative_path='python')
    task_obj.common_assets.add_directory(pth_data, relative_path='data')
    task_obj.common_assets.add_directory(file_dir)
    task_obj.common_assets.add_asset(os.path.join(pth_exe, ID_ENV))
    task_obj.common_assets.add_asset(os.path.join(pth_exe, ID_EXE))
    task_obj.common_assets.add_asset(os.path.join(pth_exe, ID_SCHEMA))
    task_obj.common_assets.add_asset(pth_pdict)

    # Add working directory assets
    ac_obj = AssetCollection()
    ac_obj.add_asset('idmtools.ini')

    # Es liebten alle Frauen
    wi_obj = SSMTWorkItem(name='Calibd_'+EXP_NAME,
                          task=task_obj,
                          transient_assets=ac_obj,
                          docker_image=DOCK_PACK)

    return wi_obj

# *****************************************************************************
