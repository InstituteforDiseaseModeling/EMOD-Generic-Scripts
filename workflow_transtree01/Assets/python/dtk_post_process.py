#********************************************************************************
#
#********************************************************************************

import os, sys, json, sqlite3

import global_data as gdata

import numpy as np

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index
  PREV_TIME     = gdata.prev_proc_time


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(PREV_TIME)
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  new_data = np.zeros((len(row_list),4),dtype=int)
  new_data[:,0] = [int(val[0]) for val in row_list]  # Time
  new_data[:,1] = [    val[2]  for val in row_list]  # Node
  new_data[:,2] = [    val[3]  for val in row_list]  # Individual ID
  new_data[:,3] = [    val[5]  for val in row_list]  # Infector ID

  tree_data = np.append(gdata.tree_data, new_data, axis=0)

  sql_inf = tree_data.shape[0]
  print('Tree data table has {:d} rows'.format(sql_inf))


  # Add tree data to summary output
  parsed_dat[key_str] = tree_data.tolist()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  # Validate entries in tree data
  with open(os.path.join(output_path,'InsetChart.json')) as fid01:
    inset_chart = json.load(fid01)
  ref_inf = np.sum(inset_chart['Channels']['New Infections']['Data'])


  # Throw exception if data issues
  if(sql_inf != ref_inf):
    raise Exception('IC = {:d}; SQL = {:d}'.format(ref_inf, sql_inf))


  return None

#*******************************************************************************
