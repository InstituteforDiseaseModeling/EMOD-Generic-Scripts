#********************************************************************************
#
# Builds a demographics.json file to be used as input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy                    as    np
import scipy.optimize           as    opt

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

from emod_api.demographics.Demographics            import Demographics, \
                                                          DemographicsOverlay
from emod_api.demographics.Node                    import Node
from emod_api.demographics.PropertiesAndAttributes import IndividualAttributes, \
                                                          NodeAttributes

#********************************************************************************

def demographicsBuilder():

  DEMOG_FILENAME = 'demographics.json'
  REF_NAME       = 'measles-custom'
  GEOG_LIST      = ['AFRO:NIGERIA:NORTH_CENTRAL',
                    'AFRO:NIGERIA:NORTH_EAST',
                    'AFRO:NIGERIA:NORTH_WEST']


  # ***** Get variables for this simulation *****
  START_YEAR   = gdata.var_params['start_year']

  SUB_LGA      = gdata.var_params['use_10k_res']

  R0           = gdata.var_params['R0']
  LOG10_IMP    = gdata.var_params['log10_import_rate']
  IND_RISK_VAR = gdata.var_params['ind_variance_risk']


  PATH_OVERLAY = 'demog_overlay'
  if(not os.path.exists(PATH_OVERLAY)):
    os.mkdir(PATH_OVERLAY)


  # ***** Populate nodes in primary file *****

  # Add nodes
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

  node_id   = 0
  ipop_time = dict()
  imp_case  = np.power(10.0, LOG10_IMP)

  for loc_name in dict_pop:
    if(any([loc_name.startswith(val) for val in GEOG_LIST])):
      ipop_time[loc_name] = dict_pop[loc_name][1] + 0.5
      node_id   = node_id + 1

      node_obj = Node(lat              = dict_longlat[loc_name][1],
                      lon              = dict_longlat[loc_name][0],
                      pop              = dict_pop[loc_name][0],
                      name             = loc_name,
                      forced_id        = node_id,
                      area             = dict_area[loc_name])

      imp_rate = imp_case*dict_pop[loc_name][0]/1.0e5
      node_obj.node_attributes.extra_attributes = {'InfectivityReservoirSize': imp_rate}

      node_list.append(node_obj)


  # ***** Write node name bookkeeping *****

  nname_dict     = {node_obj.name: node_obj.forced_id for node_obj in node_list}
  node_rep_list  = sorted([nname for nname in dict_pop_admin02.keys() if
                                             any([nname.startswith(val+':') or val == nname for val in GEOG_LIST])])
  rep_groups     = {nrep:[nname_dict[val] for val  in nname_dict.keys() if val.startswith(nrep+':') or val == nrep]
                                          for nrep in node_rep_list}

  gdata.demog_node_map = rep_groups

  # ***** Prune small nodes *****

  rev_node_list  = [node_obj for node_obj in node_list
                          if node_obj.node_attributes.initial_population >= gdata.demog_min_pop]
  node_list      = rev_node_list
  node_name_dict = {node_obj.name: node_obj.forced_id for node_obj in node_list}

  gdata.demog_node   = node_name_dict
  gdata.max_node_id  = max([node_name_dict[val] for val in node_name_dict])


  # ***** Create primary file *****

  demog_obj  = Demographics(nodes=node_list, idref=REF_NAME)

  # Save filename to global data for use in other functions
  gdata.demog_files.append(DEMOG_FILENAME)


  # ***** Update defaults in primary file ****

  demog_obj.raw['Defaults']['NodeAttributes'].clear()
  nadict = dict()
  nadict['InfectivityOverdispersion']        =   0.0
  nadict['InfectivityMultiplier']            =   1.0
  demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)

  demog_obj.raw['Defaults']['IndividualAttributes'].clear()
  iadict = dict()
  iadict['AcquisitionHeterogeneityVariance'] = IND_RISK_VAR
  demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)


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


  # ***** Write vital dynamics and susceptibility initialization overlays *****

  for k1 in range(len(vd_over_list)):
    data_tup = vd_over_list[k1]
    over_set = dict()

    # Age initialization magic
    brth_rate   = data_tup[0].item()
    d_rate_y = data_tup[1].tolist()
    d_rate_x = dict_death['BIN_EDGES']
    force_v  = 12*[1.0] # No seasonal forcing
    (grow_rate, age_x, age_y) = demoCalc_AgeDist(brth_rate,d_rate_x,d_rate_y)

    # Update initial node populations
    for node_dict in demog_obj.nodes:
      node_name  = node_dict.name
      node_id    = node_dict.forced_id
      if(node_id in data_tup[2]):
        ref_year   = ipop_time[loc_name]
        mult_fac   = grow_rate**(START_YEAR-ref_year)
        new_pop    = int(mult_fac * node_dict.node_attributes.initial_population)
        node_dict.node_attributes.initial_population = new_pop

    # Vital dynamics overlays
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

    # Calculate initial susceptibilities
    targ_frac   = 1.1*(1.0/R0)    # Tries to aim for Reff of 1.1;

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

    # Initial susceptibility overlays
    dover_obj                                                    = DemographicsOverlay()
    dover_obj.individual_attributes                              = IndividualAttributes()
    dover_obj.individual_attributes.susceptibility_distribution  = IndividualAttributes.SusceptibilityDistribution()

    dover_obj.meta_data  = {'IdReference': REF_NAME}

    dover_obj.nodes      = [nodeid for nodeid in data_tup[2]]

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