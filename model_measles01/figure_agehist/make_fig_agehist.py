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


DIRNAMES = ['experiment_popL1',
            'experiment_popL2',
            'experiment_popL3']


for dirname in DIRNAMES:

  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  inf_dat      = np.zeros((nsims,12*int(run_years)))
  age_dat      = np.zeros((nsims,   int(run_years)  ,len(AGE_HIST_BINS)-1))
  pyr_mat      = np.zeros((nsims,   int(run_years)+1,20))-1


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

  bin_wid       = np.diff(AGE_HIST_BINS)
  bin_loc       = AGE_HIST_BINS[:-1] + bin_wid/2
  age_frac      = age_dat/(inf_yrs[:,:,np.newaxis]+np.finfo(float).eps)
  age_frac_mean = np.mean(age_frac, axis=0)
  age_frac_std  = np.std(age_frac, axis=0)


  # Figures
  fig01 = plt.figure(figsize=(16,6))

  # Figures - Sims - Infections
  axs01 = fig01.add_subplot(1, 2, 1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  bin_hgt = age_frac_mean[-1-10,:]/bin_wid
  bin_std = age_frac_std[-1-10,:]/bin_wid
  axs01.bar(bin_loc, bin_hgt, width=bin_wid, edgecolor='k', yerr=bin_std)

  axs01.set_ylabel('Fraction',fontsize=16)
  axs01.set_xlabel('Age at Infection (yrs)',fontsize=16)
  axs01.set_ylim( 0.0, 0.65)
  axs01.set_xlim(min(AGE_HIST_BINS), max(AGE_HIST_BINS))
  axs01.text( 8.3, 0.55, 'Year {:d}'.format(int(run_years)-10), fontsize=18)

  axs01 = fig01.add_subplot(1, 2, 2)
  plt.sca(axs01)
  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  bin_hgt = age_frac_mean[-1,:]/bin_wid
  bin_std = age_frac_std[-1,:]/bin_wid
  axs01.bar(bin_loc, bin_hgt, width=bin_wid, edgecolor='k', yerr=bin_std)

  axs01.set_xlabel('Age at Infection (yrs)',fontsize=16)
  axs01.set_ylim( 0.0, 0.65)
  axs01.set_xlim(min(AGE_HIST_BINS), max(AGE_HIST_BINS))
  axs01.text( 8.3, 0.55, 'Year {:d}'.format(int(run_years)), fontsize=18)



  plt.tight_layout()
  plt.savefig('fig_agehist_{:s}_01.png'.format(dirname))
  plt.close()


#*******************************************************************************
