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

  DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
  BIN_EDGES = np.cumsum(15*DAY_BINS) + gdata.start_log + 0.5  # Hist for 15 years
  BIN_EDGES = np.insert(BIN_EDGES, 0, gdata.start_log + 0.5)

  SIM_IDX         = gdata.sim_index
  PREV_TIME       = gdata.prev_proc_time
  REP_MAP_DICT    = gdata.demog_node_map    # LGA Dotname:     [NodeIDs]
  NODEID_DICT     = gdata.demog_node        # Node Dotname:    ForcedID
  TIME_START      = gdata.start_time


  # ***** Get variables for this simulation *****
  TIME_DELTA      = gdata.var_params['num_tsteps']


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(PREV_TIME)
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  data_time = np.array([val[0] for val in row_list], dtype = float)  # Time
  data_node = np.array([val[2] for val in row_list], dtype = int  )  # Node
  data_mcw  = np.array([val[4] for val in row_list], dtype = float)  # MCW

  gdata.data_vec_time = np.append(gdata.data_vec_time, data_time)
  gdata.data_vec_node = np.append(gdata.data_vec_node, data_node)
  gdata.data_vec_mcw  = np.append(gdata.data_vec_mcw,  data_mcw)


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}
  calval_dat = {key_str: dict()}


  # Timestamps
  time_vec = np.arange(TIME_START, TIME_START + TIME_DELTA)


  # Aggregate new infections to timeseries by month, by admin01
  adm1_list  = list(set([val.rsplit(':',1)[0] for val in REP_MAP_DICT.keys()]))
  adm1_dict  = {adm1:[NODEID_DICT[val] for val in NODEID_DICT.keys() if val.startswith(adm1+':')]
                                       for adm1 in adm1_list}

  for adm1_name in adm1_dict:
    rep_bool          = np.isin(gdata.data_vec_node,adm1_dict[adm1_name])
    (inf_mo, tstamps) = np.histogram(gdata.data_vec_time[rep_bool],
                                     bins    = BIN_EDGES,
                                     weights = gdata.data_vec_mcw[rep_bool])

    parsed_dat[key_str][adm1_name] = inf_mo.tolist()


  # Calibration score from timeseries data
  #(obj_val, scal_vec) = norpois_opt([ref_dat], inf_mo[:len(ref_dat)])

  #calval_dat[key_str]              = float(obj_val)
  #parsed_dat[key_str]['rep_rate']  = float(scal_vec[0])


  # Sample total population pyramid every year
  with open(os.path.join(output_path,'DemographicsSummary.json')) as fid01:
    demog_output = json.load(fid01)

  age_key_list = [   '<5',   '5-9', '10-14', '15-19', '20-24', '25-29',
                  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
                  '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
                  '90-94', '95-99']
  pyr_dat      = np.zeros((int(np.floor(TIME_DELTA/365.0))+1,len(age_key_list)))

  for k1 in range(len(age_key_list)):
    age_key_str = 'Population Age {:s}'.format(age_key_list[k1])
    age_vec_dat = np.array(demog_output['Channels'][age_key_str]['Data'])
    pyr_dat[0,  k1] = age_vec_dat[0]
    pyr_dat[1:, k1] = age_vec_dat[364::365]

  parsed_dat[key_str]['pyramid'] = pyr_dat.tolist()


  # Common output data
  parsed_dat['tstamps'] = (np.diff(tstamps)/2.0 + tstamps[:-1]).tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  # Write calibration score
  with open('calval_out.json','w') as fid01:
    json.dump(calval_dat, fid01)


  return None

#*******************************************************************************
