#********************************************************************************
#
# Builds a demographics.json file to be used as input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy                    as    np

from refdat_population_admin02     import data_dict   as dict_pop_admin02
from refdat_area_admin02           import data_dict   as dict_area_admin02
from refdat_location_admin02       import data_dict   as dict_longlat_admin02

from refdat_population_100km       import data_dict   as dict_pop_100km
from refdat_area_100km             import data_dict   as dict_area_100km
from refdat_location_100km         import data_dict   as dict_longlat_100km

from refdat_alias                  import data_dict   as dict_alias
from refdat_birthrate              import data_dict   as dict_birth
from refdat_deathrate              import data_dict   as dict_death

from aux_demo_calc                 import demoCalc_AgeDist
from aux_demo_calc                 import demoCalc_hDist

from emod_api.demographics.Demographics            import Demographics, \
                                                          DemographicsOverlay
from emod_api.demographics.Node                    import Node
from emod_api.demographics.PropertiesAndAttributes import IndividualAttributes, \
                                                          IndividualProperty,   \
                                                          NodeAttributes

#********************************************************************************

def demographicsBuilder():

  DEMOG_FILENAME = 'demographics.json'
  REF_NAME       = 'polio-custom'
  GEOG_LIST      = ['AFRO:NIGERIA']


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


  # ***** Populate nodes in primary file *****

  node_list = list()

  if(SUB_LGA):
    dict_pop     = dict_pop_100km
    dict_area    = dict_area_100km
    dict_longlat = dict_longlat_100km
  else:
    dict_pop     = dict_pop_admin02
    dict_area    = dict_area_admin02
    dict_longlat = dict_longlat_admin02

  # Remove location aliases from geography list
  for rname in GEOG_LIST:
    if(rname in dict_alias):
      for rname_val in dict_alias[rname]:
        GEOG_LIST.append(rname_val)

  # Add nodes
  node_id   = 0
  ipop_time = dict()

  for loc_name in dict_pop:
    if(any([loc_name.startswith(val+':') or val == loc_name for val in GEOG_LIST])):
      ipop_time[loc_name] = dict_pop[loc_name][1] + 0.5
      node_id   = node_id + 1

      node_obj = Node(lat              = dict_longlat[loc_name][1],
                      lon              = dict_longlat[loc_name][0],
                      pop              = dict_pop[loc_name][0],
                      name             = loc_name,
                      forced_id        = node_id,
                      area             = dict_area[loc_name])

      ln_r0_sig = np.sqrt(np.log(NODE_R0_VAR+1.0))
      ln_r0_mu  = -0.5*ln_r0_sig*ln_r0_sig
      R0_mult   = np.random.lognormal(mean=ln_r0_mu,sigma=ln_r0_sig)

      node_obj.node_attributes.infectivity_multiplier = R0_mult

      if(USE_ZGRP):
        nzg_frac = NZG_BETA
        prob = np.random.uniform()
        if prob < NGZ_SCALE:
          nzg_frac = NZG_ALPHA

        nzg_mval = np.power(nzg_frac,-1.0)

        pop_frac = [1.0-nzg_frac,nzg_frac]
        mult_mat = np.array([[0.0,      0.0],
                             [0.0, nzg_mval]])

        ip_obj = IndividualProperty(initial_distribution = pop_frac,
                                    property             = 'Geographic',
                                    values               = ['L00','L01'],
                                    transitions          = list(),
                                    transmission_matrix  = {'Matrix':  mult_mat.tolist(),
                                                            'Route':           'Contact'} )

        node_obj.individual_properties.add(ip_obj)

      node_list.append(node_obj)


  # ***** Build distance matrix *****

  num_nodes = len(node_list)

  # Lat/long vectors
  xyt_vec = np.zeros((num_nodes,2))
  for k1 in range(xyt_vec.shape[0]):
    vec_idx = node_list[k1].forced_id-1
    xyt_vec[vec_idx,0] = node_list[k1].lon
    xyt_vec[vec_idx,1] = node_list[k1].lat

  # Distance matrix
  dist_mat = np.zeros((num_nodes,num_nodes))
  for k1 in range(dist_mat.shape[0]):
    dist_mat[k1,:] = demoCalc_hDist(xyt_vec[k1,1],xyt_vec[k1,0],xyt_vec[:,1],xyt_vec[:,0])

  gdata.demog_dist_mat = dist_mat


  # ***** Write node name bookkeeping *****

  nname_dict     = {node_obj.name: node_obj.forced_id for node_obj in node_list}
  node_rep_list  = sorted([nname for nname in dict_pop_admin02.keys() if
                                             any([nname.startswith(val+':') or val == nname for val in GEOG_LIST])])
  rep_groups     = {nrep:[nname_dict[val] for val  in nname_dict.keys() if val.startswith(nrep+':') or val == nrep]
                                          for nrep in node_rep_list}

  gdata.demog_node_map = rep_groups

  node_rep_dict = {val[0]:val[1]+1 for val in zip(node_rep_list,range(len(node_rep_list)))}
  with open('node_names.json','w')  as fid01:
    json.dump(node_rep_dict,fid01,sort_keys=True)

  gdata.demog_rep_index = node_rep_dict


  # ***** Prune small nodes *****

  gdata.demog_min_pop = 50

  rev_node_list  = [node_obj for node_obj in node_list
                          if node_obj.node_attributes.initial_population >= gdata.demog_min_pop]
  node_list      = rev_node_list
  node_name_dict = {node_obj.name: node_obj.forced_id for node_obj in node_list}

  gdata.demog_node = node_name_dict


  # ***** Create primary file *****

  demog_obj  = Demographics(nodes=node_list, idref=REF_NAME)

  # Save filename to global data for use in other functions
  gdata.demog_files.append(DEMOG_FILENAME)


  # ***** Update defaults in primary file ****

  demog_obj.raw['Defaults']['NodeAttributes'].clear()
  nadict = dict()
  nadict['InfectivityOverdispersion']   =   PROC_DISPER
  demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)

  demog_obj.raw['Defaults']['IndividualAttributes'].clear()
  iadict = dict()
  iadict['AcquisitionHeterogeneityVariance']   =   IND_RISK_VAR
  demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)

  if(not USE_ZGRP):
    pop_frac = [0.0, 1.0]
    mult_mat = np.array([[0.0, 0.0],
                         [0.0, 1.0]])

    demog_obj.AddIndividualPropertyAndHINT(InitialDistribution  = pop_frac,
                                           Property             = 'Geographic',
                                           Values               = ['L00','L01'],
                                           TransmissionMatrix   = mult_mat.tolist() )


  # ***** Populate vital dynamics overlays *****

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
  for node_dict in demog_obj.nodes:
    node_name  = node_dict.name
    node_id    = node_dict.forced_id
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

  demog_kid_dict = dict()

  for k1 in range(len(vd_over_list)):
    data_tup = vd_over_list[k1]
    over_set = dict()

    # Age initialization magic
    brth_rate   = data_tup[0].item()
    d_rate_y = data_tup[1].tolist()
    d_rate_x = dict_death['BIN_EDGES']
    force_v  = 12*[1.0] # No seasonal forcing
    (grow_rate, age_x, age_y) = demoCalc_AgeDist(brth_rate,d_rate_x,d_rate_y)

    # Fraction of populatin between 9 mos and 5 yrs
    targ_frac = np.interp(5.00*365.0, age_y, age_x) - np.interp(0.75*365.0, age_y, age_x)

    # Update initial node populations; calculate target populations
    for node_dict in demog_obj.nodes:
      node_name  = node_dict.name
      node_id    = node_dict.forced_id
      if(node_id in data_tup[2]):
        start_year = (gdata.start_off+TIME_START)/365.0 + 1900
        ref_year   = ipop_time[loc_name]
        mult_fac   = grow_rate**(start_year-ref_year)
        new_pop    = int(mult_fac * node_dict.node_attributes.initial_population)
        node_dict.node_attributes.initial_population = new_pop
        demog_kid_dict[node_name] = int(new_pop*targ_frac)

    dover_obj                                               = DemographicsOverlay()
    dover_obj.node_attributes                               = NodeAttributes()
    dover_obj.individual_attributes                         = IndividualAttributes()
    dover_obj.individual_attributes.age_distribution        = IndividualAttributes.AgeDistribution()
    dover_obj.individual_attributes.mortality_distribution  = IndividualAttributes.MortalityDistribution()

    dover_obj.meta_data  = {'IdReference': REF_NAME}

    dover_obj.nodes      = [nodeid for nodeid in data_tup[2]]

    dover_obj.node_attributes.birth_rate   = brth_rate
    dover_obj.node_attributes.growth_rate  = grow_rate

    dover_obj.individual_attributes.age_distribution.distribution_values  = [age_x]
    dover_obj.individual_attributes.age_distribution.result_scale_factor  = 1
    dover_obj.individual_attributes.age_distribution.result_values        = [age_y]

    dover_obj.individual_attributes.mortality_distribution.axis_names             = ['gender','age']
    dover_obj.individual_attributes.mortality_distribution.axis_scale_factors     = [1,1]
    dover_obj.individual_attributes.mortality_distribution.num_distribution_axes  = 2
    dover_obj.individual_attributes.mortality_distribution.num_population_groups  = [2,len(d_rate_x)]
    dover_obj.individual_attributes.mortality_distribution.population_groups      = [[0,1], d_rate_x]
    dover_obj.individual_attributes.mortality_distribution.result_scale_factor    = 1
    dover_obj.individual_attributes.mortality_distribution.result_values          = [d_rate_y,d_rate_y]

    nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_vd{:03}.json'.format(k1)
    nfname = os.path.join(PATH_OVERLAY,nfname)
    gdata.demog_files.append(nfname)
    dover_obj.to_file(file_name=nfname)

  # Save the target populations for use in other functions
  gdata.demog_kid_dict = demog_kid_dict

  with open('targ_pop_9mo_5yr.json','w')  as fid01:
    json.dump(demog_kid_dict,fid01,sort_keys=True,indent=3)


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
  for node_dict in demog_obj.nodes:
    node_name    = node_dict.name
    node_id      = node_dict.forced_id
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

    dover_obj                                                    = DemographicsOverlay()
    dover_obj.individual_attributes                              = IndividualAttributes()
    dover_obj.individual_attributes.susceptibility_distribution  = IndividualAttributes.SusceptibilityDistribution()

    dover_obj.meta_data  = {'IdReference': REF_NAME}

    dover_obj.nodes      = [nodeid for nodeid in is_over_list[k1][1]]

    dover_obj.individual_attributes.susceptibility_distribution.distribution_values  = isus_x
    dover_obj.individual_attributes.susceptibility_distribution.result_scale_factor  = 1
    dover_obj.individual_attributes.susceptibility_distribution.result_values        = isus_y

    nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_is{:03}.json'.format(k1)
    nfname = os.path.join(PATH_OVERLAY,nfname)
    gdata.demog_files.append(nfname)
    dover_obj.to_file(file_name=nfname)


  # ***** Write primary demographics file *****

  demog_obj.generate_file(name=DEMOG_FILENAME)

  # Save the demographics object for use in other functions
  gdata.demog_object = demog_obj



  return None

#*******************************************************************************