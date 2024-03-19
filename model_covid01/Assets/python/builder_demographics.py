# *****************************************************************************
#
# Demographics file and overlays.
#
# *****************************************************************************

import io
import json

import global_data as gdata

from aux_matrix_calc import mat_magic

import numpy as np

# *****************************************************************************

DEMOG_FILENAME = 'demographics.json'
ID_REFERENCE = 'covid-custom'

# *****************************************************************************


def demographicsBuilder():

    # Variables for this simulation
    CTEXT_VAL = gdata.var_params['ctext_val']
    TOTPOP = gdata.var_params['totpop']
    NUM_NODES = gdata.var_params['num_nodes']
    MRCOEFF = gdata.var_params['migration_coeff']
    FRAC_RURAL = gdata.var_params['frac_rural']
    POP_POW = gdata.var_params['pop_power']

    # Get HINT matrix
    pdict = {'arg_dist': [1.0, 1.0, 1.0, 1.0],
             'spike_mat': False, 'nudge_mat': False, 'hcw_h2h': False,
             'ctext_val': CTEXT_VAL}
    (age_pyr, age_names, mat_block) = mat_magic(pdict)

    # Dictionary of parameters to be written
    json_set = dict()

    # Add node list
    json_set['Nodes'] = list()

    # Generate node sizes
    nsizes = np.exp(-np.log(np.random.rand(NUM_NODES-1))/POP_POW)
    nsizes = FRAC_RURAL*nsizes/np.sum(nsizes)
    nsizes = np.minimum(nsizes, 100/TOTPOP)
    nsizes = FRAC_RURAL*nsizes/np.sum(nsizes)
    nsizes = np.insert(nsizes, 0, 1-FRAC_RURAL)
    npops = ((np.round(TOTPOP*nsizes, 0)).astype(int)).tolist()

    # Generate node lattice
    ucellb = np.array([[1.0, 0.0], [-0.5, 0.86603]])
    nlocs = np.random.rand(NUM_NODES, 2)
    nlocs[0, :] = 0.5
    nlocs = np.round(np.matmul(nlocs, ucellb), 4)

    # Add nodes to demographics
    for k1 in range(len(npops)):
        nodeDic = dict()
        nodeDic['NodeID'] = k1+1
        nodeDic['NodeAttributes'] = {'InitialPopulation': npops[k1],
                                     'Latitude': nlocs[k1, 1],
                                     'Longitude': nlocs[k1, 0]}
        json_set['Nodes'].append(nodeDic)

    # Create metadata dictionary
    json_set['Metadata'] = {'IdReference': ID_REFERENCE}

    # Create defaults dictionary
    json_set['Defaults'] = {'IndividualAttributes': dict(),
                            'IndividualProperties': list(),
                            'NodeAttributes': dict()}

    # Add default node attributes
    nadict = dict()

    nadict['InfectivityOverdispersion'] = 2.1

    json_set['Defaults']['NodeAttributes'].update(nadict)

    # Add default individual properties
    ipdict = dict()

    ipdict['Property'] = 'Geographic'
    ipdict['Values'] = age_names
    ipdict['Initial_Distribution'] = age_pyr.tolist()
    ipdict['Transitions'] = list()
    ipdict['TransmissionMatrix'] = {'Matrix': mat_block.tolist(),
                                    'Route': 'Contact'}

    json_set['Defaults']['IndividualProperties'].append(ipdict)

    # Write primary demographics file
    with open(gdata.demog_files[0], 'w') as fid01:
        json.dump(json_set, fid01, sort_keys=True)

    # Save filename to global data for use in other functions
    gdata.demog_files.append(DEMOG_FILENAME)

    # Save the demographics object for use in other functions
    gdata.demog_object = json_set

    # Write migration files
    num_dat = 30
    migJson = {'Metadata': {'IdReference': ID_REFERENCE,
                            'NodeCount': NUM_NODES,
                            'DatavalueCount': num_dat}}
    migJson['NodeOffsets'] = ''.join(['{:0>8s}{:0>8s}'.format(hex(k1+1)[2:],
                                     hex(k1*12*num_dat)[2:])
                                     for k1 in range(NUM_NODES)])

    with open('regional_migration.bin.json', 'w') as fid01:
        json.dump(migJson, fid01, sort_keys=True)

    # Calculate inter-node distances on periodic grid
    nlocs = np.tile(nlocs, (9, 1))
    nlocs[0*NUM_NODES:1*NUM_NODES, :] += [0.0, 0.0]
    nlocs[1*NUM_NODES:2*NUM_NODES, :] += [1.0, 0.0]
    nlocs[2*NUM_NODES:3*NUM_NODES, :] += [-1.0, 0.0]
    nlocs[3*NUM_NODES:4*NUM_NODES, :] += [0.0, 0.0]
    nlocs[4*NUM_NODES:5*NUM_NODES, :] += [1.0, 0.0]
    nlocs[5*NUM_NODES:6*NUM_NODES, :] += [-1.0, 0.0]
    nlocs[6*NUM_NODES:7*NUM_NODES, :] += [0.0, 0.0]
    nlocs[7*NUM_NODES:8*NUM_NODES, :] += [1.0, 0.0]
    nlocs[8*NUM_NODES:9*NUM_NODES, :] += [-1.0, 0.0]

    nlocs[0*NUM_NODES:1*NUM_NODES, :] += [0.0, 0.0]
    nlocs[1*NUM_NODES:2*NUM_NODES, :] += [0.0, 0.0]
    nlocs[2*NUM_NODES:3*NUM_NODES, :] += [0.0, 0.0]
    nlocs[3*NUM_NODES:4*NUM_NODES, :] += [-0.5, 0.86603]
    nlocs[4*NUM_NODES:5*NUM_NODES, :] += [-0.5, 0.86603]
    nlocs[5*NUM_NODES:6*NUM_NODES, :] += [-0.5, 0.86603]
    nlocs[6*NUM_NODES:7*NUM_NODES, :] += [0.5, -0.86603]
    nlocs[7*NUM_NODES:8*NUM_NODES, :] += [0.5, -0.86603]
    nlocs[8*NUM_NODES:9*NUM_NODES, :] += [0.5, -0.86603]

    distgrid = np.zeros((nlocs.shape[0], nlocs.shape[0]))

    for k1 in range(nlocs.shape[0]):
        delt_vec = np.sqrt(np.sum(np.square(nlocs - nlocs[k1, :]), axis=1))
        distgrid[k1, :] = delt_vec

    nborlist = np.argsort(distgrid, axis=1)

    outbytes = io.BytesIO()
    for k1 in range(NUM_NODES):
        for k2 in range(1, num_dat+1):
            if (distgrid.shape[0] > k2):
                tnode = int(np.mod(nborlist[k1, k2], NUM_NODES))+1
            else:
                tnode = 0
            outbytes.write(tnode.to_bytes(4, byteorder='little'))

        for k2 in range(1, num_dat+1):
            if (distgrid.shape[0] > k2):
                idnode = nborlist[k1, k2]
                tnode = int(np.mod(nborlist[k1, k2], NUM_NODES))
                dnom = np.sum(npops)*distgrid[k1, idnode]
                migrat = MRCOEFF*npops[tnode]/dnom
                val = np.array([migrat], dtype=np.float64)
            else:
                val = np.array([0.0], dtype=np.float64)

            outbytes.write(val.tobytes())

    with open('regional_migration.bin', 'wb') as fid01:
        fid01.write(outbytes.getvalue())

    return None

# *****************************************************************************
