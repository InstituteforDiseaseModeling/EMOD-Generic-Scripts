#********************************************************************************
#
#********************************************************************************

import os, sys, shutil, json, sqlite3

import global_data as gdata

import numpy as np

from aux_obj_calc     import     norpois_opt

#********************************************************************************

pop_age_days  = [     0,   1825,   3650,   5475,   7300,   9125,  10950,  12775,
                  14600,  16425,  18250,  20075,  21900,  23725,  25550,  27375,
                  29200,  31025,  32850,  34675,  36500]

nga_2010_frac = []

nga_2020_frac = []

tpop_xval = []

tpop_yval = []

ref_dat   = []

#********************************************************************************

def application(output_path):

  RUN_YEARS       = gdata.run_years
  BASE_YEAR       = gdata.base_year
  TIME_STEP       = gdata.t_step_days
  START_LOG_TIME  = gdata.start_log_time

  SIM_IDX         = gdata.sim_index
  PREV_TIME       = gdata.prev_proc_time
  REP_MAP_DICT    = gdata.demog_node_map    # LGA Dotname:     [NodeIDs]
  NODEID_DICT     = gdata.demog_node        # Node Dotname:    ForcedID


  # ***** Get variables for this simulation *****
  START_YEAR      = gdata.var_params['start_year']
  RUN_YEARS       = gdata.var_params['run_years']


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(PREV_TIME)
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  data_time = np.array([val[0] for val in row_list], dtype = float)  # Time
  data_node = np.array([val[2] for val in row_list], dtype = int  )  # Node
  data_mcw  = np.array([val[4] for val in row_list], dtype = float)  # MCW
  data_age  = np.array([val[5] for val in row_list], dtype = float)  # Age

  gdata.data_vec_time = np.append(gdata.data_vec_time, data_time)
  gdata.data_vec_node = np.append(gdata.data_vec_node, data_node)
  gdata.data_vec_mcw  = np.append(gdata.data_vec_mcw,  data_mcw)
  gdata.data_vec_age  = np.append(gdata.data_vec_mcw,  data_age)


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Aggregate new infections to timeseries by month, by admin01
  DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
  BIN_EDGES = np.cumsum(15*DAY_BINS) + START_LOG_TIME + 0.5  # Hist for 15 years
  BIN_EDGES = np.insert(BIN_EDGES, 0, START_LOG_TIME + 0.5)

  adm1_list  = list(set([val.rsplit(':',1)[0] for val in REP_MAP_DICT.keys()]))
  adm1_dict  = {adm1:[NODEID_DICT[val] for val in NODEID_DICT.keys() if val.startswith(adm1+':')]
                                       for adm1 in adm1_list}

  for adm1_name in adm1_dict:
    rep_bool          = np.isin(gdata.data_vec_node,adm1_dict[adm1_name])
    (inf_mo, tstamps) = np.histogram(gdata.data_vec_time[rep_bool],
                                     bins    = BIN_EDGES,
                                     weights = gdata.data_vec_mcw[rep_bool])

    parsed_dat[key_str][adm1_name] = inf_mo.tolist()


  # Sample population pyramid at start, then every year
  with open(os.path.join(output_path,'DemographicsSummary.json')) as fid01:
    demog_output = json.load(fid01)

  ds_start = demog_output['Header']['Start_Time']
  ds_nstep = demog_output['Header']['Timesteps']
  ds_tsize = demog_output['Header']['Simulation_Timestep']
  time_vec = np.arange(ds_nstep)*ds_tsize + ds_start
  nyr_bool = (np.diff(time_vec//365.0)>0.0)

  age_key_list = [   '<5',   '5-9', '10-14', '15-19', '20-24', '25-29',
                  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
                  '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
                  '90-94', '95-99']
  pyr_dat      = np.zeros((int(RUN_YEARS)+1,len(age_key_list)))

  for k1 in range(len(age_key_list)):
    age_key_str = 'Population Age {:s}'.format(age_key_list[k1])
    age_vec_dat = np.array(demog_output['Channels'][age_key_str]['Data'])
    pyr_dat[0,  k1] = age_vec_dat[0]
    age_subset      = age_vec_dat[:-1][nyr_bool]
    if(age_subset.shape[0] < int(RUN_YEARS)):
      age_subset = np.append(age_subset, age_vec_dat[-1])
    pyr_dat[1:, k1] = age_subset

  parsed_dat[key_str]['pyramid'] = pyr_dat.tolist()


  # Calibration score from timeseries data
  #(err_score, scal_vec) = norpois_opt([ref_dat], inf_mo[:len(ref_dat)])
  err_score = 0

  parsed_dat[key_str]['cal_val']   = float(err_score)
  #parsed_dat[key_str]['rep_rate']  = float(scal_vec[0])


  # Common output data
  parsed_dat['tstamps'] = (np.diff(tstamps)/2.0 + tstamps[:-1]).tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
