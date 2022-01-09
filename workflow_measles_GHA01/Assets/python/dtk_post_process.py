#********************************************************************************
#
#********************************************************************************

import os, sys, shutil, json

import global_data as gdata

import numpy as np

#********************************************************************************

pop_age_days  = [     0,   1825,   3650,   5475,   7300,   9125,  10950,  12775,
                  14600,  16425,  18250,  20075,  21900,  23725,  25550,  27375,
                  29200,  31025,  32850,  34675,  36500]

gha_2010_frac = [0.1448, 0.1294, 0.1187, 0.1065, 0.0956, 0.0815, 0.0692, 0.0604,
                 0.0519, 0.0425, 0.0315, 0.0218, 0.0178, 0.0123, 0.0084, 0.0049,
                 0.0021, 0.0006, 0.0001, 0.0000, 0.0000]

gha_2020_frac = [0.1343, 0.1251, 0.1120, 0.1010, 0.0921, 0.0817, 0.0729, 0.0619,
                 0.0523, 0.0452, 0.0383, 0.0304, 0.0215, 0.0136, 0.0096, 0.0051,
                 0.0022, 0.0007, 0.0001, 0.0000, 0.0000]

tpop_xval = [  2008.5,   2009.5,   2010.5,   2011.5,   2012.5,   2013.5,
               2014.5,   2015.5,   2016.5,   2017.5,   2018.5,   2019.5,
               2020.5,   2021.5,   2022.5,   2023.5,   2024.5]

tpop_yval = [23563832, 24170943, 24779614, 25387713, 25996454, 26607641,
             27224480, 27849203, 28481947, 29121464, 29767108, 30417858,
             31072945, 31732128, 32395454, 33062741, 33733902]

ref_dat   = [  4,  17,  26,  11,  11,   6,   5,   8,  13,  17,  12,   6,
              32,  47,  73,  48,  39,  33,  15,  27,  11,   7,  14,   1,
              38,  48,  58,  71,  25,  10,  16,  14,  20,   5,   9,   8,
              38,  35,  21,  13,  14,  16,   2,   1,   1,   1,   0,   0,
               1,   5,   3,   7,  11,   4,   3,   3,   5,   4,   5,   0,
               6,   5,   9,  39,  78,  90,  74,  96,  38,  17,   2,   1,
              12,   4,  14,  80, 191, 167,  52,   1,   5, 166, 147, 104,
             161, 194,  51,  66, 144,  39,  19,  66,  95, 198, 137,  38,
              30, 260, 250, 242, 100,  37,  43,  72,  47,  77, 189,  73]

#********************************************************************************

def application(output_path):

  DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
  REF_DAY   = 111*365                                 # Start log in 2011
  BIN_EDGES = np.cumsum(14*DAY_BINS) + REF_DAY + 0.5  # Log for 14 years
  BIN_EDGES = np.insert(BIN_EDGES, 0, REF_DAY + 0.5)

  SIM_IDX         = gdata.sim_index
  REP_MAP_DICT    = gdata.demog_node_map    # LGA Dotname:     [NodeIDs]
  REP_DEX_DICT    = gdata.demog_rep_index   # LGA Dotname:  Output row number


  # ***** Get variables for this simulation *****
  TIME_START      = gdata.var_params['start_time']
  TIME_DELTA      = gdata.var_params['num_tsteps']


  # Timestamps
  time_vec = np.arange(TIME_START, TIME_START + TIME_DELTA)


  # Aggregate new infections by month
  with open(os.path.join(output_path,'InsetChart.json')) as fid01:
    inset_chart = json.load(fid01)
  inf_day = inset_chart['Channels']['New Infections']['Data']

  (inf_mo, tstamps) = np.histogram(time_vec, bins=BIN_EDGES, weights=inf_day)


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Common data
  parsed_dat['tstamps'] = (np.diff(tstamps)/2.0 + tstamps[:-1]).tolist()


  # Monthly timeseries
  parsed_dat[key_str]['timeseries']   = inf_mo.tolist()


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

  parsed_dat[key_str]['pyramid'] = pyr_dat.tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)

  return None

#*******************************************************************************
