# *****************************************************************************
#
# *****************************************************************************

import json
import os

from idmtools.core.platform_factory import Platform
from idmtools.core.id_file import write_id_file

from Assets.emod_exp import exp_from_def_file
from Assets.emod_opt import next_point_alg
from Assets.emod_reduce import pool_manager

# *****************************************************************************

EX_VAL = -1.0e10

# Paths
PATH_PYTHON = os.path.abspath(os.path.join('Assets', 'python'))
PATH_DATA = os.path.abspath(os.path.join('Assets', 'data'))
PATH_EXE = os.path.abspath(os.path.join('Assets'))

# *****************************************************************************


def calibration_daemon():

    # Get calibration parameters
    with open(os.path.join('Assets', 'param_dict.json')) as fid01:
        param_dict = json.load(fid01)

    calib_dict = param_dict['EXP_OPTIMIZE']
    gen_params = {'NUM_SIMS': param_dict['NUM_SIMS'],
                  'VAR_NAMES': [pname for pname in calib_dict],
                  'VAR_RANGES': [calib_dict[pname] for pname in calib_dict]}

    # Set base name
    EXP_BASE_NAME = param_dict['EXP_NAME']

    # Prepare the platform
    plat_obj = Platform(block='COMPS',
                        endpoint='https://comps.idmod.org',
                        environment='Calculon',
                        priority='Normal',
                        simulation_root='$COMPS_PATH(USER)',
                        node_group='idm_abcd',
                        num_cores='1',
                        num_retries='0',
                        exclusive='False')

    # Iterate
    for inum in range(param_dict['NUM_ITER']):

        # Create summary data object
        sum_data = {pname: list() for pname in calib_dict}
        obj_data = list()
        for k2 in range(inum):
            with open('param_dict_iter{:02d}.json'.format(k2)) as fid01:
                temp_params = json.load(fid01)
            for var_name in sum_data:
                var_vec = temp_params['EXP_VARIABLE'][var_name]
                sum_data[var_name].extend(var_vec)

            obj_temp = temp_params['NUM_SIMS']*[EX_VAL]
            with open('data_brick_iter{:02d}.json'.format(k2)) as fid01:
                temp_objfun = json.load(fid01)
            for var_name in temp_objfun:
                if (var_name.isdecimal()):
                    obj_temp[int(var_name)] = temp_objfun[var_name]['cal_val']
            obj_data.extend(obj_temp)

        sum_data['OBJ_FUN'] = obj_data

        # Next point algorithm
        param_out = next_point_alg(gen_params, sum_data, EX_VAL)

        # Create new experiment definition file
        param_dict_new = param_dict
        param_dict_new['EXP_NAME'] = EXP_BASE_NAME + '_iter{:02d}'.format(inum)
        param_dict_new['NUM_SIMS'] = gen_params['NUM_SIMS']
        for var_name in param_out:
            param_dict_new['EXP_VARIABLE'][var_name] = param_out[var_name]

        # Save experiment definition to calibration object
        PATH_EXP_DEF = os.path.abspath('param_dict.json')
        with open(PATH_EXP_DEF, 'w') as fid01:
            json.dump(param_dict_new, fid01)

        # Create experiment object
        exp_obj_new = exp_from_def_file(PATH_EXP_DEF,
                                        PATH_PYTHON,
                                        PATH_EXE,
                                        PATH_DATA)

        # Send experiment to COMPS; start processing; wait until done
        plat_obj.run_items(exp_obj_new)
        plat_obj.wait_till_done(exp_obj_new)

        # Save experiment id to file
        write_id_file('COMPS_ID_iter{:02d}.id'.format(inum), exp_obj_new)

        # Save reduced data to calibration object
        pool_manager(exp_obj_new.id)
        os.rename('data_brick.json', 'data_brick_iter{:02d}.json'.format(inum))
        os.rename('param_dict.json', 'param_dict_iter{:02d}.json'.format(inum))

    return None

# *****************************************************************************


if (__name__ == "__main__"):

    calibration_daemon()

# *****************************************************************************
