# *****************************************************************************
#
# Demographics file and overlays.
#
# *****************************************************************************

import os

import global_data as gdata

import numpy as np

from emod_api.demographics.Demographics import Demographics, Node
from emod_api.demographics import DemographicsTemplates as DT

from emod_demog_func import demog_vd_calc, demog_vd_over
from emod_constants import DEMOG_FILE, MORT_XVAL

# *****************************************************************************


def demographicsBuilder():

    # Variables for this simulation
    MOD_AGE_INIT = gdata.var_params['modified_age_init']
    MORT_MULT01 = np.exp(gdata.var_params['log_mort_mult01'])
    MORT_MULT02 = np.exp(gdata.var_params['log_mort_mult02'])
    MORT_MULT03 = np.exp(gdata.var_params['log_mort_mult03'])

    # Load reference data
    fname_pop = os.path.join('Assets', 'data', 'pop_dat_GBR.csv')
    pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')
    year_vec = pop_input[0, :] - gdata.base_year
    year_init = gdata.start_year - gdata.base_year
    pop_mat = pop_input[1:, :] + 0.1
    pop_init = [np.interp(year_init, year_vec, pop_mat[idx, :])
                for idx in range(pop_mat.shape[0])]
    gdata.init_pop = int(np.sum(pop_init))

    # Retain reference data
    pop_mat_ref = np.zeros((pop_mat.shape[0], int(gdata.run_years)+1))
    for yr_idx in range(int(gdata.run_years)+1):
        yr_val = yr_idx + int(year_init)
        pop_vec_ref = [np.interp(yr_val, year_vec, pop_mat[idx, :])
                       for idx in range(pop_mat.shape[0])]
        pop_mat_ref[:, yr_idx] = pop_vec_ref
    gdata.pop_mat_ref = pop_mat_ref[:-1, :]

    # Populate nodes in primary file
    node_list = list()
    node_obj = Node(lat=0.0, lon=0.0, pop=gdata.init_pop,
                    name='GBR', forced_id=1)
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

    gdata.brate_mult_x = br_mult_x.tolist()
    gdata.brate_mult_y = br_mult_y.tolist()

    # Use mortality profile from initial year; data starts in 1950
    mort_year = [mort_year[0]]
    mort_mat = mort_mat[:, 0]
    mort_mat = mort_mat[..., np.newaxis]

    # Apply mortality modifiers
    mort_mat[0:6, 0] = mort_mat[0:6, 0]*MORT_MULT01
    mort_mat[6:24, 0] = mort_mat[6:24, 0]*MORT_MULT02
    mort_mat[24:36, 0] = mort_mat[24:36, 0]*MORT_MULT03

    # Apply equilibrium initial population distribution
    if (not MOD_AGE_INIT):
        mort_vec = mort_mat[:, 0].tolist()
        forcing_vec = 12*[1.0]  # No seasonal forcing
        (_, age_x_eq, age_y_eq) = DT._computeAgeDist(birth_rate, MORT_XVAL,
                                                     mort_vec, forcing_vec)
        age_x = age_x_eq
        age_y = age_y_eq

    # Write vital dynamics overlay
    n_list = [node_obj.forced_id for node_obj in node_list]
    nfname = demog_vd_over(ref_name, n_list, birth_rate,
                           mort_year, mort_mat, age_x, age_y)
    gdata.demog_files.append(nfname)

    # Write primary demographics file
    demog_obj.generate_file(name=DEMOG_FILE)

    # Save filename to global data for use in other functions
    gdata.demog_files.append(DEMOG_FILE)

    # Save the demographics object for use in other functions
    gdata.demog_object = demog_obj

    return None

# *****************************************************************************
