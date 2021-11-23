# EMOD-Generic

See https://docs.idmod.org/projects/emod-generic-scripts/en/latest/ for
additional information about how to use these scripts.


## Contents:

  env_Debian10           - Contains the definition scripts for singularity
                           image files. One image produces the the executable,
                           schema, and custom reporters; a second image is
                           used as the environment on COMPS and contains the
                           python packages available to the embedded python
                           interpreter. All files remain on COMPS and are
                           provided to the various workflows as Asset
                           Collection IDs.



  workflow_covariance01  - Demonstration of the covariance feature.

  workflow_covid01       - Baseline simulations for SARS-CoV-2 in EMOD. Collab
                           with MvG.

  workflow_demographics01- Example demographics for UK measles simulations.

  workflow_network01     - Demonstration of the network infectivity feature.

  workflow_polio01       - Example outbreak simulations for cVDPV2 in Nigeria.
                           Collab with JG and HL.

  workflow_transtree01   - Demonstration of the infector labeling feature and
                           generation of explicit transmission networks.
