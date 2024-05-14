# *****************************************************************************
#
# *****************************************************************************

import json
import os
import sqlite3

import global_data as gdata

import numpy as np

from emod_api_func import post_proc_poppyr
from emod_constants import SQL_TIME, SQL_MCW, SQL_AGE

# *****************************************************************************


def application(output_path):

    # Prep output dictionary
    SIM_IDX = gdata.sim_index
    key_str = '{:05d}'.format(SIM_IDX)
    parsed_dat = {key_str: dict()}

    # Sample population pyramid every year
    post_proc_poppyr(output_path, parsed_dat[key_str])

    # Connect to SQL database; retreive new entries
    connection_obj = sqlite3.connect('simulation_events.db')
    cursor_obj = connection_obj.cursor()

    sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME >= {:.1f}".format(0.0)
    cursor_obj.execute(sql_cmd)
    rlist = cursor_obj.fetchall()

    data_vec_time = np.array([val[SQL_TIME] for val in rlist], dtype=float)
    data_vec_mcw = np.array([val[SQL_MCW] for val in rlist], dtype=float)
    data_vec_age = np.array([val[SQL_AGE] for val in rlist], dtype=float)

    # Aggregate new infections by month
    DAY_BINS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    START_TIME = 365.0*(gdata.start_year-gdata.base_year)
    BIN_EDGES = np.cumsum(int(gdata.run_years)*DAY_BINS) + START_TIME - 0.5
    BIN_EDGES = np.insert(BIN_EDGES, 0, START_TIME - 0.5)

    (inf_mo, tstamps) = np.histogram(data_vec_time,
                                     bins=BIN_EDGES,
                                     weights=data_vec_mcw)

    # Monthly timeseries
    parsed_dat[key_str]['timeseries'] = inf_mo.tolist()

    # Age at infection histograms by year
    YR_BINS = [365]
    START_TIME = 365.0*(gdata.start_year-gdata.base_year)
    BIN_EDGES = np.cumsum(int(gdata.run_years)*YR_BINS) + START_TIME - 0.5
    BIN_EDGES = np.insert(BIN_EDGES, 0, START_TIME - 0.5)

    parsed_dat[key_str]['age_data'] = list()
    for k1 in range(len(BIN_EDGES)-1):
        idx = (data_vec_time >= BIN_EDGES[k1]) & \
              (data_vec_time < BIN_EDGES[k1+1])
        age_dat = data_vec_age[idx]
        mcw_dat = data_vec_mcw[idx]
        (age_hist, _) = np.histogram(age_dat,
                                     bins=np.array(gdata.AGE_HIST_BINS)*365.0,
                                     weights=mcw_dat)
        parsed_dat[key_str]['age_data'].append(age_hist.tolist())

    # Retain infected fraction timeseries
    with open(os.path.join(output_path, 'InsetChart.json')) as fid01:
        inset_chart = json.load(fid01)

    ic_start = inset_chart['Header']['Start_Time']
    ic_nstep = inset_chart['Header']['Timesteps']
    ic_tsize = inset_chart['Header']['Simulation_Timestep']
    inf_frac_vec = np.array(inset_chart['Channels']['Infected']['Data'])

    parsed_dat[key_str]['inf_frac_vec'] = inf_frac_vec.tolist()

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
