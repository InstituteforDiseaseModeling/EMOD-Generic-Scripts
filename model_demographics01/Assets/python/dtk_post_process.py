# *****************************************************************************
#
# *****************************************************************************

import json

import global_data as gdata

import numpy as np

from emod_api_func import post_proc_poppyr
from emod_constants import POP_PYR

# *****************************************************************************

uk_1950_frac = [0.0000, 0.0863, 0.0719, 0.0663, 0.0631, 0.0680, 0.0768, 0.0691,
                0.0769, 0.0766, 0.0713, 0.0625, 0.0546, 0.0482, 0.0410, 0.0319,
                0.0206, 0.0103, 0.0036, 0.0008, 0.0001]

uk_1960_frac = [0.0000, 0.0783, 0.0718, 0.0814, 0.0693, 0.0632, 0.0627, 0.0653,
                0.0716, 0.0644, 0.0703, 0.0688, 0.0631, 0.0519, 0.0423, 0.0330,
                0.0228, 0.0131, 0.0050, 0.0012, 0.0002]

uk_1970_frac = [0.0000, 0.0839, 0.0849, 0.0729, 0.0683, 0.0763, 0.0641, 0.0592,
                0.0580, 0.0606, 0.0655, 0.0572, 0.0613, 0.0576, 0.0485, 0.0353,
                0.0239, 0.0142, 0.0063, 0.0018, 0.0003]

uk_1980_frac = [0.0000, 0.0602, 0.0687, 0.0814, 0.0843, 0.0729, 0.0673, 0.0740,
                0.0617, 0.0570, 0.0556, 0.0572, 0.0600, 0.0503, 0.0504, 0.0423,
                0.0298, 0.0166, 0.0075, 0.0024, 0.0004]

tpop_yval = [50616014, 50601935, 50651280, 50750976, 50890915, 51063902,
             51265880, 51495702, 51754673, 52045662, 52370602, 52727768,
             53109399, 53500716, 53882751, 54240850, 54568868, 54866534,
             55132596, 55367947, 55573453, 55748531, 55892418, 56006296,
             56092066, 56152333, 56188348, 56203595, 56205913, 56205083,
             56209171]

# *****************************************************************************


def application(output_path):

    # Prep output dictionary
    SIM_IDX = gdata.sim_index
    key_str = '{:05d}'.format(SIM_IDX)
    parsed_dat = {key_str: dict()}

    # Sample population pyramid every year
    post_proc_poppyr(output_path, parsed_dat[key_str])

    # Calculate calibration score
    pyr_dat = np.array(parsed_dat[key_str][POP_PYR])
    err_score = 0

    sim_pop = np.sum(pyr_dat, axis=1)
    ref_pop = 100000*np.array(tpop_yval)/tpop_yval[0]
    sum_val = np.sum(np.power(100*(sim_pop-ref_pop)/ref_pop, 2.0))
    err_score = err_score + np.sqrt(sum_val)

    simpyr1950 = pyr_dat[0, :]/np.sum(pyr_dat[0, :])
    refpyr1950 = np.array(uk_1950_frac[1:])
    sum_val = np.sum(np.power(100*(simpyr1950-refpyr1950), 2.0))
    err_score = err_score + np.sqrt(sum_val)

    simpyr1960 = pyr_dat[10, :]/np.sum(pyr_dat[10, :])
    refpyr1960 = np.array(uk_1960_frac[1:])
    sum_val = np.sum(np.power(100*(simpyr1960-refpyr1960), 2.0))
    err_score = err_score + np.sqrt(sum_val)

    simpyr1970 = pyr_dat[20, :]/np.sum(pyr_dat[20, :])
    refpyr1970 = np.array(uk_1970_frac[1:])
    sum_val = np.sum(np.power(100*(simpyr1970-refpyr1970), 2.0))
    err_score = err_score + np.sqrt(sum_val)

    simpyr1980 = pyr_dat[30, :]/np.sum(pyr_dat[30, :])
    refpyr1980 = np.array(uk_1980_frac[1:])
    sum_val = np.sum(np.power(100*(simpyr1980-refpyr1980), 2.0))
    err_score = err_score + np.sqrt(sum_val)

    parsed_dat[key_str]['cal_val'] = -float(err_score)

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
