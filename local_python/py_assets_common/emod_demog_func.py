# *****************************************************************************
#
# *****************************************************************************

import json
import os

from emod_constants import DEMOG_FILENAME, PATH_OVERLAY, \
                           MORT_XVAL, POP_AGE_DAYS

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

    nfname = DEMOG_FILENAME.rsplit('.', 1)[0] + '_vd.json'
    nfname = os.path.join(PATH_OVERLAY, nfname)

    with open(nfname, 'w') as fid01:
        json.dump(vd_over_dict, fid01)

    return nfname

# *****************************************************************************
