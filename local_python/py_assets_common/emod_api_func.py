# *****************************************************************************
#
# *****************************************************************************

import json
import os
import time
import struct

import global_data as gdata

from builder_config import update_config_obj
from builder_demographics import demographicsBuilder
from builder_campaign import campaignBuilder
from builder_dlls import dllcBuilder

import numpy as np

from emod_api import __version__ as API_CUR

from emod_api.config import default_from_schema_no_validation as dfs

from emod_constants import API_MIN, P_FILE, I_FILE, C_FILE, EXP_C, EXP_V, \
                           AGE_KEY_LIST, YR_DAYS, POP_PYR, SPATH, CBR_VEC, \
                           NODE_IDS_STR, NODE_POP_STR, INF_FRAC, RST_FILE, \
                           RST_TIME, RST_CONT_INF, RST_CONT_TOT, R0_VEC

# *****************************************************************************


def configBuilder():

    default_conf = dfs.get_default_config_from_schema(SPATH, as_rod=True)

    # Probably ought to be an emod-api call
    config_obj = update_config_obj(default_conf)
    config_obj.parameters.finalize()
    with open(C_FILE, 'w') as fid01:
        json.dump(config_obj, fid01, sort_keys=True, indent=4)

    return C_FILE

# *****************************************************************************


def standard_pre_process():

    # Declare current version of emod-api; check min version
    print('Using emod-api {:s}'.format(API_CUR))
    for ver_val in zip(API_CUR.split('.'), API_MIN.split('.')):
        if (ver_val[0] > ver_val[1]):
            break
        if (ver_val[0] == ver_val[1]):
            continue
        if (ver_val[0] < ver_val[1]):
            err_text = 'Using emod-api {:s}; minimum version is {:s}'
            raise Exception(err_text.format(API_CUR, API_MIN))

    # Read index of simulation parameter set
    with open(I_FILE) as fid01:
        sim_index = int(fid01.readline())
    gdata.sim_index = sim_index

    # Read parameter dictionary file
    param_dict = dict()
    param_paths = ['.', 'Assets']

    for ppath in param_paths:
        pfileopt = os.path.join(ppath, P_FILE)
        if (os.path.exists(pfileopt)):
            with open(pfileopt) as fid01:
                param_dict = json.load(fid01)
            break

    # Validation checks on parameter dictionary file
    if (not param_dict):
        raise Exception('No {:s} found'.format(P_FILE))

    names_variable = set(param_dict[EXP_V].keys())
    names_constant = set(param_dict[EXP_C].keys())
    if (names_constant.intersection(names_variable)):
        err_text = 'Variable name in both {:s} and {:s}'
        raise Exception(err_text.format(EXP_C, EXP_V))

    # Select simulation parameters from parameters dictionary, save in globals
    var_params = dict()

    var_params.update({keyval: param_dict[EXP_V][keyval][sim_index]
                       for keyval in param_dict[EXP_V]})
    var_params.update({keyval: param_dict[EXP_C][keyval]
                       for keyval in param_dict[EXP_C]})

    gdata.var_params = var_params

    # Seed random number generator
    np.random.seed(sim_index)

    # Demographics file
    demographicsBuilder()
    time.sleep(1)

    # Campaign interventions file
    campaignBuilder()
    time.sleep(1)

    # Custom reporter file
    dllcBuilder()
    time.sleep(1)

    # Simulation configuration file
    config_filename = configBuilder()
    time.sleep(1)

    return config_filename

# *****************************************************************************


def post_proc_poppyr(output_path, parsed_out):

    # Sample population pyramid every year
    with open(os.path.join(output_path, 'DemographicsSummary.json')) as fid01:
        demog_output = json.load(fid01)

    ds_start = demog_output['Header']['Start_Time']
    ds_nstep = demog_output['Header']['Timesteps']
    ds_tsize = demog_output['Header']['Simulation_Timestep']
    time_vec = np.arange(ds_nstep)*ds_tsize + ds_start
    nyr_bool = (np.diff(time_vec//YR_DAYS) > 0.0)
    run_yrs = ds_nstep*ds_tsize/YR_DAYS

    pyr_dat = np.zeros((int(run_yrs)+1, len(AGE_KEY_LIST)))

    for k1 in range(len(AGE_KEY_LIST)):
        age_key_str = 'Population Age {:s}'.format(AGE_KEY_LIST[k1])
        age_vec_dat = np.array(demog_output['Channels'][age_key_str]['Data'])
        pyr_dat[0, k1] = age_vec_dat[0]
        age_subset = age_vec_dat[:-1][nyr_bool]
        if (age_subset.shape[0] < int(run_yrs)):
            age_subset = np.append(age_subset, age_vec_dat[-1])
        pyr_dat[1:, k1] = age_subset

    parsed_out[POP_PYR] = pyr_dat.tolist()

    return None

# *****************************************************************************


def post_proc_cbr(output_path, parsed_out):

    # Retain annualized count of births
    with open(os.path.join(output_path, 'InsetChart.json')) as fid01:
        inset_chart = json.load(fid01)

    ic_start = inset_chart['Header']['Start_Time']
    ic_nstep = inset_chart['Header']['Timesteps']
    ic_tsize = inset_chart['Header']['Simulation_Timestep']
    cumb_vec = np.array(inset_chart['Channels']['Births']['Data'])

    time_vec = np.arange(ic_nstep)*ic_tsize + ic_start
    nyr_bool = (np.diff(time_vec//365.0) > 0.0)
    run_years = (ic_nstep*ic_tsize)//365.0
    b_vec = cumb_vec[:-1][nyr_bool]
    if (b_vec.shape[0] < run_years):
        b_vec = np.append(b_vec, cumb_vec[-1])
    b_vec[1:] = np.diff(b_vec)

    parsed_out[CBR_VEC] = b_vec.tolist()

    return None

# *****************************************************************************


def post_proc_nodepop(output_path, parsed_out):

    # Population data from Spatial_Output_Channels = ["Population"]
    fname = 'SpatialReport_Population.bin'
    with open(os.path.join(output_path, fname), mode='rb') as fid01:
        sr_data = fid01.read()

    # Struct output is tuple even when single value
    num_nodes = struct.unpack("i", sr_data[0:4])[0]
    num_times = struct.unpack("i", sr_data[4:8])[0]
    node_ids = struct.unpack("i"*num_nodes,
                             sr_data[8:(8+4*num_nodes)])
    sim_data = struct.unpack("f"*num_nodes*num_times,
                             sr_data[(8+4*num_nodes):])

    # Construct numpy data structures
    node_id_vec = np.array([val for val in node_ids])
    pop_mat = np.reshape(np.array([val for val in sim_data]), (num_times, -1))

    parsed_out[NODE_IDS_STR] = node_id_vec.tolist()
    parsed_out[NODE_POP_STR] = pop_mat.tolist()

    return None

# *****************************************************************************


def post_proc_prev(output_path, parsed_out):

    # Retain timeseries of infected fraction
    with open(os.path.join(output_path, 'InsetChart.json')) as fid01:
        inset_chart = json.load(fid01)

    inf_frac_vec = np.array(inset_chart['Channels']['Infected']['Data'])

    parsed_out[INF_FRAC] = inf_frac_vec.tolist()

    return None

# *****************************************************************************


def post_proc_R0(output_path, parsed_out):

    # Retain timeseries of infected fraction
    with open(os.path.join(output_path, RST_FILE)) as fid01:
        rst_dat = np.loadtxt(fid01, delimiter=',', skiprows=1)

    rst_time_vec = rst_dat[:, RST_TIME]
    rst_cont_vec = rst_dat[:, RST_CONT_TOT]
    rst_infs_vec = rst_dat[:, RST_CONT_INF]
    np_eps = np.finfo(float).eps

    tot_contagion = rst_cont_vec
    tot_infection = rst_infs_vec

    est_r0_vec = tot_contagion/(tot_infection+np_eps)

    parsed_out[R0_VEC] = est_r0_vec.tolist()

    return None

# *****************************************************************************
