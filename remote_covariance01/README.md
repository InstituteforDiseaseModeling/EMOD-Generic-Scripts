This remote workflow aims to separate out defining and uploading (client
side operations) from writing inputs and running sims (server side).



Client Side: Uses 'idmtools' and 'emodpy' to communicate with COMPS

1. Create a parameter dictionary that specifies the variables for the
   simulation.

2. Upload the parameter dictionary along with an ID and python files that use
   the parameter dictionary to create input files. Run the simulations.

3. Collect results from the server.



Server Side: Uses 'emod_api' (optionally 'emodpy_measles') for file creation

Each EMOD simulation automatically runs 3 python functions: dtk_pre_process,
dtk_in_prcoess, and dtk_post_process. All file creation work is done within
the dtk_pre_prcoess function. That application will find the ID assigned to
the simulation, open the parameter dictionary and retrieve the correct values
for the simulation, then use 'emod_api' to create input files.



The easiest way to trace the workflow is to start in the experiment_example01
directory. It has 3 python scripts (corresponding to the 3 client-side steps
above) that need to be run in order.



Directory 'figure_attackfrac01' has a script that makes a figure from the 
outputs (if everything worked correctly).