# *****************************************************************************
#
# Demographics file and overlays.
#
# *****************************************************************************

import json
import os

import global_data as gdata

from emod_api.demographics.Demographics import Demographics, Node, \
                                               DemographicsOverlay

from emod_api.demographics.PropertiesAndAttributes import \
                                               IndividualAttributes, \
                                               NodeAttributes

import numpy as np

from emod_constants import MORT_XVAL, POP_AGE_DAYS, MAX_DAILY_MORT

# *****************************************************************************

DEMOG_FILENAME = 'demographics.json'

# *****************************************************************************


def demographicsBuilder():

    # Variables for this simulation
    START_YEAR = gdata.var_params['start_year']
    POP_DAT_STR = gdata.var_params['pop_dat_file']



    PATH_OVERLAY = 'demog_overlay'

    if (not os.path.exists(PATH_OVERLAY)):
        os.mkdir(PATH_OVERLAY)



    # Load reference data
    dat_file = 'pop_dat_{:s}.csv'.format(POP_DAT_STR)
    fname_pop = os.path.join('Assets', 'data', dat_file)
    pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')
    year_vec = pop_input[0, :] - gdata.base_year
    year_init = START_YEAR - gdata.base_year
    pop_mat = pop_input[1:, :] + 0.1
    pop_init = [np.interp(year_init, year_vec, pop_mat[idx, :])
                for idx in range(pop_mat.shape[0])]
    gdata.init_pop = int(np.sum(pop_init))



    # Populate nodes in primary file
    node_list = list()
    node_obj = Node(lat=0.0, lon=0.0, pop=gdata.init_pop,
                    name=POP_DAT_STR, forced_id=1)
    node_list.append(node_obj)

    # Create primary file
    ref_name = 'Demographics_Datafile'
    demog_obj = Demographics(nodes=node_list, idref=ref_name)

    # Update defaults in primary file
    demog_obj.raw['Defaults']['IndividualAttributes'].clear()
    demog_obj.raw['Defaults']['NodeAttributes'].clear()



    # Calculate vital dynamics
    diff_ratio = (pop_mat[:-1, :-1]-pop_mat[1:, 1:])/pop_mat[:-1, :-1]
    t_delta = np.diff(year_vec)
    pow_vec = 365.0*t_delta
    mortvecs = 1.0-np.power(1.0-diff_ratio, 1.0/pow_vec)
    mortvecs = np.minimum(mortvecs, MAX_DAILY_MORT)
    mortvecs = np.maximum(mortvecs, 0.0)
    tot_pop = np.sum(pop_mat, axis=0)
    tpop_mid = (tot_pop[:-1]+tot_pop[1:])/2.0
    pop_corr = np.exp(-mortvecs[0, :]*pow_vec/2.0)

    brate_vec = np.round(pop_mat[0, 1:]/tpop_mid/t_delta*1000.0, 1)/pop_corr
    brate_val = np.interp(year_init, year_vec[:-1], brate_vec)
    yrs_off = year_vec[:-1]-year_init
    yrs_dex = (yrs_off > 0)

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

    age_y = POP_AGE_DAYS
    age_init_cdf = np.cumsum(pop_init[:-1])/np.sum(pop_init)
    age_x = [0] + age_init_cdf.tolist()

    # Write vital dynamics and susceptibility initialization overlays
    vd_over_dict = dict()

    birth_rate = brate_val/365.0/1000.0
    mort_vec_X = MORT_XVAL
    mort_year = np.zeros(2*year_vec.shape[0]-3)

    mort_year[0::2] = year_vec[0:-1]
    mort_year[1::2] = year_vec[1:-1]-1e-4
    mort_year = mort_year.tolist()

    mort_mat = np.zeros((len(mort_vec_X), len(mort_year)))

    mort_mat[0:-2:2, 0::2] = mortvecs
    mort_mat[1:-2:2, 0::2] = mortvecs
    mort_mat[0:-2:2, 1::2] = mortvecs[:, :-1]
    mort_mat[1:-2:2, 1::2] = mortvecs[:, :-1]
    mort_mat[-2:, :] = MAX_DAILY_MORT

    # Vital dynamics overlays
    vd_over_dict['Metadata'] = {'IdReference': ref_name}
    vd_over_dict['Defaults'] = {'IndividualAttributes': dict(),
                                'NodeAttributes': dict()}
    vd_over_dict['Nodes'] = [{'NodeID': node_obj.forced_id}
                             for node_obj in node_list]

    vdodd = vd_over_dict['Defaults']
    vdodd['NodeAttributes'] = {'BirthRate': birth_rate}
    vdodd['IndividualAttributes'] = {'AgeDistribution': dict(),
                                     'MortalityDistributionMale': dict(),
                                     'MortalityDistributionFemale': dict()}

    vdoddiaad = vdodd['IndividualAttributes']['AgeDistribution']
    vdoddiaad['DistributionValues'] = [age_x]
    vdoddiaad['ResultScaleFactor'] = 1
    vdoddiaad['ResultValues'] = [age_y]

    vdoddiamdm = vdodd['IndividualAttributes']['MortalityDistributionMale']
    vdoddiamdm['AxisNames'] = ['age', 'year']
    vdoddiamdm['AxisScaleFactors'] = [1, 1]
    vdoddiamdm['NumDistributionAxes'] = 2
    vdoddiamdm['NumPopulationGroups'] = [len(mort_vec_X), len(mort_year)]
    vdoddiamdm['PopulationGroups'] = [mort_vec_X, mort_year]
    vdoddiamdm['ResultScaleFactor'] = 1
    vdoddiamdm['ResultValues'] = mort_mat.tolist()

    vdoddiamdf = vdodd['IndividualAttributes']['MortalityDistributionFemale']
    vdoddiamdf['AxisNames'] = ['age', 'year']
    vdoddiamdf['AxisScaleFactors'] = [1, 1]
    vdoddiamdf['NumDistributionAxes'] = 2
    vdoddiamdf['NumPopulationGroups'] = [len(mort_vec_X), len(mort_year)]
    vdoddiamdf['PopulationGroups'] = [mort_vec_X, mort_year]
    vdoddiamdf['ResultScaleFactor'] = 1
    vdoddiamdf['ResultValues'] = mort_mat.tolist()

    nfname = DEMOG_FILENAME.rsplit('.', 1)[0] + '_vd.json'
    nfname = os.path.join(PATH_OVERLAY, nfname)
    gdata.demog_files.append(nfname)

    with open(nfname, 'w') as fid01:
        json.dump(vd_over_dict, fid01, indent=3)

    # Write primary demographics file
    demog_obj.generate_file(name=DEMOG_FILENAME)

    # Save filename to global data for use in other functions
    gdata.demog_files.append(DEMOG_FILENAME)

    # Save the demographics object for use in other functions
    gdata.demog_object = demog_obj

    return None

# *****************************************************************************
