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

  REPORTS_FILENAME = gdata.reports_file


  # ***** Get variables for this simulation *****
  SERO_TIME = gdata.var_params['serosurvey_timestamps']


  # Dictionary to be written
  json_set = dict()


  # ***** Custom reporters *****
  json_set['Custom_Reports'] = dict()



  # ***** Additional reporters *****

  # Strain reporting
  json_set['Custom_Reports']['ReportStrainTracking'] = { 'Enabled': 1      ,
                                                         'Reports': list() }

  repDic = { 'Report_Name':  'ReportStrainTracking01.csv' }

  json_set['Custom_Reports']['ReportStrainTracking']['Reports'].append(repDic)


  # Serosurveys
  json_set['Custom_Reports']['ReportSerosurvey'] = { 'Enabled': 1      ,
                                                     'Reports': list() }

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
  with open(REPORTS_FILENAME,'w') as fid01:
    json.dump(json_set, fid01, sort_keys=True, indent=4)


  return None

#********************************************************************************
