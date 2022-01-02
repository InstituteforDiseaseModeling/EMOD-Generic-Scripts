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

EX_VAL = -1.0e10

def application():


  # Arguments to calibration
  gen_param = {'NSIMS':                                     300 ,
               'NITER':                                       8 ,
               'PNAMES':  ['log_mort_mult01','log_mort_mult02'] ,
               'PRANGES': [       (-2.0,2.0),       (-2.0,2.0)] }


  # Paths
  PATH_PYTHON   = os.path.abspath(os.path.join('Assets','python'))
  PATH_DATA     = os.path.abspath(os.path.join('Assets','data'))
  PATH_ENV      = os.path.abspath(os.path.join('Assets','EMOD_ENV.id'))
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

  # Get initial experiment object
  (exp_id,_,_,_) = read_id_file('COMPS_ID.id')
  exp_obj = plat_obj.get_item(item_id=exp_id, item_type=ItemType.EXPERIMENT)

  # Get initial experiment definition file and calibration scores
  exp_def_file = os.path.join('Assets','param_dict.json')
  calib_score  = 'calval_out.json'
  resp_dict    = plat_obj.get_files(exp_obj,[exp_def_file,calib_score])
  param_dict   = json.loads(resp_dict[list(resp_dict.keys())[0]][exp_def_file].decode())
  calib_list   = [json.loads(resp_dict[simid][calib_score].decode()) for simid in resp_dict.keys()]
  calib_dict   = dict()
  for cal_entry in calib_list:
    calib_dict.update(cal_entry)
  with open('param_dict_iter{:02d}.json'.format(0), 'w') as fid01:
    json.dump(param_dict, fid01, sort_keys=True, indent=4)
  with open('data_calib_iter{:02d}.json'.format(0), 'w') as fid01:
    json.dump(calib_dict, fid01, sort_keys=True, indent=4)

  # Set base name
  EXP_BASE_NAME = param_dict['EXP_NAME']

  # Iterate
  for iter_num in range(gen_param['NITER']):

    # Create summary data object
    sum_data = {pname:list() for pname in gen_param['PNAMES']}
    obj_data = list()
    for k2 in range(iter_num+1):
      with open('param_dict_iter{:02d}.json'.format(k2)) as fid01:
        temp_params = json.load(fid01)
      for var_name in sum_data:
        sum_data[var_name].extend(temp_params['EXP_VARIABLE'][var_name])

      obj_temp = temp_params['NUM_SIMS']*[EX_VAL]
      with open('data_calib_iter{:02d}.json'.format(k2)) as fid01:
        temp_objfun = json.load(fid01)
      for var_name in temp_objfun:
        obj_temp[int(var_name)] = -temp_objfun[var_name]
      obj_data.extend(obj_temp)

    sum_data['OBJ_FUN'] = obj_data

    # Next point algorithm
    param_out = next_point_alg(gen_param, sum_data, EX_VAL)

    # Create new exp definition file
    param_dict_new = param_dict
    param_dict_new['EXP_NAME'] = EXP_BASE_NAME + '_iter{:02d}'.format(iter_num+1)
    param_dict_new['NUM_SIMS'] = gen_param['NSIMS']
    for var_name in param_out:
      param_dict_new['EXP_VARIABLE'][var_name] = param_out[var_name]

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

    # Save experiment definition file and calibration scores to calibration object
    resp_dict    = plat_obj.get_files(exp_obj,[exp_def_file,calib_score])
    param_dict   = json.loads(resp_dict[list(resp_dict.keys())[0]][exp_def_file].decode())
    calib_list   = [json.loads(resp_dict[simid][calib_score].decode()) for simid in resp_dict.keys()]
    calib_dict   = dict()
    for cal_entry in calib_list:
      calib_dict.update(cal_entry)
    with open('param_dict_iter{:02d}.json'.format(iter_num+1), 'w') as fid01:
      json.dump(param_dict, fid01, sort_keys=True, indent=4)
    with open('data_calib_iter{:02d}.json'.format(iter_num+1), 'w') as fid01:
      json.dump(calib_dict, fid01, sort_keys=True, indent=4)


  return None

#*******************************************************************************

if (__name__ == "__main__"):

  application()

#*******************************************************************************
