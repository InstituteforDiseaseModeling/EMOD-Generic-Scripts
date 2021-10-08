#********************************************************************************
#
# Builds a custom_dlls.json file to be used as input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

#********************************************************************************

def dllcBuilder():

  REPORTS_FILENAME = 'custom_dlls.json'


  # ***** Get variables for this simulation *****
  SERO_TIME        = gdata.var_params['serosurvey_timestamps']


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
       },
     'ReportSerosurvey':
       {
        'Enabled':  1,
        'Reports': []
       }
    }


  # Strain reporting
  repDic = { 'Report_Name':      'ReportStrainTracking01.csv' }

  json_set['Custom_Reports']['ReportStrainTracking']['Reports'].append(repDic)


  # Serosurveys
  repDic = { 'Report_Name':      'ReportSerosurvey01.csv',
             'Time_Stamps':      SERO_TIME,
             'Age_Bins':         np.arange(365,3651,365).tolist()+[36500.0],
             'Target_Property':  'Geographic:L01' }

  json_set['Custom_Reports']['ReportSerosurvey']['Reports'].append(repDic)

  repDic = { 'Report_Name':      'ReportSerosurvey00.csv',
             'Time_Stamps':      SERO_TIME,
             'Age_Bins':         np.arange(365,3651,365).tolist()+[36500.0],
             'Target_Property':  'Geographic:L00' }

  json_set['Custom_Reports']['ReportSerosurvey']['Reports'].append(repDic)


  #  ***** End file construction *****
  with open('custom_dlls.json','w') as fid01:
    json.dump(json_set,fid01,sort_keys=True)

  # Save filename to global data for use in other functions
  gdata.reports_file = REPORTS_FILENAME


  return None

#********************************************************************************
