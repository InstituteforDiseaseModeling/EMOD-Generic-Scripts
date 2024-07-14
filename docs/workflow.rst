================================
Client- and server-side workflow
================================

This workflow separates defining and uploading (client-side operations) from writing inputs and running sims (server-side).


Client-side
===========

The client-side workflow uses |IT_s| and |emodpy| to communicate with |COMPS_s|.

#.  Create a parameter dictionary that defines the experiment by specifying values for all simulation parameters::

        OUTPUT = param_dict.json

#.  Upload the parameter dictionary along with the Python and data files for constructing model inputs. Run the simulations::

        OUTPUT = COMPS_ID.id

#.  Collect results from the server::

        OUTPUT = data_brick.json


Server-side
===========

The server-side workflow uses |emod_api| for file creation.

Each |EMOD_s| simulation automatically runs a function named ``application`` from three separate Python modules: ``dtk_pre_process``, ``dtk_in_process``, and ``dtk_post_process``.

All input file creation work is done within the function named ``application`` from ``dtk_pre_process``. That function will find the ID assigned to the simulation, open the parameter dictionary and retrieve values for the simulation, then use |emod_api| to create input files.

Every experiment directory containas an ``Assets`` folder with ``python`` and ``data`` subfolders. Each subfolder is copied to |COMPS_s| and available for all siumulations in the experiment.

* ``python``

Contains user-defined python files used by EMOD. Some filenames must remain unchanged: ``dtk_pre_process.py``, ``dtk_in_process.py``, and ``dtk_post_process.py`` are assumed to be present and contain a function named ``application``. Everything else can be user-defined.

* ``data``

Contains csv files, json files, etc. for use by the python scripts python while running EMOD.
