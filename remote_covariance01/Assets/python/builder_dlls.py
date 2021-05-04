#********************************************************************************
#
# Builds a custom_dlls.json file to be used as input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

ext_py_path = os.path.join('Assets','site_packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy as np

#********************************************************************************

def dllcBuilder():

  REPORTS_FILENAME = 'custom_dlls.json'


  # ***** Get variables for this simulation *****
  # N/A


  # Dictionary to be written
  json_set = {}


  # ***** Custom reporters *****
  json_set['Custom_Reports'] = \
    {
     'Use_Explicit_Dlls': 1
    }


  # ***** Additional reporters *****

  # None


  #  ***** End file construction *****
  with open(REPORTS_FILENAME,'w') as fid01:
    json.dump(json_set,fid01,sort_keys=True)

  # Save filename to global data for use in other functions
  gdata.reports_file = REPORTS_FILENAME


  return None

#********************************************************************************
