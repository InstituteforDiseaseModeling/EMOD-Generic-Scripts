#*******************************************************************************
#
# Python 3.6.0
#
#*******************************************************************************

import os, sys, json

from idmtools.core.platform_factory      import Platform
from idmtools.assets                     import AssetCollection
from idmtools.core.id_file               import write_id_file
from idmtools_platform_comps.utils.singularity_build \
                                         import SingularityBuildWorkItem

# ******************************************************************************

# Start and experiment on COMPS
def make_work():

  # Prepare the platform
  plat_obj = Platform(block        = 'COMPS',
                      endpoint     = 'https://comps.idmod.org',
                      environment  = 'Calculon')

  # Creates a single work item to create the image
  sbwi_obj = SingularityBuildWorkItem(definition_file  = 'EMOD_build02.def',
                                      force            = True)

  # Add base image
  ac_obj_old = AssetCollection.from_id_file('EMOD_SIF01.id')
  sbwi_obj.add_assets(ac_obj_old)

  # Wait until the image is built
  ac_obj_new = sbwi_obj.run(wait_on_done=True, platform=plat_obj)

  # Save asset id for sif to file
  write_id_file('EMOD_SIF02.id', ac_obj_new)
  print()
  print(ac_obj_new.uid.hex)

  return None

# ******************************************************************************

if(__name__ == "__main__"):

  make_work()

# ******************************************************************************