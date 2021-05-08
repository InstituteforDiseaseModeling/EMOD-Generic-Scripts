#********************************************************************************
#
# HINT matrix construction
#
# Python 3.6.0
#
#********************************************************************************

import os, sys

from refdat_age_pyr       import age_pyr_fun
from refdat_contact_mat   import contact_mat_fun
from refdat_hcw_stats     import hcw_stats_fun

ext_py_path = os.path.join('Assets','site-packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy as np

#********************************************************************************

def mat_magic(params=dict()):

  spike_mat = params['spike_mat']
  nudge_mat = params['nudge_mat']
  hcw_h2h   = params['hcw_h2h']
  arg_dist  = params['arg_dist']  
  ctext_val = params['ctext_val'] 

  # Fraction reduced work/school contacts to transfer to home
  home_acc = 0.2

  # HCW work contact multiplier
  HCW_work_mult = 20

  # HCW asymmetry multiplier
  HCW_asym_mult = 5.0/3.0

  # Distribution of R0 (must be normalized)
  #R0x = [   0.35,    0.50,        0.15] # Old style  
  #R0y = [ 1.0,     1.0,         1.0   ]
  R0x = [   0.35,    0.50,        0.15] # New style
  R0y = [3.0/5.0,     1.0,   29.0/15.0]

  # Age pyramid
  (age_rng, age_pyr) = age_pyr_fun(ctext_val)

  # Unscaled contact matrices
  (mat_home, mat_work, mat_schl, mat_comm) = contact_mat_fun(ctext_val)

  # HCW stats
  (age_pyr_hcw, tot_frk_hcw, wrk_cts_hcw)= hcw_stats_fun(ctext_val)

  # Increase contacts
  if(hcw_h2h):
    wrk_cts_hcw = \
       [0.80,0.00,0.00,0.00,0.05,0.05,0.05,0.05,
        0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]

  # Linear algebra, the best kind of algebra
  age_pyr      = np.array(age_pyr)
  age_pyr_hcw  = np.array(age_pyr_hcw)
  wrk_cts_hcw  = np.array(wrk_cts_hcw)

  mat_home = np.array(mat_home)
  mat_work = np.array(mat_work)
  mat_schl = np.array(mat_schl)
  mat_comm = np.array(mat_comm)

  # HCW - standard contacts based on age distribution; school route excluded
  col_home_hcw = np.dot(age_pyr_hcw, mat_home)/np.sum(age_pyr_hcw)  
  col_work_hcw = np.dot(age_pyr_hcw, mat_work)/np.sum(age_pyr_hcw) 
  col_comm_hcw = np.dot(age_pyr_hcw, mat_comm)/np.sum(age_pyr_hcw)  

  # HCW - redistribute HCW work contacts according to reference
  col_work_hcw = HCW_work_mult*np.sum(col_work_hcw)*wrk_cts_hcw

  # HCW - column total
  col_totl_hcw = col_home_hcw + col_work_hcw + col_comm_hcw

  # HCW - self-interaction coefficient (diagonal); school route excluded
  mat_ref      = mat_home + mat_work + mat_comm
  dia_totl_hcw = np.dot(np.diag(mat_ref), age_pyr_hcw)/np.sum(age_pyr_hcw)

  # HCW - row total
  row_totl_hcw = HCW_asym_mult*col_totl_hcw

  # Adjust and normalize age pyramid for HCW
  age_pyr       = age_pyr/np.sum(age_pyr)-tot_frk_hcw*age_pyr_hcw/np.sum(age_pyr_hcw)

  # Calculate R0 normalization value
  age_pyr_pH = np.append(age_pyr, tot_frk_hcw)
  mat_ref    = mat_home + mat_work + mat_schl + mat_comm
  mat_ref_pH = np.hstack((mat_ref,col_totl_hcw[:,np.newaxis]))
  mat_ref_pH = np.vstack((mat_ref_pH,np.append(row_totl_hcw,dia_totl_hcw)))
  R0_ref     = np.dot(np.dot(age_pyr_pH, mat_ref_pH), age_pyr_pH)

  # Calculate HINT matrix with distancing  
  mat_tot  = arg_dist[0]*mat_home + arg_dist[1]*mat_schl + \
             arg_dist[2]*mat_work + arg_dist[3]*mat_comm

  # Move fraction from school to home and fraction from work to home
  add_fac    = home_acc*(1-arg_dist[1])
  home_mag   = add_fac*np.dot(age_pyr,mat_schl)/np.dot(age_pyr,mat_home)
  mat_add1   = np.matmul(mat_home,np.diag(home_mag))

  add_fac    = home_acc*(1-arg_dist[2])
  home_mag   = add_fac*np.dot(age_pyr,mat_work)/np.dot(age_pyr,mat_home)
  mat_add2   = np.matmul(mat_home,np.diag(home_mag))

  mat_tot    = mat_tot + mat_add1 + mat_add2

  # Increase contacts
  if(spike_mat):
    mat_tot[:7,:7] = mat_tot[:7,:7]*np.array([[1.50,1.00,1.00,1.00,3.00,3.00,3.00],
                                              [1.00,1.00,1.00,1.00,1.00,1.00,1.00],
                                              [1.00,1.00,1.00,1.00,1.00,1.00,1.00],
                                              [1.00,1.00,1.00,1.00,1.00,1.00,1.00],
                                              [3.00,1.00,1.00,1.00,1.50,1.50,1.50],
                                              [3.00,1.00,1.00,1.00,1.50,1.50,1.50],
                                              [3.00,1.00,1.00,1.00,1.50,1.50,1.50]])

  if(nudge_mat):
    mat_tot[:7,:7] = mat_tot[:7,:7]*np.array([[1.05,1.00,1.00,1.00,1.20,1.20,1.20],
                                              [1.00,1.00,1.00,1.00,1.00,1.00,1.00],
                                              [1.00,1.00,1.00,1.00,1.00,1.00,1.00],
                                              [1.00,1.00,1.00,1.00,1.00,1.00,1.00],
                                              [1.20,1.00,1.00,1.00,1.05,1.05,1.05],
                                              [1.20,1.00,1.00,1.00,1.05,1.05,1.05],
                                              [1.20,1.00,1.00,1.00,1.05,1.05,1.05]])
  # Category labels
  names_big = list()
  names_big.extend(['age{:02d}_riskLO'.format(k1) for k1 in age_rng])
  names_big.extend(['age{:02d}_riskMD'.format(k1) for k1 in age_rng])
  names_big.extend(['age{:02d}_riskHI'.format(k1) for k1 in age_rng])
  names_big.append('HCW')

  # Category fractions
  age_big = np.hstack((R0x[0]*age_pyr,  R0x[1]*age_pyr,  R0x[2]*age_pyr))
  age_big = np.append(age_big,tot_frk_hcw)

  # Tile matrix
  mat_tall = np.tile(mat_tot,(3,1))
  mat_big  = np.hstack((R0y[0]*mat_tall, R0y[1]*mat_tall, R0y[2]*mat_tall))
  mat_big  = np.hstack((mat_big,np.tile(col_totl_hcw[:,np.newaxis],(3,1))))
  nrowval  = np.append(np.tile(row_totl_hcw,(1,3)),dia_totl_hcw)
  mat_big  = np.vstack((mat_big,nrowval))/R0_ref

  # Diagnostics
  #print(np.dot(np.dot(age_big,mat_big),age_big))

  #debug_v1 = np.dot(np.dot(age_pyr,mat_home),age_pyr)
  #debug_v2 = np.dot(np.dot(age_pyr,mat_work),age_pyr)
  #debug_v3 = np.dot(np.dot(age_pyr,mat_schl),age_pyr)
  #debug_v4 = np.dot(np.dot(age_pyr,mat_comm),age_pyr)
  #debug_vt = debug_v1 + debug_v2 + debug_v3 + debug_v4
  #print('Home: {:5.3f}'.format(debug_v1/debug_vt))
  #print('Work: {:5.3f}'.format(debug_v2/debug_vt))
  #print('Schl: {:5.3f}'.format(debug_v3/debug_vt))
  #print('Comm: {:5.3f}'.format(debug_v4/debug_vt))

  return(age_big, names_big, mat_big)

#********************************************************************************
#params = dict()
#params['spike_mat'] = False
#params['nudge_mat'] = False
#params['hcw_h2h']   = False
#params['arg_dist']  = [1.0,1.0,1.0,1.0]
#params['ctext_val'] = 'AFRO:ANG'#'WPRO:LAO'#'SEARO:NPL'#'EURO:UKR'#'PAHO:ECU'#'EMRO:PAK'
#mat_magic(params)
