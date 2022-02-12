#********************************************************************************
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

#********************************************************************************

tpop_2020    = 89561000

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index

  # ***** Get variables for this simulation *****
  TIME_DELTA     = gdata.var_params['num_tsteps']


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}
  calval_dat = {key_str: dict()}


  # Sample population pyramid every year
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

  parsed_dat[key_str]['pyr_data'] = pyr_dat.tolist()


  # Histogram incidence by year and by age bin
  with open(os.path.join(output_path,'BinnedReport.json')) as fid01:
    binned_output = json.load(fid01)

  age_key_list = [   '<5',   '5-9', '10-14', '15-19', '20-24', '25-29',
                  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
                  '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
                  '90-94', '95-99']
  inf_dat      = np.zeros((int(np.ceil(TIME_DELTA/365.0)),len(age_key_list)))
  inf_mat_dat  = np.array(binned_output['Channels']['New Infections']['Data'])

  for k1 in range(inf_dat.shape[1]):
    inf_vec_dat = inf_mat_dat[k1,:]
    for k2 in range(inf_dat.shape[0]):
      dex1 = int(365*(k2))
      dex2 = int(365*(k2+1))
      if(dex2>inf_vec_dat.shape[0]):
        inf_dat[k2,k1] = np.sum(inf_vec_dat[dex1:])
      else:
        inf_dat[k2,k1] = np.sum(inf_vec_dat[dex1:dex2])

  parsed_dat[key_str]['inf_data'] = inf_dat.tolist()


  # Calculate calibration score
  err_score = 0

  calval_dat[key_str] = float(err_score)


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  # Write calibration score
  with open('calval_out.json','w') as fid01:
    json.dump(calval_dat, fid01)


  return None

#*******************************************************************************
