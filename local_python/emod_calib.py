#********************************************************************************
#
#********************************************************************************

import os, shutil, json

from idmtools.core.platform_factory     import  Platform
from idmtools.core.enums                import  ItemType
from idmtools.core.id_file              import  read_id_file, write_id_file

from Assets.emod_exp                    import  exp_from_def_file
from Assets.emod_opt                    import  next_point_alg

#********************************************************************************

def application():

  # Paths
  PATH_PYTHON   = os.path.abspath(os.path.join('Assets','python'))
  PATH_DATA     = os.path.abspath(os.path.join('Assets','data'))
  PATH_ENV      = os.path.abspath(os.path.join('Assets','EMOD_SIF.id'))
  PATH_EXE      = os.path.abspath(os.path.join('Assets','EMOD_EXE.id'))

  # Prepare the platform
  plat_obj = Platform(block           = 'COMPS',
                      endpoint        = 'https://comps.idmod.org',
                      environment     = 'Calculon',
                      priority        = 'Normal',
                      simulation_root = '$COMPS_PATH(USER)',
                      node_group      = 'idm_abcd',
                      num_cores       = '1',
                      num_retries     = '0',
                      exclusive       = 'False')

  # Initialize iteration number
  iter_num = 0

  # Get initial experiment object
  (exp_id,_,_,_) = read_id_file('COMPS_ID.id')
  exp_obj = plat_obj.get_item(item_id=exp_id, item_type=ItemType.EXPERIMENT)

  1/0

  # Iterate
  for iter_num in range(3):

    # Get experiment definition file
    exp_def_file = os.path.join('Assets','param_dict.json')
    resp_dict    = plat_obj.get_files(exp_obj,[exp_def_file])
    param_dict   = json.loads(resp_dict[list(resp_dict.keys())[0]][exp_def_file].decode())
    with open('param_dict_iter{:02d}.json'.format(iter_num), 'w') as fid01:
      json.dump(param_dict, fid01, sort_keys=True, indent=4)

    # Get calibration scores
    calib_score  = 'calval_out.json'
    resp_dict    = plat_obj.get_files(exp_obj,[calib_score])
    calib_list   = [json.loads(resp_dict[simid][calib_score].decode()) for simid in resp_dict.keys()]
    calib_dict   = dict()
    for cal_entry in calib_list:
      calib_dict.update(cal_entry)
    with open('calib_dict_iter{:02d}.json'.format(iter_num), 'w') as fid01:
      json.dump(calib_dict, fid01, sort_keys=True, indent=4)

    # NEXT POINT AGLORITHM GOES HERE
    param_dict_new = param_dict   # <----
    param_dict_new['EXP_NAME'] = param_dict_new['exp_name'] + '_iter{:02d}'.format(iter_num+1)
    param_dict_new['NUM_SIMS'] = param_dict_new['num_sims']
    PATH_EXP_DEF = os.path.abspath('param_dict.json')
    with open(PATH_EXP_DEF, 'w') as fid01:
      json.dump(param_dict_new, fid01, sort_keys=True, indent=4)

    # Create experiment object
    exp_obj_new = exp_from_def_file(PATH_EXP_DEF, PATH_PYTHON, PATH_ENV, PATH_EXE, PATH_DATA)

    # Send experiment to COMPS; start processing; wait until done
    plat_obj.run_items(exp_obj_new)
    plat_obj.wait_till_done(exp_obj_new)

    # Save experiment id to file
    write_id_file('COMPS_ID_iter{:02d}.id'.format(iter_num+1), exp_obj_new)

    # Update iteration
    exp_obj = exp_obj_new


  return None

#*******************************************************************************

if (__name__ == "__main__"):

  application()

#*******************************************************************************
