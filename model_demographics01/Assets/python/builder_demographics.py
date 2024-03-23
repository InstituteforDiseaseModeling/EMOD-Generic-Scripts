# *****************************************************************************
#
# Demographics file and overlays.
#
# *****************************************************************************

import global_data as gdata

import numpy as np

from emod_api.demographics.Demographics import Demographics, Node
from emod_api.demographics import DemographicsTemplates as DT

from emod_constants import DEMOG_FILE, POP_AGE_DAYS

# *****************************************************************************

uk_1950_frac = [0.0000, 0.0863, 0.0719, 0.0663, 0.0631, 0.0680, 0.0768, 0.0691,
                0.0769, 0.0766, 0.0713, 0.0625, 0.0546, 0.0482, 0.0410, 0.0319,
                0.0206, 0.0103, 0.0036, 0.0008, 0.0001]

br_base_val = 15.3

br_force_xval = [   0.0,    1.0,    2.0,    3.0,    4.0,    5.0,    6.0,    7.0,
                    8.0,    9.0,   10.0,   11.0,   12.0,   13.0,   14.0,   15.0,
                   16.0,   17.0,   18.0,   19.0,   20.0,   21.0,   22.0,   23.0,
                   24.0,   25.0,   26.0,   27.0,   28.0,   29.0,   30.0]

br_force_yval = [0.9405, 0.9569, 0.9733, 0.9897, 1.0061, 1.0225, 1.0390, 1.0554,
                 1.0718, 1.0966, 1.1215, 1.1463, 1.1712, 1.1961, 1.1780, 1.1599,
                 1.1418, 1.1238, 1.1057, 1.0614, 1.0172, 0.9730, 0.9288, 0.8845,
                 0.8642, 0.8440, 0.8237, 0.8035, 0.7832, 0.7939, 0.8046]

dict_death = \
{
   'BIN_EDGES':
           [    0.6,    29.5,    29.6,   359.5,   359.6,  1829.5,
             1829.6,  3659.5,  3659.6,  5489.5,  5489.6,  7289.5,
             7289.6,  9119.5,  9119.6, 10949.5, 10949.6, 12779.5,
            12779.6, 14609.5, 14609.6, 16439.5, 16439.6, 18239.5,
            18239.6, 20069.5, 20069.6, 21899.5, 21899.6, 23729.5,
            23729.6, 25559.5, 25559.6, 27389.5, 27389.6, 29189.5,
            29189.6, 31019.5, 31019.6, 32849.5, 32849.6, 34679.5,
            34679.6, 36509.5, 36509.6, 38339.5, 38339.6, 40139.5,
            40139.6, 41969.5, 41969.6, 43799.5, 43799.6, 43829.5],

   'EURO:UK':
           [4.950e-05, 4.950e-05, 4.950e-06, 4.950e-06, 9.900e-07, 9.900e-07,
            5.590e-08, 5.590e-08, 5.590e-08, 5.590e-08, 5.590e-08, 5.590e-08,
            5.590e-08, 5.590e-08, 5.590e-08, 5.590e-08, 6.820e-07, 6.820e-07,
            8.516e-07, 8.516e-07, 1.476e-06, 1.476e-06, 3.160e-06, 3.160e-06,
            7.796e-06, 7.796e-06, 2.098e-05, 2.098e-05, 6.027e-05, 6.027e-05,
            1.793e-04, 1.793e-04, 4.510e-05, 4.510e-05, 1.400e-04, 1.400e-04,
            4.380e-04, 4.380e-04, 1.370e-03, 1.370e-03, 4.280e-03, 4.280e-03,
            1.330e-02, 1.330e-02, 4.100e-02, 4.100e-02, 1.250e-01, 1.250e-01,
            1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00, 1.000e+00]
}

# *****************************************************************************


def demographicsBuilder():

    # Variables for this simulation
    MOD_AGE_INIT = gdata.var_params['modified_age_init']
    MORT_MULT01 = np.exp(gdata.var_params['log_mort_mult01'])
    MORT_MULT02 = np.exp(gdata.var_params['log_mort_mult02'])
    MORT_MULT03 = np.exp(gdata.var_params['log_mort_mult03'])

    gdata.init_pop = 100000

    # Populate nodes in primary file
    node_list = list()
    node_name = 'EURO:UK'
    node_obj = Node(lat=0.0, lon=0.0, pop=gdata.init_pop,
                    name=node_name, forced_id=1)
    node_list.append(node_obj)

    # Create primary file
    ref_name = 'Demographics_Example'
    demog_obj = Demographics(nodes=node_list, idref=ref_name)

    # Update defaults in primary file
    demog_obj.raw['Defaults']['IndividualAttributes'].clear()
    demog_obj.raw['Defaults']['NodeAttributes'].clear()

    # Vital dynamics
    birth_rate = br_base_val/1000.0/365.0
    mort_vec_X = dict_death['BIN_EDGES']
    mort_vec_Y = np.array(dict_death['EURO:UK'])
    mort_vec_Y[0:6] = mort_vec_Y[0:6]*MORT_MULT01
    mort_vec_Y[6:24] = mort_vec_Y[6:24]*MORT_MULT02
    mort_vec_Y[24:36] = mort_vec_Y[24:36]*MORT_MULT03
    mort_vec_Y = mort_vec_Y.tolist()
    forcing_vec = 12*[1.0]  # No seasonal forcing

    # Calculate equilibrium distribution
    (grow_rate, age_x, age_y) = DT._computeAgeDist(birth_rate, mort_vec_X,
                                                   mort_vec_Y, forcing_vec)

    if (MOD_AGE_INIT):
        age_x = np.cumsum(np.array(uk_1950_frac)).tolist()
        age_y = POP_AGE_DAYS

    DT.MortalityRateByAge(demog_obj, (np.array(mort_vec_X)/365.0).tolist(),
                          mort_vec_Y)

    iadict = dict()
    iadict['AgeDistribution'] = {'DistributionValues': [age_x],
                                 'ResultScaleFactor': 1,
                                 'ResultValues': [age_y]}

    demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)

    # Growth rate specifed is the long-term steady-state.
    nadict = dict()
    nadict['BirthRate'] = birth_rate
    nadict['GrowthRate'] = grow_rate   # Not used; included for reference

    demog_obj.raw['Defaults']['NodeAttributes'].update(nadict)

    # Write primary demographics file
    demog_obj.generate_file(name=DEMOG_FILE)

    # Save filename to global data for use in other functions
    gdata.demog_files.append(DEMOG_FILE)

    # Save the demographics object for use in other functions
    gdata.demog_object = demog_obj

    return None

# *****************************************************************************
