#********************************************************************************
#
#********************************************************************************

import os, json

from idmtools.assets                                          import  Asset, AssetCollection
from idmtools.builders                                        import  SimulationBuilder
from idmtools.entities.experiment                             import  Experiment
from idmtools_models.python.python_task                       import  PythonTask
from idmtools_platform_comps.ssmt_work_items.comps_workitems  import  SSMTWorkItem

#from emodpy.emod_task                 import EMODTask
from emod_task                        import EMODTask

from emod_reduce                      import DOCK_PACK

#*******************************************************************************

def sweep_func(simulation, arg_tuple):

  # Unpack tuple
  sim_idx     = arg_tuple[0]
  vars_dict   = arg_tuple[1]

  # Add tags for sim index and each variable parameter
  simulation.tags['sim_index'] = sim_idx
  for var_name in vars_dict:
    simulation.tags[var_name] = vars_dict[var_name][sim_idx]

  # Create index file as simulation level asset
  simulation.task.transient_assets.add_asset(Asset(filename = 'idx_str_file.txt',
                                                   content  = '{:05d}'.format(sim_idx)))

  return None

#*******************************************************************************

def exp_from_def_file(path_param_dict, path_python, path_env_sif, path_exe, path_data):

  # Create EMODTask
  task_obj = EMODTask.from_files(ep4_path = path_python)

  # Set singularity image for environment
  task_obj.set_sif(path_env_sif)

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
  exe_asset = AssetCollection.from_id_file(path_exe)
  task_obj.common_assets.add_assets(exe_asset)

  # Add everything in the data assets directory as assets;
  task_obj.common_assets.add_directory(path_data, relative_path='data')

  # Create simulation sweep with builder
  #   Odd syntax; sweep definition needs two args: sweep function and a list. The sweep function
  #   is called once for each item in the list. Here, the list is of a 2-tuple created by the
  #   zip function. Can't just be an interable, needs to be a list. First value for each tuple is
  #   the integer index of the simulation, second value is the dict of variables. All of those
  #   second-values are actually the SAME DICTIONARY (no deep copy) so don't make any changes
  #   in the sweep function.
  build_obj     = SimulationBuilder()
  sim_id_list   = list(range(NUM_SIMS))
  dict_list     = NUM_SIMS*[VAR_DICT]
  build_obj.add_sweep_definition(sweep_func, list(zip(sim_id_list,dict_list)))

  # Create an experiment from builder
  exp_obj = Experiment.from_builder(build_obj, task_obj, name=EXP_NAME)

  return exp_obj

#*******************************************************************************

def calib_from_def_file(path_param_dict, path_python, path_env_sif, path_exe, path_data, path_local):

  # Create python task for SSMT work item
  task_obj = PythonTask(python_path = 'python3', script_path = os.path.join(path_local,'emod_calib.py'))

  # Get parameters from json file
  with open(path_param_dict) as fid01:
    param_dict = json.load(fid01)

  EXP_NAME = param_dict['EXP_NAME']

  # Add everything needed to run an experiment and ID from the initial sweep
  task_obj.common_assets.add_directory(path_python, relative_path='python')
  task_obj.common_assets.add_directory(path_data,   relative_path='data')
  task_obj.common_assets.add_directory(path_local)
  task_obj.common_assets.add_asset(path_env_sif)
  task_obj.common_assets.add_asset(path_exe)
  task_obj.common_assets.add_asset(path_param_dict)

  # Add working directory assets
  ac_obj = AssetCollection()
  ac_obj.add_asset('idmtools.ini')

  # Es liebten alle Frauen
  wi_obj = SSMTWorkItem(name             = 'Calibd_'+EXP_NAME,
                        task             = task_obj,
                        transient_assets = ac_obj,
                        docker_image     = DOCK_PACK)

  return wi_obj

#*******************************************************************************