#********************************************************************************
#
# Python 3.6.0
#
#*******************************************************************************

import os, sys, shutil, json

from idmtools.core.platform_factory                    import  Platform
from idmtools_platform_comps.utils.download.download   import  DownloadWorkItem
from idmtools.core.id_file                             import  read_id_file

import numpy as np

# ******************************************************************************



# Paths
PATH_TEMP    = os.path.abspath('temp_dir')
PATH_OUTPUT  = os.path.abspath('output')



def get_sim_files():

  # Get Experiment ID
  (exp_id,_,_,_) = read_id_file('COMPS_ID.id')

  # Connect to COMPS; needs to be the same environment used to run the sims
  plat_obj = Platform(block        = 'COMPS',
                      endpoint     = 'https://comps.idmod.org',
                      environment  = 'Calculon')

  # Creates a single docker work item to collect the specified files and download
  dwi_obj = DownloadWorkItem(item_name                    = 'RetreiveFiles01',
                             related_experiments          = [exp_id],
                             file_patterns                = ['output/lga_timeseries.csv',
                                                             'idx_str_file.txt',
                                                             'node_names.json'],
                             simulation_prefix_format_str = 'temp/{simulation.id}',
                             output_path                  = PATH_TEMP)

  # Wait until everything is downloaded
  dwi_obj.run(wait_on_done=True, platform=plat_obj)



def proc_files():

  if(not os.path.isdir(PATH_OUTPUT)):
    os.mkdir(PATH_OUTPUT)

  # Aggregates all the data from downloaded files into a single dictionary
  for (root_path, dirs_list, files_list) in os.walk(PATH_TEMP):
    for file_name in files_list:
      if(file_name == 'lga_timeseries.csv'):
        with open(os.path.join(root_path,'..','idx_str_file.txt')) as fid01:
          sim_index = int(fid01.readline())
        targ_file = os.path.join(PATH_OUTPUT,'inf_circ_{:05d}.csv'.format(sim_index))
        shutil.copyfile(os.path.join(root_path,'lga_timeseries.csv'),targ_file)
        if(sim_index == 0):
          targ_file = os.path.join(PATH_OUTPUT,'node_names.json')
          shutil.copyfile(os.path.join(root_path,'..','node_names.json'),targ_file)



  # DELETE ALL TEMPORARY FILES
  shutil.rmtree(PATH_TEMP)



# ******************************************************************************

if(__name__ == "__main__"):

  get_sim_files()

  proc_files()

# ******************************************************************************