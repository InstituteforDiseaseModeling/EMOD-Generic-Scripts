# *****************************************************************************
#
# *****************************************************************************

import json
import os

import numpy as np

from emod_constants import DEMOG_FILE, PATH_OVERLAY, \
                           MORT_XVAL, POP_AGE_DAYS, MAX_DAILY_MORT

# *****************************************************************************


def demog_vd_over(ref_name, node_list, cb_rate,
                  mort_year, mort_mat, age_x):

    if (not os.path.exists(PATH_OVERLAY)):
        os.mkdir(PATH_OVERLAY)

    vd_over_dict = dict()

    vd_over_dict['Metadata'] = {'IdReference': ref_name}
    vd_over_dict['Defaults'] = {'IndividualAttributes': dict(),
                                'NodeAttributes': dict()}
    vd_over_dict['Nodes'] = [{'NodeID': nid} for nid in node_list]

    vdodd = vd_over_dict['Defaults']
    vdodd['NodeAttributes'] = {'BirthRate': cb_rate}
    vdodd['IndividualAttributes'] = {'AgeDistribution': dict(),
                                     'MortalityDistributionMale': dict(),
                                     'MortalityDistributionFemale': dict()}

    vdoddiaad = vdodd['IndividualAttributes']['AgeDistribution']
    vdoddiaad['DistributionValues'] = [age_x]
    vdoddiaad['ResultScaleFactor'] = 1
    vdoddiaad['ResultValues'] = [POP_AGE_DAYS]

    vdoddiamdm = vdodd['IndividualAttributes']['MortalityDistributionMale']
    vdoddiamdm['AxisNames'] = ['age', 'year']
    vdoddiamdm['AxisScaleFactors'] = [1, 1]
    vdoddiamdm['NumDistributionAxes'] = 2
    vdoddiamdm['NumPopulationGroups'] = [len(MORT_XVAL), len(mort_year)]
    vdoddiamdm['PopulationGroups'] = [MORT_XVAL, mort_year]
    vdoddiamdm['ResultScaleFactor'] = 1
    vdoddiamdm['ResultValues'] = mort_mat.tolist()

    vdoddiamdf = vdodd['IndividualAttributes']['MortalityDistributionFemale']
    vdoddiamdf['AxisNames'] = ['age', 'year']
    vdoddiamdf['AxisScaleFactors'] = [1, 1]
    vdoddiamdf['NumDistributionAxes'] = 2
    vdoddiamdf['NumPopulationGroups'] = [len(MORT_XVAL), len(mort_year)]
    vdoddiamdf['PopulationGroups'] = [MORT_XVAL, mort_year]
    vdoddiamdf['ResultScaleFactor'] = 1
    vdoddiamdf['ResultValues'] = mort_mat.tolist()

    nfname = DEMOG_FILE.rsplit('.', 1)[0] + '_vd.json'
    nfname = os.path.join(PATH_OVERLAY, nfname)

    with open(nfname, 'w') as fid01:
        json.dump(vd_over_dict, fid01)

    return nfname

# *****************************************************************************


def demog_vd_calc(year_vec, year_init, pop_mat, pop_init):

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

    age_init_cdf = np.cumsum(pop_init[:-1])/np.sum(pop_init)
    age_x = [0] + age_init_cdf.tolist()

    birth_rate = brate_val/365.0/1000.0
    mort_year = np.zeros(2*year_vec.shape[0]-3)

    mort_year[0::2] = year_vec[0:-1]
    mort_year[1::2] = year_vec[1:-1]-1e-4
    mort_year = mort_year.tolist()

    mort_mat = np.zeros((len(MORT_XVAL), len(mort_year)))

    mort_mat[0:-2:2, 0::2] = mortvecs
    mort_mat[1:-2:2, 0::2] = mortvecs
    mort_mat[0:-2:2, 1::2] = mortvecs[:, :-1]
    mort_mat[1:-2:2, 1::2] = mortvecs[:, :-1]
    mort_mat[-2:, :] = MAX_DAILY_MORT

    return (mort_year, mort_mat, age_x, birth_rate, brmultx_02, brmulty_02)


# *****************************************************************************
