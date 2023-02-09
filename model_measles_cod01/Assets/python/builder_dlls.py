#********************************************************************************
#
# Builds a custom_dlls.json file to be used as input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

#********************************************************************************

def dllcBuilder():

  REPORTS_FILENAME = 'custom_dlls.json'


  # ***** Get variables for this simulation *****
  START_LOG = gdata.start_log


  # Dictionary to be written
  json_set = {}


  # ***** Custom reporters *****
  json_set['Custom_Reports'] = \
    {
     'Use_Explicit_Dlls': 1,
     'ReportStrainTracking':
       {
        'Enabled':  1,
        'Reports': []
       }
    }


  # Strain reporting
  repDic = { 'Report_Name':    'ReportStrainTracking01.csv',
             'Time_Start':      START_LOG                  }

  json_set['Custom_Reports']['ReportStrainTracking']['Reports'].append(repDic)


  #  ***** End file construction *****
  with open('custom_dlls.json','w') as fid01:
    json.dump(json_set,fid01,sort_keys=True)

  # Save filename to global data for use in other functions
  gdata.reports_file = REPORTS_FILENAME


  return None

#********************************************************************************
