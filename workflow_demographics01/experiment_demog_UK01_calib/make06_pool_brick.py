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
DOCK_PACK  = r'docker-production.packages.idmod.org/idmtools/comps_ssmt_worker:1.6.4.8'




def get_sim_files():

  # Get Work Item ID
  (wi_id,_,_,_) = read_id_file('CALIB_ID.id')

  # Connect to COMPS; needs to be the same environment used to run work item
  plat_obj  = Platform(block        = 'COMPS',
                       endpoint     = 'https://comps.idmod.org',
                       environment  = 'Calculon')

  # Calibration parameters
  with open('param_calib.json') as fid01:
    param_calib = json.load(fid01)

  filelist       = list()
  for k1 in range(param_calib['NUM_ITER']+1):
    filelist.append('param_dict_iter{:02d}.json'.format(k1))
    filelist.append('data_calib_iter{:02d}.json'.format(k1))

  # Creates a single docker work item to collect the specified files and download
  # Work item will auto-delete related_work_items! Don't let it!
  dwi_obj = DownloadWorkItem(item_name                    = 'RetreiveFiles01',
                             related_work_items           = [wi_id],
                             file_patterns                = filelist,
                             delete_after_download        = False,     # CRITICAL!!!
                             output_path                  = PATH_TEMP,
                             docker_image                 = DOCK_PACK)

  # Wait until everything is downloaded
  dwi_obj.run(wait_on_done=True, platform=plat_obj)



def proc_files():

  merged_param = dict()
  merged_calib = dict()

  # Aggregates all the data from downloaded files into a single dictionary
  for (root_path, dirs_list, files_list) in os.walk(PATH_TEMP):
    for file_name in files_list:
      idx_str = file_name[-7:-5]
      if('param' in file_name):
        with open(os.path.join(root_path,file_name)) as fid01:
          sim_dict = json.load(fid01)
        merged_param[idx_str] = sim_dict
      if('calib' in file_name):
        with open(os.path.join(root_path,file_name)) as fid01:
          sim_dict = json.load(fid01)
        merged_calib[idx_str] = sim_dict

  with open('param_dict_iters.json','w') as fid01:
    json.dump(merged_param,fid01)

  with open('data_calib_iters.json','w') as fid01:
    json.dump(merged_calib,fid01)


  # DELETE ALL TEMPORARY FILES
  shutil.rmtree(PATH_TEMP)



# ******************************************************************************

if(__name__ == "__main__"):

  get_sim_files()

  proc_files()

# ******************************************************************************