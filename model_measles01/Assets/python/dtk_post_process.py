#********************************************************************************
#
#********************************************************************************

import os, sys, json, sqlite3

import global_data as gdata

import numpy as np

#********************************************************************************

def application(output_path):

  SIM_IDX         = gdata.sim_index
  RUN_YEARS       = gdata.run_years
  BASE_YEAR       = gdata.base_year

  # ***** Get variables for this simulation *****
  START_YEAR      = gdata.var_params['start_year']


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(0.0)
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  data_vec_time = np.array([val[0] for val in row_list], dtype = float)  # Time
  data_vec_node = np.array([val[2] for val in row_list], dtype = int  )  # Node
  data_vec_mcw  = np.array([val[4] for val in row_list], dtype = float)  # MCW


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Aggregate new infections by month
  DAY_BINS    = [31,28,31,30,31,30,31,31,30,31,30,31]
  START_TIME  = 365.0*(START_YEAR-BASE_YEAR)
  BIN_EDGES   = np.cumsum(int(RUN_YEARS)*DAY_BINS) + START_TIME + 0.5
  BIN_EDGES = np.insert(BIN_EDGES, 0, START_TIME + 0.5)

  (inf_mo, tstamps) = np.histogram(data_vec_time,
                                   bins    = BIN_EDGES,
                                   weights = data_vec_mcw)

  # Monthly timeseries
  parsed_dat[key_str]['timeseries']   = inf_mo.tolist()


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


  # Calculate calibration score
  err_score = 0

  parsed_dat[key_str]['cal_val'] = float(err_score)


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
