#********************************************************************************
#
# Builds a demographics.json file to be used as input to the DTK.
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json, io

from aux_matrix_calc import mat_magic
from aux_dist_calc   import pair_dist_mat

ext_py_path = os.path.join('Assets','site-packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy                    as    np

#********************************************************************************

def demographicsBuilder(params=dict()):

  # Get HINT matrix
  pdict = {'arg_dist':            [1.0,1.0,1.0,1.0] ,
           'spike_mat':                       False ,
           'nudge_mat':                       False ,
           'hcw_h2h':                         False ,
           'ctext_val':         params['ctext_val'] }
  (age_pyr, age_names, mat_block) = mat_magic(pdict)


  # *****  Dictionary of parameters to be written ***** 

  json_set = dict()



  # ***** Detailed node attributes *****

  # Add node list
  json_set['Nodes'] = list()

  # Generate nodes
  totpop     = params['totpop']
  num_nodes  = params['num_nodes']
  mrcoeff    = params['migration_coeff']
  frac_rural = params['frac_rural']
  pop_pow    = params['pop_power']

  # Generate node sizes
  nsizes     = np.exp(-np.log(np.random.rand(num_nodes-1))/pop_pow)
  nsizes     = frac_rural*nsizes/np.sum(nsizes)
  nsizes     = np.minimum(nsizes,100/totpop)
  nsizes     = frac_rural*nsizes/np.sum(nsizes)
  nsizes     = np.insert(nsizes,0,1-frac_rural)
  npops      = ((np.round(totpop*nsizes,0)).astype(int)).tolist()

  # Generate node lattice
  ucellb     = np.array([[1.0,0.0],[-0.5,0.86603]])
  nlocs      = np.random.rand(num_nodes,2)
  nlocs[0,:] = 0.5
  nlocs      = np.round(np.matmul(nlocs,ucellb),4)

  # Add nodes to demographics
  for k1 in range(len(npops)):
    nodeDic   = dict()    
    nodeDic['NodeID']         =   k1+1
    nodeDic['NodeAttributes'] = {'InitialPopulation':    npops[k1] ,
                                 'Latitude':           nlocs[k1,1] ,
                                 'Longitude':          nlocs[k1,0] }
    json_set['Nodes'].append(nodeDic)



  # ***** Metadata and default attributes *****
  
  # Create metadata dictionary
  json_set['Metadata'] = { 'IdReference':   'covid-custom' }

  # Create defaults dictionary
  json_set['Defaults'] = { 'IndividualAttributes': dict()  ,
                           'IndividualProperties': list()  ,
                           'NodeAttributes':       dict()  }


  
  # Add default node attributes
  nadict = dict()


  nadict['BirthRate']                   =   0.0
  nadict['InfectivityOverdispersion']   =   2.1
  nadict['Airport']                     =   0
  nadict['Region']                      =   1  
  nadict['Seaport']                     =   0 

  json_set['Defaults']['NodeAttributes'].update(nadict)


  # Add default individual properties
  ipdict = dict()

  ipdict['Property']              = 'Geographic'
  ipdict['Values']                = age_names
  ipdict['Initial_Distribution']  = age_pyr.tolist()
  ipdict['Transitions']           = list()
  ipdict['TransmissionMatrix']    = {'Matrix': mat_block.tolist(),
                                     'Route':           'Contact'}

  json_set['Defaults']['IndividualProperties'].append(ipdict)



  # ***** Write demographics files ***** 
  with open('demographics.json','w')  as fid01:
    json.dump(json_set,fid01,sort_keys=True)



  # ***** Write migration files *****
  migJson = {'Metadata': { 'IdReference':   'covid-custom' ,
                           'NodeCount':          num_nodes ,
                           'DatavalueCount':            30 } }
  migJson['NodeOffsets'] = ''.join(['{:08d}{:0>8s}'.format(k1,hex(k1*360)[2:])
                                                  for k1 in range(num_nodes)])
  
  with open('regional_migration.bin.json','w') as fid01:
    json.dump(migJson,fid01,sort_keys=True)


  # Calculate inter-node distances on periodic grid
  nlocs    = np.tile(nlocs,(9,1))
  nlocs[0*num_nodes:1*num_nodes,:] += [ 0.0, 0.0]
  nlocs[1*num_nodes:2*num_nodes,:] += [ 1.0, 0.0]
  nlocs[2*num_nodes:3*num_nodes,:] += [-1.0, 0.0]
  nlocs[3*num_nodes:4*num_nodes,:] += [ 0.0, 0.0]
  nlocs[4*num_nodes:5*num_nodes,:] += [ 1.0, 0.0]
  nlocs[5*num_nodes:6*num_nodes,:] += [-1.0, 0.0]
  nlocs[6*num_nodes:7*num_nodes,:] += [ 0.0, 0.0]
  nlocs[7*num_nodes:8*num_nodes,:] += [ 1.0, 0.0]
  nlocs[8*num_nodes:9*num_nodes,:] += [-1.0, 0.0]
  nlocs[0*num_nodes:1*num_nodes,:] += [ 0.0, 0.0]
  nlocs[1*num_nodes:2*num_nodes,:] += [ 0.0, 0.0]
  nlocs[2*num_nodes:3*num_nodes,:] += [ 0.0, 0.0]
  nlocs[3*num_nodes:4*num_nodes,:] += [-0.5, 0.86603]
  nlocs[4*num_nodes:5*num_nodes,:] += [-0.5, 0.86603]
  nlocs[5*num_nodes:6*num_nodes,:] += [-0.5, 0.86603]
  nlocs[6*num_nodes:7*num_nodes,:] += [ 0.5,-0.86603]
  nlocs[7*num_nodes:8*num_nodes,:] += [ 0.5,-0.86603]
  nlocs[8*num_nodes:9*num_nodes,:] += [ 0.5,-0.86603]
  distgrid = pair_dist_mat(nlocs)
  nborlist = np.argsort(distgrid,axis=1)

  outbytes = io.BytesIO()
  for k1 in range(num_nodes):
    for k2 in range(1,31):
      if(distgrid.shape[0] > k2):
        tnode = int(np.mod(nborlist[k1,k2],num_nodes))+1
      else:
        tnode = 0
      #end-if
      outbytes.write(tnode.to_bytes(4,byteorder='little'))
    #end-k2
    for k2 in range(1,31):
      if(distgrid.shape[0] > k2):
        idnode = nborlist[k1,k2]
        tnode  = int(np.mod(nborlist[k1,k2],num_nodes))
        migrat = mrcoeff*npops[tnode]/np.sum(npops)/distgrid[k1,idnode]
        val    = np.array([migrat],dtype=np.float64)
      else:
        val = np.array([0.0],dtype=np.float64)
      #end-if
      outbytes.write(val.tobytes())
    #end-k2
  #end-k1
  with open('regional_migration.bin','wb') as fid01:
    fid01.write(outbytes.getvalue())

  return None

#*******************************************************************************
