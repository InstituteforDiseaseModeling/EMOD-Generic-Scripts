#********************************************************************************
#
# Builds a demographics file and overlays for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy                    as    np

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
  MAX_DAILY_MORT   = 0.01

  DEMOG_FILENAME   = 'demographics.json'
  PATH_OVERLAY     = 'demog_overlay'
  SETTING          = 'PLACENAME'

  gdata.demog_files.append(DEMOG_FILENAME)

  if(not os.path.exists(PATH_OVERLAY)):
    os.mkdir(PATH_OVERLAY)


  # ***** Get variables for this simulation *****
  START_YEAR   = gdata.var_params['start_year']
  POP_DAT_STR  = gdata.var_params['pop_dat_file']


  # ***** Load reference data *****
  fname_pop = os.path.join('Assets','data','pop_dat_{:s}.csv'.format(POP_DAT_STR))
  pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

  year_vec  = pop_input[0,:]  - BASE_YEAR
  year_init = START_YEAR      - BASE_YEAR
  pop_mat   = pop_input[1:,:] + 0.1

  pop_init  = [np.interp(year_init, year_vec, pop_mat[idx,:]) for idx in range(pop_mat.shape[0])]


  # ***** Populate nodes in primary file *****
  node_list = list()

  gdata.init_pop  = int(np.sum(pop_init))
  node_id         = 1
  node_name       = POP_DAT_STR

  node_obj = Node(lat         = 0.0,
                  lon         = 0.0,
                  pop         = gdata.init_pop,
                  name        = node_name,
                  forced_id   = node_id,
                  area        = 0.0)
  node_list.append(node_obj)


  # ***** Create primary file *****
  REF_NAME   = 'Demographics_Datafile'
  demog_obj  = Demographics(nodes=node_list, idref=REF_NAME)


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

  age_y        = pop_age_days
  age_init_cdf = np.cumsum(pop_init[:-1])/np.sum(pop_init)
  age_x        = [0] + age_init_cdf.tolist()


  # ***** Write vital dynamics and susceptibility initialization overlays *****

  vd_over_dict = dict()

  birth_rate      = brate_val/365.0/1000.0
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

  vd_over_dict['Defaults']['NodeAttributes']        = { 'BirthRate':                birth_rate }

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


  # ***** Write primary demographics file *****

  demog_obj.generate_file(name=DEMOG_FILENAME)

  # Save the demographics object for use in other functions
  gdata.demog_object = demog_obj


  return None

#*******************************************************************************