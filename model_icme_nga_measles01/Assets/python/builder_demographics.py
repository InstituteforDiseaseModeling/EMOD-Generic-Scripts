#********************************************************************************
#
# Builds a demographics file and overlays for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy                    as    np
import scipy.optimize           as    opt

from refdat_population_admin02     import data_dict   as dict_pop
from refdat_area_admin02           import data_dict   as dict_area
from refdat_location_admin02       import data_dict   as dict_longlat

from refdat_birthrate              import data_dict   as dict_birth

from aux_demo_calc                 import demoCalc_AgeDist

from emod_api.demographics.Demographics            import Demographics, \
                                                          DemographicsOverlay
from emod_api.demographics.Node                    import Node
from emod_api.demographics.PropertiesAndAttributes import IndividualAttributes, \
                                                          NodeAttributes

#********************************************************************************

mr_xval      = [     0.6,  1829.5,  1829.6,  3659.5,  3659.6,  5489.5,
                  5489.6,  7289.5,  7289.6,  9119.5,  9119.6, 10949.5,
                 10949.6, 12779.5, 12779.6, 14609.5, 14609.6, 16439.5,
                 16439.6, 18239.5, 18239.6, 20069.5, 20069.6, 21899.5,
                 21899.6, 23729.5, 23729.6, 25559.5, 25559.6, 27389.5,
                 27389.6, 29189.5, 29189.6, 31019.5, 31019.6, 32849.5,
                 32849.6, 34679.5, 34679.6, 36509.5, 36509.6, 38339.5]

pop_age_days = [     0,    1825,    3650,    5475,    7300,    9125,
                 10950,   12775,   14600,   16425,   18250,   20075,
                 21900,   23725,   25550,   27375,   29200,   31025,
                 32850,   34675,   36500]

#********************************************************************************

def demographicsBuilder():

  BASE_YEAR        = gdata.base_year
  START_YEAR       = gdata.start_year
  MAX_DAILY_MORT   = 0.01

  DEMOG_FILENAME   = 'demographics.json'
  PATH_OVERLAY     = 'demog_overlay'
  POP_DAT_STR      = 'NGA'
  REF_NAME         = 'ICME_NGA'

  gdata.demog_files.append(DEMOG_FILENAME)

  if(not os.path.exists(PATH_OVERLAY)):
    os.mkdir(PATH_OVERLAY)


  # ***** Get variables for this simulation *****
  STATE_NAME   = gdata.var_params['nga_state_name']

  R0           = gdata.var_params['R0']


  # ***** Load reference data *****
  fname_pop = os.path.join('Assets','data','pop_dat_{:s}.csv'.format(POP_DAT_STR))
  pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

  year_vec  = pop_input[0,:]  - BASE_YEAR
  year_init = START_YEAR      - BASE_YEAR
  pop_mat   = pop_input[1:,:] + 0.1

  pop_init  = [np.interp(year_init, year_vec, pop_mat[idx,:]) for idx in range(pop_mat.shape[0])]


  # ***** Populate nodes in primary file *****
  node_list = list()
  node_id   = 0
  ipop_time = dict()

  GEOG_LIST = ['AFRO:NIGERIA:{:s}'.format(STATE_NAME)]

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

      imp_rate = R0/6.0 * dict_pop[loc_name][0] * 1.0e-6
      node_obj.node_attributes.extra_attributes = {'InfectivityReservoirSize': imp_rate}

      node_list.append(node_obj)


  # ***** Write node name bookkeeping *****

  nname_dict     = {node_obj.name: node_obj.forced_id for node_obj in node_list}
  node_rep_list  = sorted([nname for nname in dict_pop.keys() if
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
  demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)

  demog_obj.raw['Defaults']['IndividualAttributes'].clear()
  iadict = dict()
  demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)


  # ***** Calculate vital dynamics ****

  diff_ratio = (pop_mat[:-1,:-1]-pop_mat[1:,1:])/pop_mat[:-1,:-1]
  t_delta    = np.diff(year_vec)
  pow_vec    = 365.0*t_delta
  mortvecs   = 1.0-np.power(1.0-diff_ratio,1.0/pow_vec)
  mortvecs   = np.minimum(mortvecs, MAX_DAILY_MORT)
  mortvecs   = np.maximum(mortvecs,            0.0)
  tot_pop    = np.sum(pop_mat,axis=0)
  tpop_mid   = (tot_pop[:-1]+tot_pop[1:])/2.0
  pop_corr   = np.exp(-mortvecs[0,:]*pow_vec/2.0)

  brate_vec  = np.round(pop_mat[0,1:]/tpop_mid/t_delta*1000.0,1)/pop_corr
  brate_val  = np.interp(year_init, year_vec[:-1], brate_vec)

  yrs_off    = year_vec[:-1]-year_init
  yrs_dex    = (yrs_off>0)

  brmultx_01 = np.array([0.0] + (365.0*yrs_off[yrs_dex]).tolist())
  brmulty_01 = np.array([1.0] + (brate_vec[yrs_dex]/brate_val).tolist())
  brmultx_02 = np.zeros(2*len(brmultx_01)-1)
  brmulty_02 = np.zeros(2*len(brmulty_01)-1)

  brmultx_02[0::2] = brmultx_01[0:]
  brmulty_02[0::2] = brmulty_01[0:]
  brmultx_02[1::2] = brmultx_01[1:]-0.5
  brmulty_02[1::2] = brmulty_01[0:-1]

  gdata.brate_mult_x = brmultx_02.tolist()
  gdata.brate_mult_y = brmulty_02.tolist() 


  # ***** Write vital dynamics and susceptibility initialization overlays *****

  # Age initialization magic
  brth_rate = dict_birth[GEOG_LIST[0]]
  mort_init = [np.interp(year_init, year_vec[:-1], mortvecs[idx,:]) for idx in range(mortvecs.shape[0])]

  d_rate_y         = np.zeros(len(mr_xval),dtype=float)
  d_rate_y[0:-2:2] = mort_init
  d_rate_y[1:-2:2] = mort_init
  d_rate_y[-2:]    = MAX_DAILY_MORT
  d_rate_y         = d_rate_y.tolist()

  d_rate_x  = mr_xval
  force_v   = 12*[1.0] # No seasonal forcing
  (grow_rate, age_x, age_y) = demoCalc_AgeDist(brth_rate,d_rate_x,d_rate_y)

  # Update initial node populations
  for node_dict in demog_obj.nodes:
    node_name  = node_dict.name
    node_id    = node_dict.forced_id
    ref_year   = ipop_time[node_name]
    mult_fac   = grow_rate**(START_YEAR-ref_year)
    new_pop    = int(mult_fac * node_dict.node_attributes.initial_population)
    node_dict.node_attributes.initial_population = new_pop

  # Save total initial population
  gdata.init_pop = sum([node_obj.pop for node_obj in node_list])

  # Overlay json
  vd_over_dict = dict()

  mort_vec_X      = mr_xval
  mort_year       = np.zeros(2*year_vec.shape[0]-3)

  mort_year[0::2] = year_vec[0:-1]
  mort_year[1::2] = year_vec[1:-1]-1e-4
  mort_year       = mort_year.tolist()

  mort_mat = np.zeros((len(mort_vec_X),len(mort_year)))

  mort_mat[0:-2:2,0::2] = mortvecs
  mort_mat[1:-2:2,0::2] = mortvecs
  mort_mat[0:-2:2,1::2] = mortvecs[:,:-1]
  mort_mat[1:-2:2,1::2] = mortvecs[:,:-1]
  mort_mat[-2:   , :]   = MAX_DAILY_MORT

  # Vital dynamics overlays
  vd_over_dict['Defaults']  =  { 'IndividualAttributes':         dict() ,
                                 'NodeAttributes':               dict() }

  vd_over_dict['Metadata']  =  { 'IdReference': REF_NAME }

  vd_over_dict['Nodes']     = [{'NodeID':node_obj.forced_id} for node_obj in node_list]

  vd_over_dict['Defaults']['NodeAttributes']        = { 'BirthRate':                brth_rate }

  vd_over_dict['Defaults']['IndividualAttributes']  = { 'AgeDistribution':              dict() ,
                                                        'MortalityDistributionMale':    dict() ,
                                                        'MortalityDistributionFemale':  dict() }

  vd_over_dict['Defaults']['IndividualAttributes']['AgeDistribution']['DistributionValues']  = [age_x]
  vd_over_dict['Defaults']['IndividualAttributes']['AgeDistribution']['ResultScaleFactor']   = 1
  vd_over_dict['Defaults']['IndividualAttributes']['AgeDistribution']['ResultValues']        = [age_y]

  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['AxisNames']             = ['age','year']
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['AxisScaleFactors']      = [1,1]
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['NumDistributionAxes']   = 2
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['NumPopulationGroups']   = [len(mort_vec_X), len(mort_year)]
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['PopulationGroups']      = [mort_vec_X, mort_year]
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['ResultScaleFactor']     = 1
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionMale']['ResultValues']          = mort_mat.tolist()

  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['AxisNames']           = ['age','year']
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['AxisScaleFactors']    = [1,1]
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['NumDistributionAxes'] = 2
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['NumPopulationGroups'] = [len(mort_vec_X), len(mort_year)]
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['PopulationGroups']    = [mort_vec_X, mort_year]
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['ResultScaleFactor']   = 1
  vd_over_dict['Defaults']['IndividualAttributes']['MortalityDistributionFemale']['ResultValues']        = mort_mat.tolist()

  nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_vd.json'
  nfname = os.path.join(PATH_OVERLAY,nfname)
  gdata.demog_files.append(nfname)

  with open(nfname, 'w') as fid01:
    json.dump(vd_over_dict, fid01, indent=3)

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

  dover_obj.nodes      = [node_obj.forced_id for node_obj in node_list]

  dover_obj.individual_attributes.susceptibility_distribution.distribution_values  = isus_x
  dover_obj.individual_attributes.susceptibility_distribution.result_scale_factor  = 1
  dover_obj.individual_attributes.susceptibility_distribution.result_values        = isus_y

  nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_is.json'
  nfname = os.path.join(PATH_OVERLAY,nfname)
  gdata.demog_files.append(nfname)
  dover_obj.to_file(file_name=nfname)


  # ***** Write primary demographics file *****

  demog_obj.generate_file(name=DEMOG_FILENAME)

  # Save the demographics object for use in other functions
  gdata.demog_object = demog_obj


  return None

#*******************************************************************************