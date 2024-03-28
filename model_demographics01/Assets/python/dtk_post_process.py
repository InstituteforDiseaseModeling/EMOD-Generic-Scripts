# *****************************************************************************
#
# *****************************************************************************

import json

import global_data as gdata

import numpy as np

from emod_api_func import post_proc_poppyr
from emod_constants import POP_PYR

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

    # Error from total pop (every year)
    sim_pop = np.sum(pyr_dat, axis=1)
    ref_pop = np.sum(gdata.pop_mat_ref, axis=0)
    sum_val = np.sum(np.power(100*(sim_pop-ref_pop)/ref_pop, 2.0))
    err_score = err_score + np.sqrt(sum_val)

    # Error from pyramid shape (every decade)
    for yr_idx in range(0, int(gdata.run_years)+1, 10):
        sim_pyr = pyr_dat[yr_idx, :]/np.sum(pyr_dat[yr_idx, :])
        ref_pyr = np.array(gdata.pop_mat_ref[:, yr_idx])
        sum_val = np.sum(np.power(100*(sim_pyr-ref_pyr), 2.0))
        err_score = err_score + np.sqrt(sum_val)

    # Record calibration score
    parsed_dat[key_str]['cal_val'] = -float(err_score)

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
