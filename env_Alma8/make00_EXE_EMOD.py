#*******************************************************************************
#
#*******************************************************************************

import os, sys, json

from idmtools.core.platform_factory      import Platform
from idmtools.core.id_file               import write_id_file
from idmtools.entities.command_task      import CommandTask
from idmtools.entities.experiment        import Experiment
from idmtools_platform_comps.utils.singularity_build \
                                         import SingularityBuildWorkItem
from idmtools_platform_comps.utils.assetize_output.assetize_output \
                                         import AssetizeOutput

# ******************************************************************************

# Run work items on COMPS
def make_work():

  # Prepare the platform
  plat_obj = Platform(block            = 'COMPS',
                      endpoint         = 'https://comps.idmod.org',
                      environment      = 'Calculon',
                      priority         = 'Highest',
                      simulation_root  = '$COMPS_PATH(USER)',
                      node_group       = 'idm_48cores',
                      num_cores        = '1',
                      num_retries      = '0',
                      exclusive        = 'False')

  # Creates a work item to create the build image
  sbwi_obj = SingularityBuildWorkItem(name             = 'Build_EMOD_EXE_Alma8',
                                      definition_file  = 'EMOD_EXE_Alma8.def',
                                      force            = True)

  # Wait until the build image is finished
  ac_obj = sbwi_obj.run(wait_on_done=True, platform=plat_obj)

  # Magic words
  cmd_line = 'singularity exec Assets/EMOD_EXE_Alma8.sif cp -r /outputs/. .'

  # Create CommandTask
  task_obj = CommandTask(command=cmd_line)
  task_obj.common_assets.add_assets(ac_obj)

  # Wait until asset collection has been built
  ao_obj = AssetizeOutput(no_simulation_prefix = True)
  ao_obj.from_items(Experiment.from_task(task_obj))
  ao_obj.run(wait_on_done=True, platform=plat_obj)

  # Save asset collection id to file
  write_id_file('EMOD_EXE.id', ao_obj.asset_collection)
  print()
  print(ao_obj.uid.hex)

  return None

# ******************************************************************************

if(__name__ == "__main__"):

  make_work()

# ******************************************************************************