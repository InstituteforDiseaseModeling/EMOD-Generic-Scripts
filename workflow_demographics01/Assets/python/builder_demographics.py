#********************************************************************************
#
# Builds a demographics file and overlays for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

from refdat_deathrate      import data_dict   as dict_death

from dtk_post_process      import pop_age_days, uk_1950_frac

from emod_api.demographics.Demographics  import Demographics, Node
from emod_api.demographics               import DemographicsTemplates as DT

#********************************************************************************

br_base_val   = 15.3

br_force_xval = [   0.0,    1.0,    2.0,    3.0,    4.0,    5.0,    6.0,    7.0,
                    8.0,    9.0,   10.0,   11.0,   12.0,   13.0,   14.0,   15.0,
                   16.0,   17.0,   18.0,   19.0,   20.0,   21.0,   22.0,   23.0,
                   24.0,   25.0,   26.0,   27.0,   28.0,   29.0,   30.0]

br_force_yval = [0.9405, 0.9569, 0.9733, 0.9897, 1.0061, 1.0225, 1.0390, 1.0554,
                 1.0718, 1.0966, 1.1215, 1.1463, 1.1712, 1.1961, 1.1780, 1.1599,
                 1.1418, 1.1238, 1.1057, 1.0614, 1.0172, 0.9730, 0.9288, 0.8845,
                 0.8642, 0.8440, 0.8237, 0.8035, 0.7832, 0.7939, 0.8046]

#********************************************************************************

def demographicsBuilder():

  DEMOG_FILENAME = 'demographics.json'
  SETTING        = 'EURO:UK'


  # ***** Get variables for this simulation *****
  MOD_AGE_INIT = gdata.var_params['modified_age_init']
  LN_MORT_MULT = gdata.var_params['log_mortality_mult']


  # ***** Populate nodes in primary file *****
  node_list = list()

  init_pop   = 100000
  node_id    = 1
  node_name  = SETTING+':A{:05d}'.format(node_id)

  node_obj = Node(lat=0.0, lon=0.0, pop=init_pop, name=node_name, forced_id=node_id)
  node_list.append(node_obj)


  # ***** Create primary file *****
  ref_name   = 'Jun2021_Demographics_Example'
  demog_obj  = Demographics(nodes=node_list, idref=ref_name)


  # ***** Vital dynamics *****
  global br_base_val

  birth_rate   = br_base_val/1000.0/365.0
  mort_vec_X   = dict_death['BIN_EDGES']
  mort_vec_Y   = [mort_val*np.exp(LN_MORT_MULT) for mort_val in dict_death[SETTING]]
  forcing_vec  = 12*[1.0]                 # No seasonal forcing

  # Calculate equilibrium distribution
  (grow_rate, age_x, age_y) = DT._computeAgeDist(birth_rate,mort_vec_X,mort_vec_Y,forcing_vec)

  if(MOD_AGE_INIT):
    age_x = np.cumsum(np.array(uk_1950_frac)).tolist()
    age_y = pop_age_days

  # ***** Update defaults in primary file ****

  demog_obj.raw['Defaults']['IndividualAttributes'].clear()
  demog_obj.raw['Defaults']['NodeAttributes'].clear()

  DT.MortalityRateByAge(demog_obj, (np.array(mort_vec_X)/365.0).tolist(), mort_vec_Y)

  # Stuff below could use a dedicated setter-function. Couldn't find it in emod_api.
  iadict = dict()

  iadict['AgeDistribution'] = {'DistributionValues':  [age_x] ,
                               'ResultScaleFactor':         1 ,
                               'ResultValues':        [age_y] }

  demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)

  # The growth rate specifed here is the exact solution to the long-term steady-state value.
  nadict = dict()

  nadict['BirthRate']      =   birth_rate
  nadict['GrowthRate']     =   grow_rate   # Not used; included for reference

  demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)


  # ***** Write primary demographics file *****

  demog_obj.generate_file(name=DEMOG_FILENAME)

  # Save filename to global data for use in other functions
  gdata.demog_files.append(DEMOG_FILENAME)

  # Save the demographics object for use in other functions
  gdata.demog_object = demog_obj



  return None

#*******************************************************************************