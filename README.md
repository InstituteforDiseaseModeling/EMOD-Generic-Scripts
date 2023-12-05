# EMOD-Generic

See documentation at https://docs.idmod.org/projects/emod-generic-scripts/en/latest/ for
additional information about how to use these scripts.

To build the documentation locally, do the following:

1. Create and activate a venv.  *** Does not support Python 3.11: Use 3.10 ***
2. Navigate to the root directory of the repo and enter the following

    ```
    pip install -r docs/requirements.txt
    ```
## Contents:

| Directory | Description |
| --- | --- |
| env_Alma9 <br /> env_Debian12 <br /> env_Fedora38 <br /> env_Ubuntu22 |  Contains the definition scripts for singularity containers. Produces the the EMOD executable, schema, and custom reporters; creates an environment for running EMOD on COMPS and contains the python packages available to the embedded python interpreter. All files remain on COMPS and are provided to the various workflows as Asset Collection IDs. |
| local_python             | Contains additional python scripts that provide helper functions common to all of the workflows. |
| model_covariance01       | Demonstration of the covariance feature. |
| model_covid01            | Baseline simulations for SARS-CoV-2 in EMOD. Collab with MvG. |
| model_demographics01     | Example demographics for UK measles simulations. |
| model_demographics02     | Example demographics using UN WPP data as inputs. |
| model_measles_gha01      | Examination of RDT use and responsive campaigns for measles using Ghana as an example context. |
| model_measles_nga01      | Documentation. |
| model_network01          | Demonstration of the network infectivity feature. |
| model_polio_nga01        | Example outbreak simulations for cVDPV2 in Nigeria. Collab with JG and HL. |
| model_rubella01          | Projections of rubella infections and CRS burden following RCV introduction.  |
| model_transtree01        | Demonstration of the infector labeling feature and generation of explicit transmission networks. |
| refdat_mcv1              | IHME MCV1 coverage estimates used to construct input files for EMOD simulations. |
| refdat_namesets          | Namesets used for region identification. |
| refdat_poppyr            | UN WPP age structured population estimates used to construct input files for EMOD simulations. |
