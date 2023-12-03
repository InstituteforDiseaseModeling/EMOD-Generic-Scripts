#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt
import matplotlib.patches  as patch
import matplotlib          as mpl

from global_data           import run_years
from dtk_post_process      import AGE_HIST_BINS, IHME_MORT_X, IHME_MORT_Y

#*******************************************************************************


DIRNAMES = ['experiment_popL1',
            'experiment_popL1_MCV2',
            'experiment_popL2',
            'experiment_popL2_SIA6MO',
            'experiment_popL2_SIA9MO',
            'experiment_popL2_SIA9MO80p',
            'experiment_popL2_MCV2',
            'experiment_popL3',
            'experiment_popL3_MCV2']


for dirname in DIRNAMES:

  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  ref_year     = param_dict['EXP_CONSTANT']['start_year']
  inf_dat      = np.zeros((nsims,12*int(run_years)))
  age_dat      = np.zeros((nsims,   int(run_years)  ,len(AGE_HIST_BINS)-1))
  mort_dat     = np.zeros((nsims,   int(run_years)))
  pyr_mat      = np.zeros((nsims,   int(run_years)+1,20))-1

  mcv1_vec     = np.array(param_dict['EXP_VARIABLE']['MCV1'])
  mcv1_lvl     = np.unique(mcv1_vec)

  mcv1_age_vec = np.array(param_dict['EXP_VARIABLE']['MCV1_age'])
  mcv1_age_lvl = np.unique(mcv1_age_vec)

  mcv2_vec     = np.ones(nsims)*param_dict['EXP_CONSTANT']['MCV2']
  mcv2_lvl     = np.unique(mcv2_vec)

  xval         = np.arange(0,run_years,1/12) + 1/24
  xyrs         = np.arange(0,run_years,1)    + 1/2
  xages        = AGE_HIST_BINS[1:] + np.diff(AGE_HIST_BINS)/2
  mort_prob    = np.interp(xages, IHME_MORT_X, IHME_MORT_Y)

  for sim_idx_str in data_brick:
    if(not sim_idx_str.isdigit()):
      continue

    sim_idx = int(sim_idx_str)
    inf_dat[sim_idx,:]   = np.array(data_brick[sim_idx_str]['timeseries'])
    age_dat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['age_data'])
    pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])
    mort_dat[sim_idx,:]  = np.sum(age_dat[sim_idx,:,:]*mort_prob, axis=1)


  fidx = (pyr_mat[:,0,0]>=0)

  pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
  tpop_avg    = np.sum(pyr_mat_avg, axis=1)
  tpop_xval   = np.arange(len(tpop_avg))
  pops        = np.interp(xyrs, tpop_xval, tpop_avg)
  mort_nrm    = mort_dat[fidx,:]/pops*1e5


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
    if(mcv1_age_val > 300):
      continue

    idx02 = (mcv1_age_vec == mcv1_age_val)
    tidx  = (fidx & idx02)
    xval  = mcv1_vec[tidx]
    xval2 = np.arange(0.2,1.001,0.01)
    yval  = np.mean(mort_nrm[tidx,-10:],axis=1)/12.0
    pcoef = np.polyfit(xval,yval,4)
    yval2 = np.polyval(pcoef,xval2)

    #axs01.scatter(xval, yval, c=yval, vmin=20, vmax=180)
    axs01.plot(xval,  yval,  '.',  alpha=0.1, color='C{:d}'.format(k1),
                                   markeredgecolor=None)
    axs01.plot(xval2, yval2, '-', alpha=1.0, color='C{:d}'.format(k1))

    txt_age = int(np.round(mcv1_age_val/365*12))
    axs01.text( 0.56, 3.76-0.24*k1, 'MCV1 {:>2d}mo'.format(txt_age), fontsize=18,
                                color='C{:d}'.format(k1))
    if(mcv2_lvl[0] > 0):
      axs01.text( 0.74, 3.76-0.24*k1, '+ MCV2 15mo', fontsize=18,
                                  color='C{:d}'.format(k1))

    k1 = k1 + 1


  if(ref_year == 2020):
    demogname = 'Demog: Early'
  elif(ref_year == 2040):
    demogname = 'Demog: Mid'
  elif(ref_year == 2060):
    demogname = 'Demog: Late'

  axs01.set_ylabel('Monthly Mortality per-100k',fontsize=16)
  axs01.set_xlabel('MCV Coverage',fontsize=16)
  axs01.set_ylim(  0, 4.0)
  axs01.set_xlim(0.2, 1.0)
  #axs01.text( 0.71, 270, demogname, fontsize=18)
  axs01.tick_params(axis='both', which='major', labelsize=14)

  plt.tight_layout()
  plt.savefig('fig_trends_{:s}_01.png'.format(dirname))
  plt.close()


#*******************************************************************************
