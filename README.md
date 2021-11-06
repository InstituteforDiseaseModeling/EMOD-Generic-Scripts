# EMOD-Generic

See documentation at https://docs.idmod.org/projects/emod-generic-scripts/en/latest/
for additional information about how to use the scripts.

## Contents:

  env_CentOS8            - Contains the definition script for a singularity 
                           image file that is used for for running EMOD on COMPS.
                           Produces an asset collection ID that is used in the
                           various workflows.

  env_BuildEMOD          - Contains the definition script for a singularity 
                           image file that builds the EMOD executable.
                           Produces an asset collection ID that is used in the
                           various workflows.


  workflow_covariance01  - Demonstration of the covariance feature.

  workflow_covid01       - Baseline simulations for SARS-CoV-2 in EMOD. Collab
                           with MvG.

  workflow_demographics01- Example demographics for UK measles simulations.

  workflow_network01     - Demonstration of the network infectivity feature.

  workflow_polio01       - Example outbreak simulations for cVDPV2 in Nigeria.
                           Collab with JG and HL.

  workflow_trans-tree01  - Demonstration of the infector labeling feature and
                           generation of explicit transmission networks.