# EMOD-Generic



Contents:

  exe_GenericOngoing     - Contains the executable, schema file, and reporters
                           (if any). Including these files here is not best
                           practice (could auto-download) but having a local
                           copy eliminates some VPN issues:
                           InstituteforDiseaseModeling/DtkTrunk/Generic-Ongoing

  workflow_covariance01  - Demonstration of the covariance feature.



Workflow notes:

  Separate defining and uploading (client side operations) from writing
  inputs and running sims (server side).


  Client Side: Uses 'idmtools' and 'emodpy' to communicate with COMPS

  1. Create a parameter dictionary that specifies the variables for the
     simulation.

  2. Upload the parameter dictionary along with an ID and python files that use
     the parameter dictionary to create input files. Run the simulations.

  3. Collect results from the server.


  Server Side: Uses 'emod_api' for file creation

    Each EMOD simulation automatically runs 3 python functions: dtk_pre_process,
    dtk_in_prcoess, and dtk_post_process. All file creation work is done within
    the dtk_pre_prcoess function. That application will find the ID assigned to
    the simulation, open the parameter dictionary and retrieve the correct
    values for the simulation, then use 'emod_api' to create input files.

    The easiest way to trace the workflow is to start in an experiment directory
    and examine the 3 python scripts (corresponding to the 3 client-side steps
    above) that need to be run in order.



Environment notes (client):

  Requires idmtools[idm] and emodpy

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

    