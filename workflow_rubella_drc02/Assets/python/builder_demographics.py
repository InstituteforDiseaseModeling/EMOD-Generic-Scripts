#********************************************************************************
#
# Builds a demographics file and overlays for input to the DTK.
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy                    as    np
import scipy.optimize           as    opt

from emod_api.demographics.Demographics            import Demographics, \
                                                          DemographicsOverlay
from emod_api.demographics.Node                    import Node
from emod_api.demographics.PropertiesAndAttributes import IndividualAttributes, \
                                                          NodeAttributes

#********************************************************************************

EPS = np.finfo(float).eps

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

  DEMOG_FILENAME = 'demographics.json'
  SETTING        = 'AFRO:DRCONGO'

  PATH_OVERLAY = 'demog_overlay'
  if(not os.path.exists(PATH_OVERLAY)):
    os.mkdir(PATH_OVERLAY)


  # ***** Get variables for this simulation *****
  R0           = gdata.var_params['R0']
  INIT_AGENT   = gdata.var_params['num_agents']
  LOG10_IMP    = gdata.var_params['log10_import_mult']
  POP_DAT_STR  = gdata.var_params['pop_dat_file']


  # ***** Populate nodes in primary file *****
  node_list = list()
  imp_rate  = 0.03229*R0/6.0*INIT_AGENT/200000.0

  init_pop   = int(INIT_AGENT)
  node_id    = 1
  node_name  = SETTING+':A{:05d}'.format(node_id)

  node_obj = Node(lat         = 0.0,
                  lon         = 0.0,
                  pop         = init_pop,
                  name        = node_name,
                  forced_id   = node_id,
                  area        = 0.0)
  node_obj.node_attributes.extra_attributes = {'InfectivityReservoirSize': imp_rate}
  node_list.append(node_obj)


  # ***** Create primary file *****
  REF_NAME   = 'DRC_Demographics_Datafile'
  demog_obj  = Demographics(nodes=node_list, idref=REF_NAME)


  # ***** Update defaults in primary file ****

  demog_obj.raw['Defaults']['NodeAttributes'].clear()
  nadict = dict()
  nadict['InfectivityOverdispersion']        =   0.0
  nadict['InfectivityMultiplier']            =   1.0
  demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)

  demog_obj.raw['Defaults']['IndividualAttributes'].clear()
  iadict = dict()
  iadict['AcquisitionHeterogeneityVariance'] =   0.0
  demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)


  # ***** Calculate vital dynamics ****

  fname_pop = os.path.join('Assets','data','pop_data_{:s}.csv'.format(POP_DAT_STR))
  pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

  year_vec  = pop_input[0,:]
  pop_mat   = pop_input[1:,:]
  pop_mat   = np.append(pop_mat, np.zeros((1,year_vec.shape[0])),axis=0)

  diff_ratio = pop_mat[1:,1:]/(pop_mat[:-1,:-1]+EPS)
  pow_vec    = 365.0*np.diff(year_vec)
  mortvecs   = 1.0-np.power(diff_ratio,1.0/pow_vec)
  tot_pop    = np.sum(pop_mat,axis=0)

  brate_vec  = np.round(pop_mat[0,1:]/tot_pop[:-1]/5.0*1000.0,1)
  brate_val  = brate_vec[0]

  gdata.brate_mult_x = year_vec[:-1].tolist()
  gdata.brate_mult_y = (brate_vec/brate_val).tolist()

  age_y        = pop_age_days
  age_init_cdf = np.cumsum(pop_mat[:-1,0])/np.sum(pop_mat[:,0])
  age_x        = [0] + age_init_cdf.tolist()

  mortvecs_alt = np.copy(mortvecs)
  for k1 in range(mortvecs_alt.shape[0]-1):
    mortvecs_alt[k1,:] = np.power(mortvecs_alt[k1,:],2.0)/mortvecs_alt[k1+1,:]


  # ***** Write vital dynamics and susceptibility initialization overlays *****

  vd_over_dict = dict()

  birth_rate   = brate_val/1000.0/365.0
  mort_vec_X   = mr_xval
  mort_year    = year_vec[:-1].tolist()

  mort_mat = np.zeros((len(mort_vec_X),len(mort_year)))

  mort_mat[0:-2:2,:] = mortvecs_alt
  mort_mat[1:-2:2,:] = mortvecs_alt
  mort_mat[-2:   ,:] = 1.0

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


  # Calculate initial susceptibilities
  targ_frac   = 1.1*(1.0/R0)    # Tries to aim for Reff of 1.1;

  # Stuff below ought to get wrapped into a separate function. It's doing an implicit solve
  # of an exponential decay mapped onto the age distribution specified above. The target 
  # area-under-the-curve is the value specified by targ_frac above. Just aims to get close.
  # May break for very low target frac values (e.g., < 0.01)
  age_y_res   = np.arange(1,100*365,30)
  age_x_res   = np.interp(age_y_res, age_y, age_x)
  age_year    = np.array(age_y_res[1:])/365.0
  age_prob    = np.diff(np.array(age_x_res))

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

  # Save filename to global data for use in other functions
  gdata.demog_files.append(DEMOG_FILENAME)

  # Save the demographics object for use in other functions
  gdata.demog_object = demog_obj


  return None

#*******************************************************************************