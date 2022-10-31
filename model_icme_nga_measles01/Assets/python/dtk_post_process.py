#********************************************************************************
#
#********************************************************************************

import os, sys, shutil, json, sqlite3

import global_data as gdata

import numpy as np

#********************************************************************************

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index
  BASE_YEAR     = gdata.base_year


  # ***** Get variables for this simulation *****
  TIME_YEARS    = gdata.var_params['num_years']
  SIA_ADDLIST   = gdata.var_params['test_sias']



  DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
  BIN_EDGES = np.cumsum(TIME_YEARS*DAY_BINS) + gdata.start_log + 0.5
  BIN_EDGES = np.insert(BIN_EDGES, 0, gdata.start_log + 0.5)


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}
  calval_dat = {key_str: dict()}


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > 0"
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  data_time = np.array([val[0] for val in row_list], dtype = float)  # Time
  data_node = np.array([val[2] for val in row_list], dtype = int  )  # Node
  data_mcw  = np.array([val[4] for val in row_list], dtype = float)  # MCW


  # Sample population pyramid every year
  with open(os.path.join(output_path,'DemographicsSummary.json')) as fid01:
    demog_output = json.load(fid01)

  age_key_list = [   '<5',   '5-9', '10-14', '15-19', '20-24', '25-29',
                  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
                  '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
                  '90-94', '95-99']
  pyr_dat      = np.zeros((int(TIME_YEARS)+1,len(age_key_list)))

  for k1 in range(len(age_key_list)):
    age_key_str = 'Population Age {:s}'.format(age_key_list[k1])
    age_vec_dat = np.array(demog_output['Channels'][age_key_str]['Data'])
    pyr_dat[0,  k1] = age_vec_dat[0]
    pyr_dat[1:, k1] = age_vec_dat[364::365]

  parsed_dat[key_str]['pyr_data'] = pyr_dat.tolist()


  # Get campaign doses
  parsed_dat[key_str]['sia_summary'] = list()

  with open(os.path.join(output_path,'InsetChart.json')) as fid01:
    inset_chart = json.load(fid01)
  sia_doses = np.diff(np.array(inset_chart['Channels']['Campaign Cost']['Data']))
  sia_doses = sia_doses[sia_doses>0]


  # Post-process strain reporter
  strain_dat = np.loadtxt(os.path.join(output_path,'ReportStrainTracking01.csv'),delimiter=',',skiprows=1,ndmin=2)
  rep_bool   = (strain_dat[:,3]==1)
  targ_dat   = strain_dat[rep_bool,:]
  for k1 in range(len(SIA_ADDLIST)):
    year_val   = SIA_ADDLIST[k1]
    targ_val   = sia_doses[k1]
    start_val  = np.ceil((year_val-BASE_YEAR)*365.0)
    rep_bool   = (targ_dat[:,0]==start_val)
    num_inf    = np.sum(targ_dat[rep_bool,4])
    parsed_dat[key_str]['sia_summary'].append([start_val, num_inf, targ_val])


  # Aggregate new infections to timeseries by month
  (inf_mo, tstamps) = np.histogram(data_time,
                                   bins    = BIN_EDGES,
                                   weights = data_mcw)

  # Correct for SIA doses as infections
  for k1 in range(len(parsed_dat[key_str]['sia_summary'])):
    for k2 in range(len(BIN_EDGES)):
      if(parsed_dat[key_str]['sia_summary'][k1][0]<BIN_EDGES[k2]):
        inf_mo[k2-1] -= parsed_dat[key_str]['sia_summary'][k1][1]
        break

  parsed_dat[key_str]['inf_mo'] = inf_mo.tolist()


  # Calculate calibration score
  err_score = 0

  calval_dat[key_str] = float(err_score)


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
