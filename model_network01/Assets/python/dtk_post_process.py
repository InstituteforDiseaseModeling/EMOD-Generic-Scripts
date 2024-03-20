# *****************************************************************************
#
# *****************************************************************************

import json
import sqlite3

import global_data as gdata

import numpy as np

# *****************************************************************************


def application(output_path):

    # Prep output dictionary
    SIM_IDX = gdata.sim_index
    key_str = '{:05d}'.format(SIM_IDX)
    parsed_dat = {key_str: dict()}

    # Connect to SQL database; retreive new entries
    connection_obj = sqlite3.connect('simulation_events.db')
    cursor_obj = connection_obj.cursor()

    sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(0.0)
    cursor_obj.execute(sql_cmd)
    row_list = cursor_obj.fetchall()

    dvec_time = np.array([val[0] for val in row_list], dtype=float)  # Time
    dvec_node = np.array([val[2] for val in row_list], dtype=int)    # Node
    dvec_mcwt = np.array([val[4] for val in row_list], dtype=float)  # MCW

    # Daily timeseries for each node
    max_time = np.max(dvec_time)+10
    max_node = np.max(dvec_node)
    bin_edges = np.arange(0.5, max_time+1)
    inf_dat = np.zeros((int(max_node), int(max_time)))
    for k1 in range(inf_dat.shape[0]):
        idx = (dvec_node == k1+1)
        (inf_day, _) = np.histogram(dvec_time[idx],
                                    bins=bin_edges,
                                    weights=dvec_mcwt[idx])
        inf_dat[k1, :] = inf_day
    parsed_dat[key_str]['inf_data'] = inf_dat.tolist()

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
