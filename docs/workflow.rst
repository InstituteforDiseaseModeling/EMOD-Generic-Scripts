================================
Client- and server-side workflow
================================

This workflow separates defining and uploading (client-side operations) from writing inputs and running sims (server-side).


Client-side
===========

The client-side workflow uses |IT_s| and |emodpy| to communicate with |COMPS_s|.

#.  Create a parameter dictionary that defines the experiment by specifying values for all simulation parameters::

        OUTPUT = param_dict.json

#.  Upload the parameter dictionary along with the Python files that construct the model inputs. Run the simulations::

        OUTPUT = COMPS_ID.id

#.  Collect results from the server::

        OUTPUT = data_brick.json


Server-side
===========

The server-side workflow uses |emod_api| for file creation.

Each |EMOD_s| simulation automatically runs three Python functions: ``dtk_pre_process``, ``dtk_in_process``, and ``dtk_post_process``. All file creation work is done within the ``dtk_pre_process`` function. That application will find the ID assigned to the simulation, open the parameter dictionary and retrieve the correct values for the simulation, then use |emod_api| to create input files.

The easiest way to trace the workflow is to start in an experiment directory and examine the three Python scripts (corresponding to the three client-side steps above) that need to be run in order.
