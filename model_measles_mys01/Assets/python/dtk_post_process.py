#********************************************************************************
#
#********************************************************************************

import os, sys, shutil, json, sqlite3

import global_data as gdata

import numpy as np

from aux_obj_calc     import     norpois_opt

#********************************************************************************

ref_dat_01 = [216, 244, 203, 189, 155, 113,  70, 104,  88,  78,  60,  67,
               77,  61, 122, 142, 186, 139, 198, 194, 157, 172, 140, 105,
              115, 135, 152, 226, 244, 171, 204, 159, 137, 152, 149, 114,
               80,  91,  93,  71,  70, 129, 112, 105,  65,  88,  96,  77,
               74, 104,  94,  30,  15,  29,  27,  30,  13,  22,  19,  20,
               10,  11,  18,  20,  13,   8,   5,   6,   3,  11,  13,  10,
               12,   7,  11,   9,  17,  13,  11,  27,  19,  33,  27,  23,
               16,  26,  64,  79, 103,  56,   0,   0,   0,   0,   0,   0]

#********************************************************************************

def application(output_path):

  BASE_YEAR      = gdata.base_year
  START_YEAR     = gdata.start_year
  START_LOG      = gdata.start_log

  SIM_IDX        = gdata.sim_index
  PREV_TIME      = gdata.prev_proc_time
  REP_MAP_DICT   = gdata.demog_node_map    # LGA Dotname:     [NodeIDs]


  LOG_TIME  = 365.0*(START_LOG-BASE_YEAR)
  DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
  BIN_EDGES = np.cumsum(10*DAY_BINS) + LOG_TIME + 0.5  # Hist for 10 years
  BIN_EDGES = np.insert(BIN_EDGES, 0, LOG_TIME + 0.5)


  # ***** Get variables for this simulation *****
  RUN_YEARS      = gdata.var_params['run_years']


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


  # Aggregate new infections by month
  (inf_mo, tstamps) = np.histogram(gdata.data_vec_time,
                                   bins    = BIN_EDGES,
                                   weights = gdata.data_vec_mcw)


  # Monthly timeseries
  parsed_dat[key_str]['timeseries']   = inf_mo.tolist()


  # Calibration score from timeseries data
  (obj_val, scal_vec) = norpois_opt([ref_dat_01], inf_mo[:len(ref_dat_01)])

  parsed_dat[key_str]['cal_val']   = float(obj_val)
  parsed_dat[key_str]['rep_rate']  = float(scal_vec[0])


  # Sample population pyramid every year
  with open(os.path.join(output_path,'DemographicsSummary.json')) as fid01:
    demog_output = json.load(fid01)

  age_key_list = [   '<5',   '5-9', '10-14', '15-19', '20-24', '25-29',
                  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
                  '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
                  '90-94', '95-99']
  pyr_dat      = np.zeros((int(RUN_YEARS)+1,len(age_key_list)))

  for k1 in range(len(age_key_list)):
    age_key_str = 'Population Age {:s}'.format(age_key_list[k1])
    age_vec_dat = np.array(demog_output['Channels'][age_key_str]['Data'])
    pyr_dat[0,  k1] = age_vec_dat[0]
    pyr_dat[1:, k1] = age_vec_dat[364::365]

  parsed_dat[key_str]['pyr_data'] = pyr_dat.tolist()


  # Common output data
  parsed_dat['tstamps'] = (np.diff(tstamps)/2.0 + tstamps[:-1]).tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
