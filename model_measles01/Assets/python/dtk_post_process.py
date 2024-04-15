# *****************************************************************************
#
# *****************************************************************************

import json
import sqlite3

import global_data as gdata

import numpy as np

from emod_api_func import post_proc_poppyr
from emod_constants import SQL_TIME, SQL_MCW, SQL_AGE

# *****************************************************************************

AGE_HIST_BINS = np.arange(0,2,1/12).tolist() + \
                [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

# NGA 2019 CFR; IHME 2023
IHME_MORT_X = np.arange(0,  5, 1/12).tolist() + \
              np.arange(5, 41, 1   ).tolist()
IHME_MORT_Y = [0.02871109,0.02624552,0.0242363 ,0.02261083,0.02131237, 0.02029702,
               0.01953139,0.0189909 ,0.01865851,0.01845707,0.01824601, 0.01802163,
               0.01778448,0.01753512,0.01727415,0.01700218,0.01672054, 0.01644462,
               0.01618027,0.01592708,0.01568466,0.01545264,0.01523068, 0.01501844,
               0.01481561,0.01462189,0.014437  ,0.01426067,0.01409264, 0.01393269,
               0.01378057,0.01363608,0.01349901,0.01336917,0.01324637, 0.01313046,
               0.01302127,0.01291865,0.01282247,0.01273258,0.01264888, 0.01257124,
               0.01249957,0.01243377,0.01237375,0.01231943,0.01227074, 0.01222493,
               0.01217928,0.0121338 ,0.0120885 ,0.01204336,0.01199838, 0.01195357,
               0.01190893,0.01186445,0.01182014,0.01177598,0.011732  , 0.01168817,
               0.01164451,0.01113295,0.01064362,0.01017558,0.00972792, 0.00929977,
               0.00889029,0.00849869,0.00812419,0.00776607,0.00742362, 0.00709616,
               0.00678304,0.00648365,0.00619739,0.0059237 ,0.00566203, 0.00541185,
               0.00517266,0.004944  ,0.0047254 ,0.00451641,0.00431663, 0.00412565,
               0.00394309,0.00376858,0.00360176,0.0034423 ,0.00328987, 0.00314418,
               0.00300491,0.0028718 ,0.00274457,0.00262296,0.00250672, 0.00239563]

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
    BIN_EDGES = np.cumsum(int(gdata.run_years)*DAY_BINS) + START_TIME + 0.5
    BIN_EDGES = np.insert(BIN_EDGES, 0, START_TIME + 0.5)

    (inf_mo, tstamps) = np.histogram(data_vec_time,
                                     bins=BIN_EDGES,
                                     weights=data_vec_mcw)

    # Monthly timeseries
    parsed_dat[key_str]['timeseries'] = inf_mo.tolist()

    # Age at infection histograms by year
    YR_BINS = [365]
    START_TIME = 365.0*(gdata.start_year-gdata.base_year)
    BIN_EDGES = np.cumsum(int(gdata.run_years)*YR_BINS) + START_TIME + 0.5
    BIN_EDGES = np.insert(BIN_EDGES, 0, START_TIME + 0.5)

    parsed_dat[key_str]['age_data'] = list()
    for k1 in range(len(BIN_EDGES)-1):
        idx = (data_vec_time >= BIN_EDGES[k1]) & (data_vec_time < BIN_EDGES[k1+1])
        age_dat = data_vec_age[idx]
        mcw_dat = data_vec_mcw[idx]
        (age_hist, _) = np.histogram(age_dat,
                                     bins=np.array(AGE_HIST_BINS)*365.0,
                                     weights=mcw_dat)
        parsed_dat[key_str]['age_data'].append(age_hist.tolist())

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
