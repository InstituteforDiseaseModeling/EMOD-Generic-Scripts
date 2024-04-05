# *****************************************************************************
#
# *****************************************************************************

import json
import sqlite3

import global_data as gdata

import numpy as np

from emod_api_func import post_proc_poppyr, post_proc_cbr
from emod_constants import SQL_TIME, SQL_MCW, SQL_AGE, POP_AGE_DAYS

# *****************************************************************************


def application(output_path):

    # Prep output dictionary
    SIM_IDX = gdata.sim_index
    key_str = '{:05d}'.format(SIM_IDX)
    parsed_dat = {key_str: dict()}

    # Sample population pyramid every year
    post_proc_poppyr(output_path, parsed_dat[key_str])

    # Retain annualized count of births
    post_proc_cbr(output_path, parsed_dat[key_str])

    # Connect to SQL database; retreive new entries
    connection_obj = sqlite3.connect('simulation_events.db')
    cursor_obj = connection_obj.cursor()

    sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME >= {:.1f}".format(0.0)
    cursor_obj.execute(sql_cmd)
    rlist = cursor_obj.fetchall()

    data_vec_time = np.array([val[SQL_TIME] for val in rlist], dtype=float)
    data_vec_mcw = np.array([val[SQL_MCW] for val in rlist], dtype=float)
    data_vec_age = np.array([val[SQL_AGE] for val in rlist], dtype=float)

    # Yearly timeseries by age
    DAY_BINS = [365]
    START_TIME = 365.0*(gdata.start_year-gdata.base_year)
    BIN_EDGES = np.cumsum(int(gdata.run_years)*DAY_BINS) + START_TIME + 0.5
    BIN_EDGES = np.insert(BIN_EDGES, 0, START_TIME + 0.5)

    inf_dat = np.zeros((int(gdata.run_years), len(POP_AGE_DAYS)-1))
    for k1 in range(inf_dat.shape[1]):
        idx = (data_vec_age >= POP_AGE_DAYS[k1]) & \
              (data_vec_age < POP_AGE_DAYS[k1+1])
        (inf_yr, tstamps) = np.histogram(data_vec_time[idx],
                                         bins=BIN_EDGES,
                                         weights=data_vec_mcw[idx])
        inf_dat[:, k1] = inf_yr
    parsed_dat[key_str]['inf_data'] = inf_dat.tolist()

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
