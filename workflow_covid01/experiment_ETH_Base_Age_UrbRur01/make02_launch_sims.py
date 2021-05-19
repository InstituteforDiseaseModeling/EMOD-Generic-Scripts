#*******************************************************************************
#
# Python 3.6.0
#
#*******************************************************************************

import os, sys, json, time

from idmtools.assets                  import Asset, AssetCollection
from idmtools.builders                import SimulationBuilder
from idmtools.core.platform_factory   import Platform
from idmtools.entities.experiment     import Experiment
from idmtools_platform_comps.utils.python_requirements_ac.requirements_to_asset_collection \
                                      import RequirementsToAssetCollection

from emodpy.emod_task                 import EMODTask

# ******************************************************************************



# Paths
PATH_PARAM  = os.path.abspath('param_dict.json')
PATH_PYTHON = os.path.abspath(os.path.join('..', 'Assets', 'python'))
PATH_BIN    = os.path.abspath(os.path.join('..', '..', 'exe_GenericOngoing', 'Eradication'))
PATH_DLLS   = os.path.abspath(os.path.join('..', '..', 'exe_GenericOngoing', 'reporter_plugins'))
PATH_SCHEMA = os.path.abspath(os.path.join('..', '..', 'exe_GenericOngoing', 'schema.json'))



# Function for use in sweep builder
def sweep_func(simulation, arg_tuple):
  sim_idx     = arg_tuple[0]
  vars_dict   = arg_tuple[1]

  simulation.tags['sim_index'] = sim_idx
  for var_name in vars_dict:
    simulation.tags[var_name] = vars_dict[var_name][sim_idx]

  simulation.task.transient_assets.add_asset(Asset(filename = 'idx_str_file.txt',
                                                   content  = '{:05d}'.format(sim_idx)))
  return None



# Start and experiment on COMPS
def run_sims():

  # Get experiment parameters from json file
  with open(PATH_PARAM) as fid01:
    param_dict = json.load(fid01)
  exp_name = param_dict['exp_name']
  num_sims = param_dict['num_sims']

  # Prepare the platform
  plat_obj = Platform('COMPS',
                      endpoint        = 'https://comps.idmod.org',
                      environment     = 'Calculon',
                      priority        = 'Normal',
                      simulation_root = '$COMPS_PATH(USER)',
                      node_group      = 'idm_abcd',
                      num_cores       = '1',
                      num_retries     = '0',
                      exclusive       = 'False')

  # Request python packages on COMPS (may take a while if first time requesting package)
  asset_builder = RequirementsToAssetCollection(plat_obj, pkg_list=['emod-api'])
  asset_id01    = asset_builder.run()
  python_reqs   = AssetCollection.from_id(asset_id01, platform=plat_obj)
  exp_assets    = AssetCollection(python_reqs)

  # Create EMODTask
  task_obj = EMODTask.from_files(config_path        = None,
                                 demographics_paths = None,
                                 eradication_path   = PATH_BIN,
                                 ep4_path           = PATH_PYTHON)
  task_obj.campaign            = None
  task_obj.common_assets       = exp_assets

  # Add the parameters dictionary to assets
  param_asset = Asset(absolute_path=PATH_PARAM)
  task_obj.common_assets.add_asset(param_asset)

  # Add the parameters dictionary to assets
  param_asset = Asset(absolute_path=PATH_SCHEMA)
  task_obj.common_assets.add_asset(param_asset)

  # Add everything in the python assets directory as assets
  task_obj.common_assets.add_directory(assets_directory=PATH_PYTHON,relative_path='python')

  # Create simulation sweep with builder
  #   Odd syntax; sweep definition needs two args: sweep function and a list. The sweep function
  #   is called once for each item in the list. Here, the list is of a 2-tuple created by the
  #   zip function. Can't just be an interable, needs to be a list. First value for each tuple is
  #   the integer index of the simulation, second value is the dict of variables. All of those
  #   second-values are actually the SAME DICTIONARY (no deep copy) so don't make any changes
  #   in the sweep function.
  build_obj     = SimulationBuilder()
  sim_id_list   = list(range(num_sims))
  dict_list     = num_sims*[param_dict['EXP_VARIABLE']]
  build_obj.add_sweep_definition(sweep_func, list(zip(sim_id_list,dict_list)))

  # Create an experiment from builder
  experiment = Experiment.from_builder(build_obj, task_obj, name=exp_name)

  # Run experiment
  plat_obj.run_items(experiment)

  # Save experiment id to file
  with open('COMPS_ID', 'w') as fid01:
    fid01.write(experiment.uid.hex)
  print()
  print(experiment.uid.hex)

  return None



# ******************************************************************************

if __name__ == "__main__":

  run_sims()

# ******************************************************************************