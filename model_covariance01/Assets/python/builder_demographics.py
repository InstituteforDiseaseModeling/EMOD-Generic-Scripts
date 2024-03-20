# *****************************************************************************
#
# Demographics file and overlays.
#
# *****************************************************************************

import global_data as gdata

from emod_api.demographics.Demographics import Demographics, Node

# *****************************************************************************

DEMOG_FILENAME = 'demographics.json'

# *****************************************************************************


def demographicsBuilder():

    # Variables for this simulation
    IND_RISK_VAR = gdata.var_params['indiv_variance_acq']

    # Populate nodes in primary file
    node_list = list()
    node_obj = Node(lat=0.0, lon=0.0, pop=100000,
                    name='CATAN:001', forced_id=1)
    node_list.append(node_obj)

    # Create primary file
    ref_name = 'Example_Covariance_Sims'
    demog_obj = Demographics(nodes=node_list, idref=ref_name)

    # Update defaults in primary file
    demog_obj.raw['Defaults']['IndividualAttributes'].clear()
    demog_obj.raw['Defaults']['NodeAttributes'].clear()

    iadict = dict()
    iadict['AcquisitionHeterogeneityVariance'] = IND_RISK_VAR
    demog_obj.raw['Defaults']['IndividualAttributes'].update(iadict)

    # Write primary demographics file
    demog_obj.generate_file(name=DEMOG_FILENAME)

    # Save filename to global data for use in other functions
    gdata.demog_files.append(DEMOG_FILENAME)

    # Save the demographics object for use in other functions
    gdata.demog_object = demog_obj

    return None

# *****************************************************************************
