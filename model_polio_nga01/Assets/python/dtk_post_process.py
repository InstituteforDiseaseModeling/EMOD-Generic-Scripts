# *****************************************************************************
#
# *****************************************************************************

import json
import os

import global_data as gdata

import numpy as np

from emod_constants import RST_FILE, RST_TIME, RST_NODE, RST_CLADE, \
                           RST_GENOME, RST_NEW_INF

# *****************************************************************************


def application(output_path):

    # Prep output dictionary
    SIM_IDX = gdata.sim_index
    key_str = '{:05d}'.format(SIM_IDX)
    parsed_dat = {key_str: dict()}

    REP_MAP_DICT = gdata.demog_node_map    # LGA Dotname: [NodeIDs]
    REP_DEX_DICT = gdata.demog_rep_index   # LGA Dotname: Output row number

    # Variables for this simulation
    START_YEAR = gdata.var_params['start_year']
    TIME_DELTA = 365.0*gdata.run_years
    cVDPV_genome = gdata.boxes_sabin2 + gdata.boxes_nopv2

    # Timesteps
    t_ini = 365.0*(START_YEAR-gdata.base_year)
    t_end = t_ini + 365.0*gdata.run_years
    t_vec = np.arange(t_ini, t_end+1, gdata.t_step_days)

    # Post-process strain reporter
    strain_dat = np.loadtxt(os.path.join(output_path, RST_FILE),
                            delimiter=',', skiprows=1, ndmin=2)

    # Construct csv file for cVDPV infections
    node_reps = list(REP_DEX_DICT.keys())
    dbrick0 = np.zeros((len(node_reps), t_vec.shape[0]))

    if(strain_dat.shape[0] > 0):
        for rep_name in node_reps:
            brick_dex = REP_DEX_DICT[rep_name]
            gidx = (strain_dat[:, RST_CLADE]==0) & (strain_dat[:, RST_GENOME]==cVDPV_genome)
            rep_bool = np.isin(strain_dat[:, RST_NODE], REP_MAP_DICT[rep_name]) & gidx
            targ_dat = strain_dat[rep_bool, :]
            for k1 in range(targ_dat.shape[0]):
                time_dex = int((targ_dat[k1, RST_TIME]-t_ini)/gdata.t_step_days)
                dbrick0[brick_dex, time_dex] += targ_dat[k1, RST_NEW_INF]

    np.savetxt(os.path.join(output_path,'lga_timeseries.csv'),
               dbrick0, fmt='%.0f', delimiter=',')

    # Log data for local machine
    fatime = np.argmax(dbrick0, axis=1)
    totinf = np.sum(dbrick0, axis=0)

    parsed_dat[key_str]['fatime'] = fatime.tolist()
    parsed_dat[key_str]['totinf'] = totinf.tolist()
    parsed_dat['t_vec'] = t_vec.tolist()
    parsed_dat['node_names'] = REP_DEX_DICT

    # Write output dictionary
    with open('parsed_out.json', 'w') as fid01:
        json.dump(parsed_dat, fid01)

    return None

# *****************************************************************************
