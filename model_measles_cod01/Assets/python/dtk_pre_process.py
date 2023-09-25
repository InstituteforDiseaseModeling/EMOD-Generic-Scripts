#********************************************************************************
#
#********************************************************************************

import os, sys, json, time

import global_data as gdata

from builder_config         import configBuilder
from builder_demographics   import demographicsBuilder
from builder_campaign       import campaignBuilder
from builder_dlls           import dllcBuilder

import numpy as np

import emod_api

#*******************************************************************************

API_CUR = emod_api.__version__
API_MIN = '1.30.0'

#*******************************************************************************

def application(config_filename_in):

  PFILE   = 'param_dict.json'
  I_FILE  = 'idx_str_file.txt'
  EXP_C   = 'EXP_CONSTANT'
  EXP_V   = 'EXP_VARIABLE'


  # Declare current version of emod-api; check min version
  print('Using emod-api {:s}'.format(API_CUR))
  for ver_val in zip(API_CUR.split('.'),API_MIN.split('.')):
    if(ver_val[0] >  ver_val[1]):
      break
    if(ver_val[0] == ver_val[1]):
      continue
    if(ver_val[0] <  ver_val[1]):
      raise Exception('Using emod-api {:s}; minimum version is {:s}'.format(API_CUR,API_MIN))


  # Read index of simulation parameter set
  with open(I_FILE) as fid01:
    sim_index = int(fid01.readline())
  gdata.sim_index = sim_index


  # Read parameter dictionary file
  param_dict  = dict()
  param_paths = ['.','Assets']

  for ppath in param_paths:
    pfileopt = os.path.join(ppath,PFILE)
    if(os.path.exists(pfileopt)):
      with open(pfileopt) as fid01:
        param_dict = json.load(fid01)
      break


  # Validation checks on parameter dictionary file
  if(not param_dict):
    raise Exception('No {:s} found'.format(PFILE))

  names_variable = set(param_dict[EXP_V].keys())
  names_constant = set(param_dict[EXP_C].keys())
  if(names_constant.intersection(names_variable)):
    raise Exception('Variable name in both {:s} and {:s}'.format(EXP_C,EXP_V))


  # Select simulation parameters from parameters dictionary, save in globals
  var_params  = dict()

  var_params.update({keyval:param_dict[EXP_V][keyval][sim_index]
                  for keyval in param_dict[EXP_V]})
  var_params.update({keyval:param_dict[EXP_C][keyval]
                  for keyval in param_dict[EXP_C]})

  gdata.var_params = var_params


  # Seed random number generator
  np.random.seed(sim_index)


  # Demographics file
  demographicsBuilder()
  time.sleep(1)


  # Campaign interventions file
  campaignBuilder()
  time.sleep(1)


  # Custom reporter file
  dllcBuilder()
  time.sleep(1)


  # Simulation configuration file
  config_filename = configBuilder()
  time.sleep(1)


  # Pre-process function needs to return config filename as a string
  return config_filename

#*******************************************************************************
