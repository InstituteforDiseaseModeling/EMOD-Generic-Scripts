#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json, sqlite3

import global_data as gdata

import numpy as np

#*******************************************************************************

def application(timestep):

  PREV_TIME     = gdata.prev_proc_time
  FIRST_CALL    = gdata.first_call_bool

  proc_time     = float(timestep)


  # First call to in-process; initialize tree data
  if(FIRST_CALL):
    gdata.first_call_bool = False
    gdata.tree_data       = np.zeros((0,4),dtype=int)
    print("Hello from in-process at time {:.1f}".format(proc_time))


  # Only evaluate every 10th timestep
  if(proc_time%10 < 9.0):
    return None


  # Connect to SQL database; retreive new entries
  connection_obj = sqlite3.connect('simulation_events.db')
  cursor_obj     = connection_obj.cursor()

  sql_cmd = "SELECT * FROM SIM_EVENTS WHERE SIM_TIME > {:.1f}".format(PREV_TIME)
  cursor_obj.execute(sql_cmd)
  row_list = cursor_obj.fetchall()

  print('Row list has {:d} rows'.format(len(row_list)))

  new_data = np.zeros((len(row_list),4),dtype=int)
  new_data[:,0] = [int(val[0]) for val in row_list]  # Time
  new_data[:,1] = [    val[2]  for val in row_list]  # Node
  new_data[:,2] = [    val[3]  for val in row_list]  # Individual ID
  new_data[:,3] = [    val[5]  for val in row_list]  # Infector ID
  gdata.tree_data = np.append(gdata.tree_data, new_data, axis=0)

  print('Tree data table has {:d} rows'.format(gdata.tree_data.shape[0]))


  # Record timestamp of previous process
  gdata.prev_proc_time = proc_time


  return None

#*******************************************************************************
