================================
Client- and server-side workflow
================================

This workflow separates defining and uploading (client-side operations) from writing inputs and running sims (server-side).


Client-side
===========

The client-side workflow uses |IT_s| and |emodpy| to communicate with |COMPS_s|.

#.  Create a parameter dictionary that specifies the values for simulation parameters::

        OUTPUT = param_dict.json

#.  Upload the parameter dictionary along with the Python files that use that parameter dictionary to create input files. Run the simulations::

        OUTPUT = COMPS_ID.id

#.  Collect results from the server::

        OUTPUT = data_brick.json (and others)

Client-side speed-up
--------------------

There is a known issue that causes the time to create simulations on |COMPS_s| to increase with the size of Python requirements (see https://github.com/InstituteforDiseaseModeling/idmtools/issues/1395). To work around this issue and reduce the time needed, modify the |IT_s| code as follows::

    DIRNAME\Lib\site-packages\idmtools\entities\templated_simulation.py
    (line 236)
      + sim.task.common_assets = self.base_simulation.task.common_assets

    DIRNAME\Lib\site-packages\idmtools\entities\itask.py
    (line 281)
      - if k not in ['_task_log']:
      + if k not in ['_task_log','common_assets']:

Server-side
===========

The server-side workflow uses |emod_api| for file creation.

Each |EMOD_s| simulation automatically runs three Python functions: ``dtk_pre_process``, ``dtk_in_process``, and ``dtk_post_process``. All file creation work is done within the ``dtk_pre_process`` function. That application will find the ID assigned to the simulation, open the parameter dictionary and retrieve the correct values for the simulation, then use |emod_api| to create input files.

The easiest way to trace the workflow is to start in an experiment directory and examine the three Python scripts (corresponding to the three client-side steps above) that need to be run in order.
