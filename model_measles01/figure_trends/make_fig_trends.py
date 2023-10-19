#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt
import matplotlib.patches  as patch
import matplotlib          as mpl

from global_data           import run_years
from dtk_post_process      import AGE_HIST_BINS

#*******************************************************************************


DIRNAMES = {'experiment_popL1':      'Late',
            'experiment_popL1_MCV2': 'Late',
            'experiment_popL2':      'Mid',
            'experiment_popL2_MCV2': 'Mid',
            'experiment_popL3':      'Early',
            'experiment_popL3_MCV2': 'Early'}


for dirname in DIRNAMES:

  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  inf_dat      = np.zeros((nsims,12*int(run_years)))
  age_dat      = np.zeros((nsims,   int(run_years)  ,15))
  pyr_mat      = np.zeros((nsims,   int(run_years)+1,20))-1

  if('MCV1' in param_dict['EXP_VARIABLE']):
    mcv1_vec   = np.array(param_dict['EXP_VARIABLE']['MCV1'])
  else:
    mcv1_vec   = np.ones(nsims)*param_dict['EXP_CONSTANT']['MCV1']
  mcv1_lvl = np.unique(mcv1_vec)

  if('MCV1_age' in param_dict['EXP_VARIABLE']):
    mcv1_age_vec = np.array(param_dict['EXP_VARIABLE']['MCV1_age'])
  else:
    mcv1_age_vec = np.ones(nsims)*param_dict['EXP_CONSTANT']['MCV1_age']
  mcv1_age_lvl = np.unique(mcv1_age_vec)

  if('MCV2' in param_dict['EXP_VARIABLE']):
    mcv2_vec   = np.array(param_dict['EXP_VARIABLE']['MCV2'])
  else:
    mcv2_vec   = np.ones(nsims)*param_dict['EXP_CONSTANT']['MCV2']
  mcv2_lvl = np.unique(mcv2_vec)

  if('mat_factor' in param_dict['EXP_VARIABLE']):
    mat_fac_vec = np.array(param_dict['EXP_VARIABLE']['mat_factor'])
  else:
    mat_fac_vec = np.ones(nsims)*param_dict['EXP_CONSTANT']['mat_factor']
  mat_fac_lvl = np.unique(mat_fac_vec)

  for sim_idx_str in data_brick:
    if(not sim_idx_str.isdigit()):
      continue

    sim_idx = int(sim_idx_str)
    inf_dat[sim_idx,:]  = np.array(data_brick[sim_idx_str]['timeseries'])
    age_dat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['age_data'])
    pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])

  fidx = (pyr_mat[:,0,0]>=0)

  pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
  tpop_avg    = np.sum(pyr_mat_avg, axis=1)
  tpop_xval   = np.arange(len(tpop_avg))

  xval        = np.arange(0,run_years,1/12) + 1/24
  pops        = np.interp(xval, tpop_xval, tpop_avg)
  inf_dat_nrm = inf_dat[fidx,:]/pops*1e5

  inf_yrs     = np.zeros((nsims,int(run_years)))
  inf_yrs_nrm = np.zeros((nsims,int(run_years)))
  for k1 in range(int(run_years)):
    inf_yrs[:,k1]     = np.sum(inf_dat[:,(k1*12):((k1+1)*12)],axis=1)
    inf_yrs_nrm[:,k1] = np.mean(inf_dat_nrm[:,(k1*12):((k1+1)*12)],axis=1)


  # Figures
  fig01 = plt.figure(figsize=(8,6))

  # Figures - Sims - Infections
  axs01 = fig01.add_subplot(1, 1, 1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  k1 = 0
  for mcv1_age_val in mcv1_age_lvl:
    for mat_fac_val in mat_fac_lvl:
      idx01 = (mat_fac_vec  == mat_fac_val)
      idx02 = (mcv1_age_vec == mcv1_age_val)
      tidx  = (fidx & idx01 & idx02)
      xval  = mcv1_vec[tidx]
      xval2 = np.arange(0.2,1.001,0.01)
      yval  = np.mean(inf_yrs_nrm[tidx,-10:],axis=1)
      pcoef = np.polyfit(xval,yval,4)
      yval2 = np.polyval(pcoef,xval2)
      if(mat_fac_val == 1):
        lfmt = '-'
      else:
        lfmt = '--'
      axs01.plot(xval,  yval,  '.',  alpha=0.1, color='C{:d}'.format(k1),
                                     markeredgecolor=None)
      axs01.plot(xval2, yval2, lfmt, alpha=1.0, color='C{:d}'.format(k1))

    txt_age = int(np.round(mcv1_age_val/365*12))
    axs01.text( 0.23, 54-15*k1, 'MCV1 {:>2d}mo'.format(txt_age), fontsize=14,
                                color='C{:d}'.format(k1))
    if(mcv2_lvl[0] > 0):
      axs01.text( 0.37, 54-15*k1, '+ MCV2 15mo', fontsize=14,
                                  color='C{:d}'.format(k1))

    k1 = k1 + 1



  axs01.set_ylabel('Monthly Incidence per-100k',fontsize=16)
  axs01.set_xlabel('MCV Coverage',fontsize=16)
  axs01.set_ylim(  0, 300)
  axs01.set_xlim(0.2, 1.0)
  axs01.text( 0.71, 270, 'Demog: {:s}'.format(DIRNAMES[dirname]), fontsize=18)
  axs01.text( 0.76, 253, '100% Maternal', fontsize=14)
  axs01.plot([0.71, 0.75], [257,257], 'k-')
  axs01.text( 0.76, 238, '50%  Maternal', fontsize=14)
  axs01.plot([0.71, 0.75], [242,242], 'k--')

  plt.tight_layout()
  plt.savefig('fig_trends_{:s}_01.png'.format(dirname))
  plt.close()


#*******************************************************************************
