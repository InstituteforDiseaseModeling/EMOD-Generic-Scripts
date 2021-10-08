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

  SIM_IDX         = gdata.sim_index
  REP_MAP_DICT    = gdata.demog_node_map    # LGA Dotname:     [NodeIDs]
  REP_DEX_DICT    = gdata.demog_rep_index   # LGA Dotname:  Output row number

  START_DAY       = gdata.start_off


  # ***** Get variables for this simulation *****
  TIME_START      = gdata.var_params['start_time']
  TIME_DELTA      = gdata.var_params['num_tsteps']

  OPV_BOXES       = gdata.var_params['OPV_compartments']
  NOPV_BOXES      = gdata.var_params['nOPV_compartments']

  cVDPV_genome    = OPV_BOXES + NOPV_BOXES


  # Timesteps
  time_init  = START_DAY + TIME_START
  time_vec   = np.arange(time_init, time_init + 2*TIME_DELTA)


  # Post-process strain reporter
  strain_dat = np.loadtxt(os.path.join(output_path,'ReportStrainTracking01.csv'),delimiter=',',skiprows=1,ndmin=2)


  # Construct csv file for cVDPV infections (Sabin descent: Clade = 0)
  node_reps     = list(REP_DEX_DICT.keys())
  dbrick0       = np.zeros((len(node_reps)+1,int(TIME_DELTA)))
  dbrick0[0,:]  = time_vec[:int(TIME_DELTA)]

  if(strain_dat.shape[0]>0):
    for rep_name in node_reps:
      brick_dex      = REP_DEX_DICT[rep_name]
      rep_bool       = np.isin(strain_dat[:,1],REP_MAP_DICT[rep_name]) & (strain_dat[:,2]==0) & (strain_dat[:,3]==cVDPV_genome)
      targ_dat       = strain_dat[rep_bool,:]
      for k1 in range(targ_dat.shape[0]):
        dbrick0[brick_dex,int(targ_dat[k1,0]-time_init)] += targ_dat[k1,7]

  np.savetxt(os.path.join(output_path,'lga_timeseries.csv'),dbrick0,fmt='%.0f',delimiter=',')


  # Construct csv file for cVDPV infections (nOPV descent: Clade = 1)
  node_reps     = list(REP_DEX_DICT.keys())
  dbrick0       = np.zeros((len(node_reps)+1,int(TIME_DELTA)))
  dbrick0[0,:]  = time_vec[:int(TIME_DELTA)]

  if(strain_dat.shape[0]>0):
    for rep_name in node_reps:
      brick_dex      = REP_DEX_DICT[rep_name]
      rep_bool       = np.isin(strain_dat[:,1],REP_MAP_DICT[rep_name]) & (strain_dat[:,2]==1) & (strain_dat[:,3]==cVDPV_genome)
      targ_dat       = strain_dat[rep_bool,:]
      for k1 in range(targ_dat.shape[0]):
        dbrick0[brick_dex,int(targ_dat[k1,0]-time_init)] += targ_dat[k1,7]

  np.savetxt(os.path.join(output_path,'lga_timeseries_nopv.csv'),dbrick0,fmt='%.0f',delimiter=',')


  # Post-process serosurveys
  sero_dat00 = np.loadtxt(os.path.join(output_path,'ReportSerosurvey00.csv'),delimiter=',',skiprows=1,ndmin=2)
  sero_dat01 = np.loadtxt(os.path.join(output_path,'ReportSerosurvey01.csv'),delimiter=',',skiprows=1,ndmin=2)


  # Construct csv file for non-zero group serosurveys
  # Do something useful



  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Empty object
  parsed_dat[key_str] = dict()


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)

  return None

#*******************************************************************************
