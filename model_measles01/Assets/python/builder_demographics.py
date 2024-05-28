# *****************************************************************************
#
# Demographics file and overlays.
#
# *****************************************************************************

import os
import json

import global_data as gdata

import numpy as np

from sklearn.cluster import KMeans

from emod_api.demographics.Demographics import Demographics, Node
from emod_api.demographics import DemographicsTemplates as DT

from emod_demog_func import demog_vd_calc, demog_vd_over, demog_is_over
from emod_constants import DEMOG_FILE, MORT_XVAL

# *****************************************************************************


def demographicsBuilder():

    # Variables for this simulation
    R0 = gdata.var_params['R0']
    LOG10_IMP = gdata.var_params['log10_import_mult']
    REF_YEAR = gdata.var_params['ref_year']
    SS_DEMOG = True
    RUN_NUM = gdata.var_params['run_number']
    FNAME_CLASS = gdata.var_params['file_classifier']
    TARG_CLUST = gdata.var_params['target_cluster']

    # Load reference data
    dat_file = 'pop_dat_COD.csv'
    fname_pop = os.path.join('Assets', 'data', dat_file)
    pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')
    year_vec = pop_input[0, :] - gdata.base_year
    year_init = REF_YEAR - gdata.base_year
    pop_mat = pop_input[1:, :] + 0.1
    pop_init = [np.interp(year_init, year_vec, pop_mat[idx, :])
                for idx in range(pop_mat.shape[0])]



    # Random geography
    fname = os.path.join('Assets', 'data', 'latlong_NGA.json')
    with open(fname) as fid01:
        dict_latlong = json.load(fid01)

    fname = os.path.join('Assets', 'data', 'pop_NGA.json')
    with open(fname) as fid01:
        dict_pop = json.load(fid01)

    fname = os.path.join('Assets', 'data', FNAME_CLASS)
    with open(fname) as fid01:
        dict_class = json.load(fid01)

    list_name = list(dict_pop.keys())
    vec_pop = np.array([dict_pop[val] for val in list_name])
    vec_yx = np.array([[dict_latlong[val][0],dict_latlong[val][1]] for val in list_name])
    vec_class = np.array([dict_class[val] for val in list_name])

    class_idx = (vec_class==TARG_CLUST)
    vec_pop = vec_pop[class_idx]
    vec_yx = vec_yx[class_idx]

    tpop = np.sum(vec_pop)
    ktarg = int(tpop/gdata.init_pop)
    sub_clust = KMeans(n_clusters=ktarg, random_state=RUN_NUM).fit(vec_yx, sample_weight=vec_pop)
    sub_label = sub_clust.labels_

    area_dict = dict()
    for k1 in range(ktarg):
        sub_yx = vec_yx[sub_label==k1]
        dy = np.max(sub_yx[:,0]) - np.min(sub_yx[:,0])
        dx = np.max(sub_yx[:,1]) - np.min(sub_yx[:,1])
        a_est = dx*dy
        area_dict[k1] = a_est

    alistmed = np.median([area_dict[keyval] for keyval in area_dict])
    targ_clu = np.random.randint(ktarg)
    while(area_dict[targ_clu] > alistmed):
        targ_clu = np.random.randint(ktarg)

    pop_set = vec_pop[sub_label==targ_clu][:]
    long_set = vec_yx[sub_label==targ_clu][:,0]
    lat_set = vec_yx[sub_label==targ_clu][:,1]



    # Populate nodes in primary file
    node_list = list()
    for k1 in range(pop_set.shape[0]):
        node_id = 1 + k1
        node_pop = pop_set[k1]
        imp_rate = R0/6.0 * node_pop * 1.615e-7 * np.power(10.0, LOG10_IMP)
        nname = 'EXAMPLE:A{:05d}'.format(node_id)
        node_obj = Node(lat=lat_set[k1], lon=long_set[k1], pop=node_pop,
                        name=nname, forced_id=node_id)
        irs_key = 'InfectivityReservoirSize'
        node_obj.node_attributes.extra_attributes = {irs_key: imp_rate}
        node_list.append(node_obj)

    # Create primary file
    ref_name = 'Demographics_Datafile'
    demog_obj = Demographics(nodes=node_list, idref=ref_name)

    # Update defaults in primary file
    demog_obj.raw['Defaults']['IndividualAttributes'].clear()
    demog_obj.raw['Defaults']['NodeAttributes'].clear()

    # Calculate vital dynamics
    vd_tup = demog_vd_calc(year_vec, year_init, pop_mat, pop_init)

    mort_year = vd_tup[0]
    mort_mat = vd_tup[1]
    age_x = vd_tup[2]
    age_y = None
    birth_rate = vd_tup[3]
    br_mult_x = vd_tup[4]
    br_mult_y = vd_tup[5]

    if (SS_DEMOG):
        br_mult_y = 1.0 + 0.0*br_mult_y
        mort_vec = np.array([np.interp(year_init, mort_year, mort_mat[idx, :])
                             for idx in range(mort_mat.shape[0])])
        mort_year = [year_init]
        mort_mat = mort_vec[:, np.newaxis]
        mort_vec = mort_vec.tolist()
        forcing_vec = 12*[1.0]  # No seasonal forcing
        (_, age_x_eq, age_y_eq) = DT._computeAgeDist(birth_rate, MORT_XVAL,
                                                     mort_vec, forcing_vec)
        age_x = age_x_eq
        age_y = age_y_eq

    gdata.brate_mult_x = br_mult_x.tolist()
    gdata.brate_mult_y = br_mult_y.tolist()

    # Write vital dynamics overlay
    n_list = [node_obj.forced_id for node_obj in node_list]
    nfname = demog_vd_over(ref_name, n_list, birth_rate,
                           mort_year, mort_mat, age_x, age_y)
    gdata.demog_files.append(nfname)

    # Write initial susceptibility overlay
    n_list = [node_obj.forced_id for node_obj in node_list]
    nfname = demog_is_over(ref_name, n_list, R0, age_x, age_y)
    gdata.demog_files.append(nfname)

    # Write primary demographics file
    demog_obj.generate_file(name=DEMOG_FILE)

    # Save filename to global data for use in other functions
    gdata.demog_files.append(DEMOG_FILE)

    # Save the demographics object for use in other functions
    gdata.demog_object = demog_obj

    return None

# *****************************************************************************
