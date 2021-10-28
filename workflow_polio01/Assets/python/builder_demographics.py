#********************************************************************************
#
# Builds a demographics.json file to be used as input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json, io

import global_data as gdata

from aux_demo_calc           import demoCalc_AgeDist

from refdat_population_admin02     import data_dict   as dict_pop_admin02
from refdat_area_admin02           import data_dict   as dict_area_admin02
from refdat_location_admin02       import data_dict   as dict_longlat_admin02

from refdat_population_100km       import data_dict   as dict_pop_100km
from refdat_area_100km             import data_dict   as dict_area_100km
from refdat_location_100km         import data_dict   as dict_longlat_100km

from refdat_alias                  import data_dict   as dict_alias
from refdat_birthrate              import data_dict   as dict_birth
from refdat_deathrate              import data_dict   as dict_death

import numpy                    as    np

#********************************************************************************

def demographicsBuilder():

  DEMOG_FILENAME = 'demographics.json'


  # ***** Get variables for this simulation *****
  SUB_LGA      = gdata.var_params['use_10k_res']

  LOWER_INIT   = gdata.var_params['use_50pct_init']

  TIME_START   = gdata.var_params['start_time']
  PROC_DISPER  = gdata.var_params['proc_overdispersion']

  NODE_R0_VAR  = gdata.var_params['node_variance_R0']
  IND_RISK_VAR = gdata.var_params['ind_variance_risk']

  USE_ZGRP     = gdata.var_params['use_zero_group']
  NZG_ALPHA    = gdata.var_params['nonzero_group_beta_dist_param_alpha']
  NZG_BETA     = gdata.var_params['nonzero_group_beta_dist_param_beta']
  NGZ_SCALE    = gdata.var_params['nonzero_group_scale']


  PATH_OVERLAY = 'demog_overlay'
  if(not os.path.exists(PATH_OVERLAY)):
    os.mkdir(PATH_OVERLAY)

  # ***** Prep dict for primary file *****

  # Save filename to global data for use in other functions
  gdata.demog_files.append(DEMOG_FILENAME)

  json_set = dict()

  json_set['Metadata'] = { 'IdReference':   'polio-custom' }
  json_set['Defaults'] = { 'IndividualAttributes': dict()  ,
                           'IndividualProperties': list()  ,
                           'NodeAttributes':       dict()  }
  json_set['Nodes']    = list()


  # ***** Populate nodes in primary file *****

  geog_list     = ['AFRO:NIGERIA']

  if(SUB_LGA):
    dict_pop     = dict_pop_100km
    dict_area    = dict_area_100km
    dict_longlat = dict_longlat_100km
  else:
    dict_pop     = dict_pop_admin02
    dict_area    = dict_area_admin02
    dict_longlat = dict_longlat_admin02

  # Add nodes
  node_id   = 0
  ipop_time = dict()
  
  for loc_name in dict_pop:
    if(any([loc_name.startswith(val) for val in geog_list])):
      ipop_time[loc_name] = dict_pop[loc_name][1] + 0.5
      node_id   = node_id + 1
      ln_r0_sig = np.sqrt(np.log(NODE_R0_VAR+1.0))
      ln_r0_mu  = -0.5*ln_r0_sig*ln_r0_sig
      R0_mult   = np.random.lognormal(mean=ln_r0_mu,sigma=ln_r0_sig)
      node_dict = dict()
      node_dict['NodeID']         =   node_id
      node_dict['Name']           =   loc_name
      
      node_dict['NodeAttributes'] = {'InitialPopulation':        dict_pop[loc_name][0],
                                     'Longitude':                dict_longlat[loc_name][0],
                                     'Latitude':                 dict_longlat[loc_name][1],
                                     'Area':                     dict_area[loc_name],
                                     'InfectivityMultiplier':    R0_mult}

      if(USE_ZGRP):
        node_dict['IndividualProperties'] = list()
        nzg_frac = np.random.beta(NZG_ALPHA,NZG_BETA)*NGZ_SCALE
        if(nzg_frac < 0.01):
            nzg_frac = 0.01
        nzg_mval = np.power(nzg_frac,-1.0)

        pop_frac = [1.0-nzg_frac,nzg_frac]
        mult_mat = np.array([[0.0,      0.0],
                             [0.0, nzg_mval]])

        ipdict = dict()

        ipdict = {'Initial_Distribution':  pop_frac,
                  'Property':              'Geographic',
                  'Values':                ['L00','L01'],
                  'Transitions':           list(),
                  'TransmissionMatrix':   {'Matrix':  mult_mat.tolist() ,
                                           'Route':           'Contact' } }

        node_dict['IndividualProperties'].append(ipdict)

      json_set['Nodes'].append(node_dict)


  # ***** Write node name bookkeeping *****

  nname_dict     = {node_obj['Name']:node_obj['NodeID'] for node_obj in json_set['Nodes']}
  node_rep_list  = sorted([nname for nname in dict_pop_admin02.keys() if
                                             any([nname.startswith(val) for val in geog_list])])
  rep_groups     = {nrep:[nname_dict[val] for val  in nname_dict.keys() if val.startswith(nrep+':') or val == nrep]
                                          for nrep in node_rep_list}

  gdata.demog_node_map = rep_groups


  node_rep_dict = {val[0]:val[1]+1 for val in zip(node_rep_list,range(len(node_rep_list)))}
  with open('node_names.json','w')  as fid01:
    json.dump(node_rep_dict,fid01,sort_keys=True)

  gdata.demog_rep_index = node_rep_dict


  # ***** Prune small nodes *****

  gdata.demog_min_pop = 50

  rev_node_list = [node_obj for node_obj in json_set['Nodes'] 
                         if node_obj['NodeAttributes']['InitialPopulation'] >= gdata.demog_min_pop]

  json_set['Nodes'] = rev_node_list

  node_name_dict = {node_obj['Name']:node_obj['NodeID'] for node_obj in json_set['Nodes']}

  gdata.demog_node = node_name_dict


  # ***** Update defaults in primary file ****

  nadict = dict()

  nadict['InfectivityOverdispersion']   =   PROC_DISPER

  json_set['Defaults']['NodeAttributes'].update(nadict)


  iadict = dict()

  iadict['AcquisitionHeterogeneityVariance']   =   IND_RISK_VAR

  json_set['Defaults']['IndividualAttributes'].update(iadict)


  ipdict = dict()

  if(not USE_ZGRP):
    mult_mat = np.array([[0.0, 0.0],
                         [0.0, 1.0]])

    ipdict['Initial_Distribution']  = [0.0, 1.0]
    ipdict['Property']              = 'Geographic'
    ipdict['Values']                = ['L00','L01']
    ipdict['Transitions']           = list()
    ipdict['TransmissionMatrix']    = {'Matrix':  mult_mat.tolist() ,
                                       'Route':           'Contact' }

  json_set['Defaults']['IndividualProperties'].append(ipdict)


  # ***** Populate birth, mortality, initial ages in vital dynamics overlays *****

  # Remove mortality aliases from ref data
  ddeath_keys = list(dict_death.keys())
  for rname in ddeath_keys:
    if(rname in dict_alias):
      for rname_val in dict_alias[rname]:
        dict_death[rname_val] = dict_death[rname]
      dict_death.pop(rname)

  # Remove birth aliases from ref data
  dbirth_keys = list(dict_birth.keys())
  for rname in dict_birth:
    if(rname in dict_alias):
      for rname_val in dict_alias[rname]:
        dict_birth[rname_val] = dict_birth[rname]
      dict_birth.pop(rname)

  # Create list of vital dynamics overlays
  vd_over_list = list()
  for node_dict in json_set['Nodes']:
    node_name  = node_dict['Name']
    node_id    = node_dict['NodeID']
    node_birth = None
    node_death = None

    for rname in dict_death:
      if(node_name.startswith(rname+':') or node_name==rname):
        if(node_death is None):
          node_death = np.array(dict_death[rname])
        else:
          raise Exception("Duplicate mortality data")

    for rname in dict_birth:
      if(node_name.startswith(rname+':') or node_name==rname):
        if(node_birth is None):
          node_birth = np.array(dict_birth[rname])
        else:
          raise Exception("Duplicate birthrate data")

    match_found = False
    for data_tup in vd_over_list:
      if(np.all(np.equal(data_tup[0],node_birth)) and
         np.all(np.equal(data_tup[1],node_death))):
        data_tup[2].append(node_id)
        match_found = True
        break

    if(not match_found):
      vd_over_list.append((node_birth,node_death,[node_id]))


  # ***** Write vital dynamics overlays *****

  for k1 in range(len(vd_over_list)):
    data_tup = vd_over_list[k1]
    over_set = dict()

    # Age initialization magic
    b_rate   = data_tup[0].item()
    d_rate_y = data_tup[1].tolist()
    d_rate_x = dict_death['BIN_EDGES']
    (grow_rate, age_x, age_y) = demoCalc_AgeDist(b_rate,d_rate_x,d_rate_y)

    # Update initial node populations
    for node_dict in json_set['Nodes']:
      node_name  = node_dict['Name']
      node_id    = node_dict['NodeID']
      if(node_id in data_tup[2]):
        start_year = (gdata.start_off+TIME_START)/365.0 + 1900
        ref_year   = ipop_time[loc_name]
        mult_fac   = grow_rate**(start_year-ref_year)
        node_dict['NodeAttributes']['InitialPopulation'] =  \
             int(mult_fac * node_dict['NodeAttributes']['InitialPopulation'])

    over_set['Metadata'] = { 'IdReference':   'polio-custom' }
    over_set['Defaults'] = { 'IndividualAttributes': dict()  ,
                             'NodeAttributes':       dict()  }
    over_set['Nodes']    = [{'NodeID':val} for val in data_tup[2]]

    over_set['Defaults']['NodeAttributes']['GrowthRate'] = grow_rate
    over_set['Defaults']['NodeAttributes']['BirthRate']  = b_rate
    over_set['Defaults']['IndividualAttributes']['MortalityDistribution'] = \
               {'NumPopulationGroups':                     [2,len(d_rate_x)] ,
                'NumDistributionAxes':                                     2 ,
                'AxisNames':                                ['gender','age'] ,
                'AxisScaleFactors':                                    [1,1] ,
                'ResultScaleFactor':                                       1 ,
                'PopulationGroups':                        [[0,1], d_rate_x] ,
                'ResultValues':                          [d_rate_y,d_rate_y] }
    over_set['Defaults']['IndividualAttributes']['AgeDistribution'] = \
               {'DistributionValues':                                [age_x] ,
                'ResultScaleFactor':                                       1 ,
                'ResultValues':                                      [age_y] }

    nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_vd{:03}.json'.format(k1)
    nfname = os.path.join(PATH_OVERLAY,nfname)
    gdata.demog_files.append(nfname)
    with open(nfname,'w')  as fid01:
      json.dump(over_set,fid01,sort_keys=True)


  # ***** Populate susceptibility overlays *****

  # Load immunity mapper data
  imm_map_dat = dict()
  if(LOWER_INIT):
    init_sus_val = 50
  else:
    init_sus_val = 80

  fname = 'NGA_SUSINIT_{:02d}pct.json'.format(init_sus_val)
  with open(os.path.join('Assets','data', fname)) as fid01:
    isus_dict = json.load(fid01)

  isus_name = np.array(isus_dict['namevec'])
  isus_time = np.array(isus_dict['timevec'])
  isus_ages = np.array(isus_dict['agesvec'])

  for k1 in range(isus_ages.shape[0]):
    aval  = isus_ages[k1]
    fname = 'NGA_SUSINIT_{:02d}pct_{:02d}.csv'.format(init_sus_val,isus_ages[k1])
    imm_map_dat[aval] = np.loadtxt(os.path.join('Assets','data',fname),delimiter=',')


  # Create list of initial susceptibility overlays
  is_over_list = list()
  for node_dict in json_set['Nodes']:
    node_name  = node_dict['Name']
    node_id    = node_dict['NodeID']
    node_initsus = None


    for k1 in range(isus_name.shape[0]):
      rname = isus_name[k1]
      if(node_name.startswith(rname+':') or node_name==rname):
        if(node_initsus is None):
          node_initsus = list()
          for k2 in range(isus_ages.shape[0]):
            aval          = isus_ages[k2]
            node_isus_dat = imm_map_dat[aval][k1,:]
            node_initsus.append(np.interp(gdata.start_off+TIME_START,isus_time,node_isus_dat))
          node_initsus = np.array(node_initsus)
        else:
          raise Exception("Duplicate susceptibility data")

    match_found = False
    for data_tup in is_over_list:
      if(np.all(np.equal(data_tup[0],node_initsus))):
        data_tup[1].append(node_id)
        match_found = True
        break

    if(not match_found):
      is_over_list.append((node_initsus,[node_id]))


  # ***** Write susceptibility overlays *****
  for k1 in range(len(is_over_list)):
    isus_x     = [0.0] + (365.0*(isus_ages+3.0)/12.0).tolist() + [365.0*10.0]
    isus_y     = [1.0] + is_over_list[k1][0].tolist()          + [0.0]

    over_set   = dict()

    over_set['Metadata'] = { 'IdReference':   'polio-custom' }
    over_set['Defaults'] = { 'IndividualAttributes': dict()  ,
                             'NodeAttributes':       dict()  }
    over_set['Nodes']    = [{'NodeID':val} for val in is_over_list[k1][1]]

    over_set['Defaults']['IndividualAttributes']['SusceptibilityDistribution'] = \
               {'DistributionValues':                                 isus_x ,
                'ResultScaleFactor':                                       1 ,
                'ResultValues':                                       isus_y }

    nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_is{:03}.json'.format(k1)
    nfname = os.path.join(PATH_OVERLAY,nfname)
    gdata.demog_files.append(nfname)
    with open(nfname,'w')  as fid01:
      json.dump(over_set,fid01,sort_keys=True)


  # ***** Write primary demographics file *****

  with open(DEMOG_FILENAME,'w')  as fid01:
    json.dump(json_set,fid01,sort_keys=True)

  # Save the demographics object for use in other functions
  gdata.demog_dict       = json_set


  return None

#*******************************************************************************