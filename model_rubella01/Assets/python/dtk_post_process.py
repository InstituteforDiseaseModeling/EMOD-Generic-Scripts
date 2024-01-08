#********************************************************************************
#
#********************************************************************************

import os, sys, json, sqlite3

import global_data as gdata

import numpy as np

from builder_demographics import pop_age_days

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index
  BASE_YEAR     = gdata.base_year
  START_YEAR    = gdata.start_year
  RUN_YEARS     = gdata.run_years
  TIME_STEP     = gdata.t_step_days


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(0.0)
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  data_vec_time = np.array([val[0] for val in row_list], dtype = float)  # Time
  data_vec_node = np.array([val[2] for val in row_list], dtype = int  )  # Node
  data_vec_mcw  = np.array([val[4] for val in row_list], dtype = float)  # MCW
  data_vec_age  = np.array([val[5] for val in row_list], dtype = float)  # Age


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


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

  parsed_dat[key_str]['pyr_data'] = pyr_dat.tolist()


  # Yearly timeseries by age
  DAY_BINS    = [365]
  START_TIME  = 365.0*(START_YEAR-BASE_YEAR)
  BIN_EDGES   = np.cumsum(int(RUN_YEARS)*DAY_BINS) + START_TIME + 0.5
  BIN_EDGES   = np.insert(BIN_EDGES, 0, START_TIME + 0.5)

  inf_dat     = np.zeros((int(RUN_YEARS),len(pop_age_days)-1))
  for k1 in range(inf_dat.shape[1]):
    idx = (data_vec_age >= pop_age_days[k1]) & (data_vec_age < pop_age_days[k1+1])
    (inf_yr, tstamps) = np.histogram(data_vec_time[idx],
                                     bins    = BIN_EDGES,
                                     weights = data_vec_mcw[idx])
    inf_dat[:,k1] = inf_yr
  parsed_dat[key_str]['inf_data'] = inf_dat.tolist()


  # Retain annualized count of births; store in a json dict
  with open(os.path.join(output_path,'InsetChart.json')) as fid01:
    inset_chart = json.load(fid01)

  ic_start = inset_chart['Header']['Start_Time']
  ic_nstep = inset_chart['Header']['Timesteps']
  ic_tsize = inset_chart['Header']['Simulation_Timestep']
  cumb_vec = np.array(inset_chart['Channels']['Births']['Data'])

  time_vec = np.arange(ic_nstep)*ic_tsize + ic_start
  nyr_bool = (np.diff(time_vec//365.0)>0.0)
  b_vec    = cumb_vec[:-1][nyr_bool]
  if(b_vec.shape[0] < int(RUN_YEARS)):
    b_vec = np.append(b_vec, cumb_vec[-1])
  b_vec[1:] = np.diff(b_vec)

  parsed_dat[key_str]['cbr_vec'] = b_vec.tolist()


  # Calculate calibration score
  err_score = 0

  parsed_dat[key_str]['cal_val'] = float(err_score)


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
