#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from global_data          import start_year    as INIT_YR
from global_data          import run_years     as NUM_YRS

#*******************************************************************************

# Years simulated
XDAT     = np.arange(INIT_YR, INIT_YR+int(NUM_YRS)) + 0.5

# Load UN WPP fertility distribution data
fname    = os.path.join('..','Assets','data','fert_dat_SSA.csv')
fert_dat = np.loadtxt(fname,delimiter=',')
fert_yr  = fert_dat[0, :]
fert_mat = fert_dat[1:,:]

# Fertility distributions interpolated for years simulated
fert_set = np.zeros((fert_mat.shape[0],XDAT.shape[0]))
for k1 in range(fert_set.shape[0]):
  fert_set[k1,:] = np.interp(XDAT, fert_yr, fert_mat[k1,:])
fert_set = fert_set/1000.0 # births/woman/year

#*******************************************************************************


DIRNAMES = ['experiment_working01',
            'experiment_working02']


for dirname in DIRNAMES:
  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  ss_demog     =     param_dict['EXP_CONSTANT']['steady_state_demog']

  pyr_mat      = np.zeros((nsims,int(NUM_YRS+1),20))-1
  inf_mat      = np.zeros((nsims,int(NUM_YRS),  20))
  birth_mat    = np.zeros((nsims,int(NUM_YRS)     ))

  for sim_idx_str in data_brick:
    sim_idx = int(sim_idx_str)
    pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])
    inf_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['inf_data'])
    birth_mat[sim_idx,:] = np.array(data_brick[sim_idx_str]['cbr_vec'])

  # Index for simulations with output
  fidx = (pyr_mat[:,0,0]>=0)

  # Annual crude births simulated in model
  pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
  pop_tot     = np.sum(pyr_mat_avg,axis=1)
  pop_tot     = np.diff(pop_tot)/2.0 + pop_tot[:-1]
  birth_vec   = np.mean(birth_mat[fidx,:], axis=0)

  # Annual births implied by fertility distribution
  tot_fem = np.transpose((np.diff(pyr_mat_avg,axis=0)/2.0 + pyr_mat_avg[:-1,:])/2.0)
  fertopt = fert_set
  if(ss_demog):
    fertopt = fert_set[:,0]
    fertopt = fertopt[:,np.newaxis]
  fert_births = np.sum(fertopt*tot_fem,axis=0)

  # Normalize timeseries required for CRS calculation
  norm_crs_timevec = birth_vec/fert_births

  # Calculate CRS probabilities
  crs_prob_vec  = np.ones(fertopt.shape)     # P = 1
  crs_prob_vec  = crs_prob_vec * 0.5         # P(female)
  crs_prob_vec  = crs_prob_vec * fertopt     # P(gave birth during year)
  crs_prob_vec  = crs_prob_vec * 9.0/12.0    # P(pregnant during year)
  crs_prob_vec  = crs_prob_vec * (0.85*13/39 + 0.50*13/39 + 0.50*4/39)
                                             # P(infection leads to CRS)


  # Figures
  fig01 = plt.figure(figsize=(16,6))


  # Figures - Sims - Infections
  axs01 = fig01.add_subplot(1, 2, 1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_xlabel('Year', fontsize=14)
  axs01.set_ylabel('Total Infections per 100k', fontsize=14)

  axs01.set_xlim(2020, 2050)
  axs01.set_ylim(   0, 6000)

  inf_mat_avg = np.mean(inf_mat[fidx,:,:],axis=0)
  ydat        = np.sum(inf_mat_avg,axis=1)/pop_tot*1e5

  axs01.plot(XDAT,ydat)


  # Figures - Sims - CRS
  axs01 = fig01.add_subplot(1, 2, 2)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_xlabel('Year', fontsize=14)
  axs01.set_ylabel('CRS Burden per 1k Births', fontsize=14)

  axs01.set_xlim(2020, 2050)
  axs01.set_ylim( 0.0,  6.0)

  inf_mat_avg = np.mean(inf_mat[fidx,:,:],axis=0)
  crs_mat     = inf_mat_avg*np.transpose(crs_prob_vec)
  ydat        = np.sum(crs_mat,axis=1)/birth_vec*norm_crs_timevec*1e3

  axs01.plot(XDAT,ydat)


  plt.tight_layout()
  plt.savefig('fig_pyr_{:s}.png'.format(dirname))
  plt.close()


#*******************************************************************************
