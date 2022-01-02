#********************************************************************************
#
#*******************************************************************************

import os, sys, shutil, json

from idmtools.core.platform_factory                    import  Platform
from idmtools_platform_comps.utils.download.download   import  DownloadWorkItem
from idmtools.core.id_file                             import  read_id_file

import numpy as np

# ******************************************************************************



# Paths
PATH_TEMP  = os.path.abspath('temp_dir')



def get_sim_files():

  # Get Experiment ID
  (exp_id,_,_,_) = read_id_file('COMPS_ID.id')

  # Connect to COMPS; needs to be the same environment used to run the sims
  plat_obj = Platform(block        = 'COMPS',
                      endpoint     = 'https://comps.idmod.org',
                      environment  = 'Calculon')

  # Creates a single docker work item to collect the specified files and download
  dwi_obj = DownloadWorkItem(name                         = 'RetreiveFiles',
                             related_experiments          = [exp_id],
                             file_patterns                = ['calval_out.json'],
                             simulation_prefix_format_str = 'temp/{simulation.id}',
                             output_path                  = PATH_TEMP)

  # Wait until everything is downloaded
  dwi_obj.run(wait_on_done=True, platform=plat_obj)



def proc_files():

  merged_data  = dict()
  merged_calib = dict()

  # Aggregates all the data from downloaded files into a single dictionary
  for (root_path, dirs_list, files_list) in os.walk(PATH_TEMP):
    for file_name in files_list:
      if(file_name == 'calval_out.json'):
        with open(os.path.join(root_path,file_name)) as fid01:
          sim_dict = json.load(fid01)
        merged_calib.update(sim_dict)

  with open('data_calib.json','w') as fid01:
    json.dump(merged_calib,fid01)


  # DELETE ALL TEMPORARY FILES
  shutil.rmtree(PATH_TEMP)



# ******************************************************************************

if(__name__ == "__main__"):

  get_sim_files()

  proc_files()

# ******************************************************************************