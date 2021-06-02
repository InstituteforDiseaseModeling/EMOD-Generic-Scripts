#*******************************************************************************
#
# Python 3.6.0
#
#*******************************************************************************

import os, sys, json

from idmtools.core.platform_factory      import Platform
from idmtools_platform_comps.utils.singularity_build \
                                         import SingularityBuildWorkItem

# ******************************************************************************

# Start and experiment on COMPS
def make_work():

  # Prepare the platform
  plat_obj = Platform('COMPS',
                      endpoint        = 'https://comps.idmod.org',
                      environment     = 'Calculon',
                      priority        = 'Normal',
                      simulation_root = '$COMPS_PATH(USER)',
                      node_group      = 'idm_48cores',
                      num_cores       = '1',
                      num_retries     = '0',
                      exclusive       = 'False')

  # Creates a single work item to create the image
  sbwi_obj = SingularityBuildWorkItem(definition_file  = 'EMOD_env01.def',
                                      force            = True)

  # Wait until the image is built
  ac_obj = sbwi_obj.run(wait_on_done=True, platform=plat_obj)

  # Save asset id for sif to file
  with open('ASSETS_ID', 'w') as fid01:
    fid01.write(ac_obj.uid.hex)
  print()
  print(ac_obj.uid.hex)


  return None



# ******************************************************************************

if(__name__ == "__main__"):

  make_work()

# ******************************************************************************