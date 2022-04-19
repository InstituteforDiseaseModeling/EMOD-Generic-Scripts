# EMOD-Generic

See https://docs.idmod.org/projects/emod-generic-scripts/en/latest/ for
additional information about how to use these scripts.


## Contents:

| Directory | Description |
| --- | --- |
| env_Alma8 <br /> env_Debian11 <br /> env_Fedora35 <br /> env_Ubuntu22 |  Contains the definition scripts for singularity image files. One image produces the the EMOD executable, schema, and custom reporters; a second image is used as the environment for running EMOD on COMPS and contains the python packages available to the embedded python interpreter. All files remain on COMPS and are provided to the various workflows as Asset Collection IDs. |
| local_python             | Contains additional python scripts that provide helper functions common to all of the workflows. |
| workflow_covariance01    | Demonstration of the covariance feature. |
| workflow_covid01         | Baseline simulations for SARS-CoV-2 in EMOD. Collab with MvG. |
| workflow_demographics01  | Example demographics for UK measles simulations. |
| workflow_demographics02  | Example demographics using UN WPP data as inputs. |
| workflow_measles_gha01   | Examination of RDT use and responsive campaigns for measles using Ghana as an example context. |
| workflow_network01       | Demonstration of the network infectivity feature. |
| workflow_polio_nga01     | Example outbreak simulations for cVDPV2 in Nigeria. Collab with JG and HL. |
| workflow_rubella_drc01   | Example of rubella vaccine introduction for the Democratic Republic of the Congo assuming rollout through routine immunization services only. |
| workflow_rubella_drc02   | Extension of the DRC01 workflow examining time-varying demographics and correcting DHS fertility rate values. |
| workflow_transtree01     | Demonstration of the infector labeling feature and generation of explicit transmission networks. |
