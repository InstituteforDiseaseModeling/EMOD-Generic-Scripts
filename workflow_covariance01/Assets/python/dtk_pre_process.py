#********************************************************************************
#
# Python 3.6.0
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

def application(config_filename_in): 

  # Declare current version of emod-api
  print('Using emod-api {:s}'.format(emod_api.__version__))


  # Read index of simulation parameter set
  with open('idx_str_file.txt') as fid01:
    sim_index = int(fid01.readline())
  gdata.sim_index = sim_index


  # Read parameter dictionary, select appropriate index, save in globals
  with open(os.path.join('Assets','param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  var_params = dict()
  var_params.update({keyval:param_dict['EXP_VARIABLE'][keyval][sim_index]
                  for keyval in param_dict['EXP_VARIABLE']})
  var_params.update({keyval:param_dict['EXP_CONSTANT'][keyval]
                  for keyval in param_dict['EXP_CONSTANT']})
  gdata.var_params = var_params


  # Validation checks on param_dict.json
  names_variable = set(param_dict['EXP_VARIABLE'].keys())
  names_constant = set(param_dict['EXP_CONSTANT'].keys())
  if(names_constant.intersection(names_variable)):
    raise Exception('In param_dict.json: name in both EXP_CONSTANT and EXP_VARIABLE')


  # Seed random number generator
  np.random.seed(sim_index)


  # Make demographics file
  demographicsBuilder()
  time.sleep(1)


  # Make campaign file
  campaignBuilder()
  time.sleep(1)


  # Make custom reporter file
  dllcBuilder()
  time.sleep(1)


  # Simulation configuration file
  config_filename = configBuilder()
  time.sleep(1)


  # Pre-process function needs to return config filename as a string
  return config_filename

#*******************************************************************************
