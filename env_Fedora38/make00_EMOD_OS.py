#*******************************************************************************
#
#*******************************************************************************

import os, sys, json

from idmtools.core.platform_factory      import Platform
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

  # Creates a work item to build image
  sbwi_obj = SingularityBuildWorkItem(name             = 'Build_EMOD_OS_Fedora38',
                                      definition_file  = 'EMOD_OS_Fedora38.def',
                                      force            = True)

  # Wait until the image is built
  ac_obj = sbwi_obj.run(wait_on_done=True, platform=plat_obj)

  # Save asset id for sif to file
  write_id_file('EMOD_OS.id', ac_obj)
  print()
  print(ac_obj.uid.hex)

  return None

# ******************************************************************************

if(__name__ == "__main__"):

  make_work()

# ******************************************************************************