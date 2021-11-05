#*******************************************************************************
#
# Python 3.6.0
#
#*******************************************************************************

import os, sys, json

from idmtools.assets                  import Asset, AssetCollection
from idmtools.builders                import SimulationBuilder
from idmtools.core.platform_factory   import Platform
from idmtools.entities.experiment     import Experiment
from idmtools.core.id_file            import write_id_file

from emodpy.emod_task                 import EMODTask

# ******************************************************************************



# Paths
PATH_PARAM  = os.path.abspath('param_dict.json')
PATH_PYTHON = os.path.abspath(os.path.join('..', 'Assets', 'python'))
PATH_ENV    = os.path.abspath(os.path.join('..', '..', 'env_CentOS8',   'EMOD_SIF.id'))
PATH_EXE    = os.path.abspath(os.path.join('..', '..', 'env_BuildEMOD', 'EMOD_EXE.id'))



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

  # Prepare the platform
  plat_obj = Platform(block           = 'COMPS',
                      endpoint        = 'https://comps.idmod.org',
                      environment     = 'Calculon',
                      priority        = 'Normal',
                      simulation_root = '$COMPS_PATH(USER)',
                      node_group      = 'idm_abcd',
                      num_cores       = '1',
                      num_retries     = '0',
                      exclusive       = 'False')

  # Create EMODTask
  task_obj = EMODTask.from_files(ep4_path = PATH_PYTHON)
  task_obj.set_sif(PATH_ENV)

  # Get experiment parameters from json file
  with open(PATH_PARAM) as fid01:
    param_dict = json.load(fid01)
  EXP_NAME = param_dict['EXP_NAME']
  NUM_SIMS = param_dict['NUM_SIMS']

  # Add the parameters dictionary to assets
  param_asset = Asset(absolute_path=PATH_PARAM)
  task_obj.common_assets.add_asset(param_asset)

  # Add the executable and schema
  exe_asset   = AssetCollection.from_id_file(PATH_EXE)
  task_obj.common_assets.add_assets(exe_asset)

  # Add everything in the python assets directory as assets; dtk files already added
  for filename in os.listdir(PATH_PYTHON):
    if(not filename.startswith('dtk') and not filename.startswith('__')):
      param_asset = Asset(absolute_path=os.path.join(PATH_PYTHON,filename),relative_path='python')
      task_obj.common_assets.add_asset(param_asset)

  # Create simulation sweep with builder
  #   Odd syntax; sweep definition needs two args: sweep function and a list. The sweep function
  #   is called once for each item in the list. Here, the list is of a 2-tuple created by the
  #   zip function. Can't just be an interable, needs to be a list. First value for each tuple is
  #   the integer index of the simulation, second value is the dict of variables. All of those
  #   second-values are actually the SAME DICTIONARY (no deep copy) so don't make any changes
  #   in the sweep function.
  build_obj     = SimulationBuilder()
  sim_id_list   = list(range(NUM_SIMS))
  dict_list     = NUM_SIMS*[param_dict['EXP_VARIABLE']]
  build_obj.add_sweep_definition(sweep_func, list(zip(sim_id_list,dict_list)))

  # Create an experiment from builder
  experiment = Experiment.from_builder(build_obj, task_obj, name=EXP_NAME)

  # Run experiment
  plat_obj.run_items(experiment)

  # Save experiment id to file
  write_id_file('COMPS_ID.id', experiment)
  print()
  print(experiment.uid.hex)

  return None


# ******************************************************************************

if(__name__ == "__main__"):

  run_sims()

# ******************************************************************************