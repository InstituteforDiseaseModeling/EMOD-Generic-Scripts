#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, shutil, json

import global_data as gdata

import numpy as np

#********************************************************************************

def application(output_path):

  DAY_BINS  = [31,28,31,30,31,30,31,31,30,31,30,31]
  REF_DAY   = 110*365                                 # Start log in 2010
  BIN_EDGES = np.cumsum(11*DAY_BINS) + REF_DAY + 0.5  # Log for 10 years
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


  # Monthly timeseries
  parsed_dat[key_str]   = inf_mo.tolist()
  parsed_dat['tstamps'] = (np.diff(tstamps)/2.0 + tstamps[:-1]).tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)

  return None

#*******************************************************************************
