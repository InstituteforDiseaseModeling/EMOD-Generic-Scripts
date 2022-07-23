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

from emod_api.demographics          import DemographicsTemplates as DT

#********************************************************************************

br_base_val   = 53.0

mr_xval = [     0.6,    29.5,    29.6,   359.5,   359.6,  1829.5,
             1829.6,  3659.5,  3659.6,  5489.5,  5489.6,  7289.5,
             7289.6,  9119.5,  9119.6, 10949.5, 10949.6, 12779.5,
            12779.6, 14609.5, 14609.6, 16439.5, 16439.6, 18239.5,
            18239.6, 20069.5, 20069.6, 21899.5, 21899.6, 23729.5,
            23729.6, 25559.5, 25559.6, 27389.5, 27389.6, 29189.5,
            29189.6, 31019.5, 31019.6, 32849.5, 32849.6, 34679.5,
            34679.6, 36509.5, 36509.6, 38339.5, 38339.6, 40139.5,
            40139.6, 41969.5, 41969.6, 43799.5, 43799.6, 43829.5]

mr_yval = [ 8.02e-4, 8.02e-4, 1.52e-4, 1.52e-4, 4.79e-5, 4.79e-5,
            2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5,
            2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5,
            2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5,
            2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5,
            2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5,
            2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5, 2.35e-5,
            1.00e-0, 1.00e-0, 1.00e-0, 1.00e-0, 1.00e-0, 1.00e-0,
            1.00e-0, 1.00e-0, 1.00e-0, 1.00e-0, 1.00e-0, 1.00e-0]

#********************************************************************************

def demographicsBuilder():

  DEMOG_FILENAME = 'demographics.json'
  SETTING        = 'AFRO:DRCONGO'

  PATH_OVERLAY = 'demog_overlay'
  if(not os.path.exists(PATH_OVERLAY)):
    os.mkdir(PATH_OVERLAY)


  # ***** Get variables for this simulation *****
  R0           = gdata.var_params['R0']
  #LOG10_IMP    = gdata.var_params['log10_import_rate']


  # ***** Populate nodes in primary file *****
  node_list = list()
  imp_rate  = 0.03229*R0/6.0

  init_pop   = 200000
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
  REF_NAME   = 'DRC_Demographics_Steady-State'
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


  # ***** Write vital dynamics and susceptibility initialization overlays *****

  # Calculate equilibrium distribution
  birth_rate      = br_base_val/1000.0/365.0
  mort_vec_X      = mr_xval
  mort_vec_Y      = mr_yval
  forcing_vec     = 12*[1.0]                 # No seasonal forcing

  (grow_rate, age_x, age_y) = DT._computeAgeDist(birth_rate,mort_vec_X,mort_vec_Y,forcing_vec)

  # Vital dynamics overlays
  dover_obj                                               = DemographicsOverlay()
  dover_obj.node_attributes                               = NodeAttributes()
  dover_obj.individual_attributes                         = IndividualAttributes()
  dover_obj.individual_attributes.age_distribution        = IndividualAttributes.AgeDistribution()
  dover_obj.individual_attributes.mortality_distribution  = IndividualAttributes.MortalityDistribution()

  dover_obj.meta_data  = {'IdReference': REF_NAME}

  dover_obj.nodes      = [node_obj.forced_id for node_obj in node_list]

  dover_obj.node_attributes.birth_rate   = birth_rate
  dover_obj.node_attributes.growth_rate  = grow_rate

  dover_obj.individual_attributes.age_distribution.distribution_values  = [age_x]
  dover_obj.individual_attributes.age_distribution.result_scale_factor  = 1
  dover_obj.individual_attributes.age_distribution.result_values        = [age_y]

  dover_obj.individual_attributes.mortality_distribution.axis_names             = ['gender','age']
  dover_obj.individual_attributes.mortality_distribution.axis_scale_factors     = [1,1]
  dover_obj.individual_attributes.mortality_distribution.num_distribution_axes  = 2
  dover_obj.individual_attributes.mortality_distribution.num_population_groups  = [2,len(mort_vec_X)]
  dover_obj.individual_attributes.mortality_distribution.population_groups      = [[0,1], mort_vec_X]
  dover_obj.individual_attributes.mortality_distribution.result_scale_factor    = 1
  dover_obj.individual_attributes.mortality_distribution.result_values          = [mort_vec_Y,mort_vec_Y]

  nfname = DEMOG_FILENAME.rsplit('.',1)[0] + '_vd.json'
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