# EMOD-Generic

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


## Workflow notes:

  Separate defining and uploading (client side operations) from writing
  inputs and running sims (server side).


  Client Side: Uses 'idmtools' and 'emodpy' to communicate with COMPS

  1. Create a parameter dictionary that specifies the variables for the
     simulation.
     OUTPUT = param_dict.json

  2. Upload the parameter dictionary along with an ID and python files that use
     the parameter dictionary to create input files. Run the simulations.
     OUTPUT = COMPS_ID.id

  3. Collect results from the server.
     OUTPUT = data_brick.json (and others)


  Server Side: Uses 'emod-api' for file creation

    Each EMOD simulation automatically runs 3 python functions: dtk_pre_process,
    dtk_in_process, and dtk_post_process. All file creation work is done within
    the dtk_pre_process function. That application will find the ID assigned to
    the simulation, open the parameter dictionary and retrieve the correct
    values for the simulation, then use 'emod-api' to create input files.

    The easiest way to trace the workflow is to start in an experiment directory
    and examine the 3 python scripts (corresponding to the 3 client-side steps
    above) that need to be run in order.


## To run an example:

1. Setup a virtual environment (e.g. conda)
2. Install requirements via `pip` using IDM artifactory:
    ```
    >> pip install -r requirements.txt --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
    ```
3. Build the environment:
    ```
    >> cd EMOD-Generic/env_CentOS8
    >> python make00_container.py
    ```
4. Build the executable:
    ```
    >> cd EMOD-Generic/env_BuildEMOD
    >> python make00_executable.py
    ```
4. Run experiment:
    ```
    >> cd EMOD_Generic/workflow_covariance01/experiment_covariance01
    >> python make01_param_dict.py
    >> python make02_lauch_sims.py
    >> python make03_pool_brick.py
    ```
5. Generate figures:
    ```
    >> cd EMOD_Generic/workflow_covariance01/figure_attackfrac01
    >> make_fig_attackrate01.py
    ```


## Environment notes (client):

  ********************************
  Helpful speed-up (see InstituteforDiseaseModeling/idmtools/issues/1395)

    DIRNAME\idmtools\Lib\site-packages\idmtools\entities\templated_simulation.py
    (line 184)
      + sim.task.common_assets = self.base_simulation.task.common_assets

    DIRNAME\idmtools\Lib\site-packages\idmtools\entities\itask.py
    (line 224)
      - if k not in ['_task_log']:
      + if k not in ['_task_log','common_assets']:

  ********************************
