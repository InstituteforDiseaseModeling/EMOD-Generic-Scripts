#********************************************************************************
#
# Builds a demographics file and overlays for input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

from refdat_birthrate              import data_dict   as dict_birth
from refdat_deathrate              import data_dict   as dict_death

import numpy as np

import scipy.optimize      as opt

from emod_api.demographics.Demographics  import Demographics, Node
from emod_api.demographics               import DemographicsTemplates as DT

#********************************************************************************

def demographicsBuilder():

  DEMOG_FILENAME = 'demographics.json'
  SETTING        = 'AFRO:NIGERIA'


  # ***** Get variables for this simulation *****
  R0             = gdata.var_params['R0']
  IND_RISK_VAR   = gdata.var_params['ind_variance_risk']
  INF_RES_SIZE   = gdata.var_params['inf_res_size']
  INF_RES_END   = gdata.var_params['inf_res_end']
  BIRTH_RATE    = gdata.var_params['birth_rate'] / 1000.0 / 365.0

  # ***** Populate nodes in primary file *****

  node_list = list()

  init_pop   = int(100000)
  node_id    = 1
  node_name  = SETTING+':A{:05d}'.format(node_id)

  node_obj = Node(lat=0.0, lon=0.0, pop=init_pop, name=node_name, forced_id=node_id)
  node_list.append(node_obj)


  # ***** Create primary file *****

  ref_name   = 'seasonality_dynamics'
  demog_obj  = Demographics(nodes=node_list, idref=ref_name)


  # ***** Vital dynamics *****
  # birth_rate   = dict_birth[SETTING]
  mort_vec_X   = dict_death['BIN_EDGES']
  mort_vec_Y   = dict_death[SETTING]
  forcing_vec  = 12*[1.0]                 # No seasonal forcing

  # Calculate equilibrium distribution
  (grow_rate, age_x, age_y) = DT._computeAgeDist(BIRTH_RATE,mort_vec_X,mort_vec_Y,forcing_vec)


  # ***** Initial susceptibility *****
  targ_frac   = 1.1*(1.0/R0)    # Tries to aim for Reff of 1.1;
                                # not precise because of maternal immunity

  # Stuff below ought to get wrapped into a separate function. It's doing an implicit solve
  # of an exponential decay mapped onto the age distribution specified above. The target
  # area-under-the-curve is the value specified by targ_frac above. Just aims to get close.
  # May break for very low target frac values (e.g., < 0.01)
  age_year    = np.array(age_y[1:])/365.0
  age_prob    = np.diff(np.array(age_x))

  boxer       = lambda x1: np.sum(np.minimum(np.exp(x1*(age_year-0.65)),1.0)*age_prob)-targ_frac
  iSP0        = opt.brentq(boxer, a=-80, b=0)

  isus_x      = [0] + (np.logspace(1.475,4.540,20,dtype=int)).tolist()
  isus_y      = [round(np.minimum(np.exp(iSP0*(val/365.0-0.65)),1.0),4) for val in isus_x]


  # ***** Update defaults in primary file ****

  demog_obj.raw['Defaults']['IndividualAttributes'].clear()
  demog_obj.raw['Defaults']['NodeAttributes'].clear()


  # Stuff below could use a dedicated setter-function. Couldn't find it in emod_api.
  iadict = dict()
  iadict['AcquisitionHeterogeneityVariance']   =   IND_RISK_VAR
  iadict['MortalityDistribution']              = \
               {'NumPopulationGroups':                   [2,len(mort_vec_X)] ,
                'NumDistributionAxes':                                     2 ,
                'AxisNames':                                ['gender','age'] ,
                'AxisScaleFactors':                                    [1,1] ,
                'ResultScaleFactor':                                       1 ,
                'PopulationGroups':                      [[0,1], mort_vec_X] ,
                'ResultValues':                      [mort_vec_Y,mort_vec_Y] }
  iadict['AgeDistribution']                    = \
               {'DistributionValues':                                [age_x] ,
                'ResultScaleFactor':                                       1 ,
                'ResultValues':                                      [age_y] }
  iadict['SusceptibilityDistribution']         = \
               {'DistributionValues':                                 isus_x ,
                'ResultScaleFactor':                                       1 ,
                'ResultValues':                                       isus_y }

  demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)

  # The growth rate specifed here is the exact solution to the long-term steady-state
  # value. It can be used to estimate total population over time with very good
  # precision.
  nadict = dict()
  nadict['BirthRate']                          =   BIRTH_RATE
  nadict['GrowthRate']                         =   grow_rate   # Not used; included for reference
  nadict['InfectivityReservoirSize']           =   INF_RES_SIZE
  nadict['InfectivityReservoirEndTime']        =   INF_RES_END*365

  demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)


  # ***** Write primary demographics file *****

  demog_obj.generate_file(name=DEMOG_FILENAME)

  # Save filename to global data for use in other functions
  gdata.demog_files.append(DEMOG_FILENAME)

  # Save the demographics object for use in other functions
  gdata.demog_object = demog_obj


  return None

#*******************************************************************************