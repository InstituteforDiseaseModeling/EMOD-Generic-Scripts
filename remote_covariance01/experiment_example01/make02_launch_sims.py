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
def sweep_func(simulation, sim_idx_val):
  sim_idx_str = '{:05d}'.format(sim_idx_val)
  simulation.tags['sim_index'] = sim_idx_str
  simulation.task.transient_assets.add_asset(Asset(filename = "idx_str_file.txt",
                                                   content  = sim_idx_str))
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
  asset_builder = RequirementsToAssetCollection(plat_obj, pkg_list=['emod_api']) # can specify version 'emod_api==1.0.0'
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

  # Add the schema to assets
  param_asset = Asset(absolute_path=PATH_SCHEMA)
  task_obj.common_assets.add_asset(param_asset)

  # Add everything in the dlls directory as assets
  task_obj.common_assets.add_directory(assets_directory=PATH_DLLS,  relative_path='reporter_plugins')

  # Add everything in the python assets directory as assets
  task_obj.common_assets.add_directory(assets_directory=PATH_PYTHON,relative_path='python')

  # Create simulation sweep with builder
  build_obj = SimulationBuilder()
  build_obj.add_sweep_definition(sweep_func, list(range(num_sims)))

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

if(__name__ == "__main__"):

  run_sims()

# ******************************************************************************