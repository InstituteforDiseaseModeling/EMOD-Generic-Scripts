#********************************************************************************
#
#********************************************************************************

import os, sys, json, sqlite3

import global_data as gdata

import numpy as np

import emod_api.campaign     as     camp_module

from builder_campaign   import   IV_SIA

#*******************************************************************************

def application(timestep):

  PREV_TIME     = gdata.prev_proc_time
  FIRST_CALL    = gdata.first_call_bool
  NODE_DICT     = gdata.demog_node

  CASE_THRESH   = gdata.var_params['adm01_case_threshold']
  LOG_REP_RATE  = gdata.var_params['log10_min_reporting']

  proc_time     = float(timestep)


  # First call to in-process; initialize as needed
  if(FIRST_CALL):
    gdata.first_call_bool = False
    gdata.data_vec_time = np.array(list())
    gdata.data_vec_node = np.array(list())
    gdata.data_vec_mcw  = np.array(list())

    adm01_name = list(set([':'.join(val.split(':')[:3]) for val in NODE_DICT]))
    adm01_list = [[val,list(),0] for val in adm01_name]
    for nname in NODE_DICT:
      for adm01_tup in adm01_list:
        if(nname.startswith(adm01_tup[0]+':')):
          adm01_tup[1].append(NODE_DICT[nname])

    adm02_name = list(set([':'.join(val.split(':')[:4]) for val in NODE_DICT]))
    adm02_rate = {val:np.random.beta(0.33,8.0) for val in adm02_name}

    with open('adm02_obsrate.json','w') as fid01:
      json.dump(adm02_rate,fid01,sort_keys=True,indent=3)

    nobs_list = np.zeros(gdata.max_node_id,dtype=float)
    for nname in NODE_DICT:
      for adm02_name in adm02_rate:
        if(nname.startswith(adm02_name+':')):
          nobs_list[NODE_DICT[nname]-1] = adm02_rate[adm02_name]

    gdata.adm01_list = adm01_list
    gdata.nobs_vec   = nobs_list

    print("Hello from in-process at time {:.1f}".format(proc_time))


  # Only evaluate every month-ish
  if(((proc_time%365.0)%30.0) < 29.0):
    return None


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


  # Record timestamp of previous process
  gdata.prev_proc_time = proc_time


  # Only do response starting in 2020
  if(proc_time > 43800.0):
    for k1 in range(gdata.max_node_id):
      nid_val  = k1 + 1
      gidx     = (data_node==nid_val)
      min_rate = np.power(10.0,LOG_REP_RATE)
      nreprate = np.maximum(gdata.nobs_vec[nid_val-1],min_rate)
      obs_inf  = np.sum(data_mcw[gidx])*nreprate
      for adm01_tup in gdata.adm01_list:
        if(nid_val in adm01_tup[1]):
          adm01_tup[2] += obs_inf


  # Reactive campaign
  targ_nodes = list()
  for adm01_tup in gdata.adm01_list:
    if(adm01_tup[2] > CASE_THRESH):
      targ_nodes.extend(adm01_tup[1])
      adm01_tup[2] = 0

  if(len(targ_nodes) > 0):
    camp_module.reset()
    pdict     = {'startday':  proc_time+30.0 ,
                 'nodes':         targ_nodes ,
                 'agemin':        0.75*365.0 ,
                 'agemax':        5.00*365.0 ,
                 'coverage':            0.50 }
    CAMP_FILE = 'campaign_{:05d}.json'.format(int(proc_time))
    camp_module.add(IV_SIA(pdict))
    camp_module.save(filename=CAMP_FILE)

    return CAMP_FILE


  return None

#*******************************************************************************
