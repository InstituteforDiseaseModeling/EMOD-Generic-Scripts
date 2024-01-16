#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from global_data          import start_year, run_years

#*******************************************************************************

# Years simulated
XDAT     = np.arange(start_year, start_year+int(run_years)) + 0.5

# Load UN WPP fertility distribution data
fname    = os.path.join('..','Assets','data','fert_dat_COD.csv')
fert_dat = np.loadtxt(fname,delimiter=',')
fert_yr  = fert_dat[0, :]
fert_mat = fert_dat[1:,:]

# Fertility distributions interpolated for years simulated
fert_set = np.zeros((fert_mat.shape[0],XDAT.shape[0]))
for k1 in range(fert_set.shape[0]):
  fert_set[k1,:] = np.interp(XDAT, fert_yr, fert_mat[k1,:])
fert_set = fert_set/1000.0 # births/woman/year

#*******************************************************************************


DIRNAMES = ['experiment_sweepRI_popEQL_noSIAs',
            'experiment_sweepRI_popEQL_noSIAs_impHI' ]


for dirname in DIRNAMES:

  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  ss_demog     =     param_dict['EXP_CONSTANT']['steady_state_demog']

  try: 
    ri_vec = np.array(param_dict['EXP_VARIABLE']['RI_rate'])
  except:
    ri_vec = np.ones(nsims) * param_dict['EXP_CONSTANT']['RI_rate']

  ri_lev       = sorted(list(set(ri_vec.tolist())))
  pyr_mat      = np.zeros((nsims,int(run_years)+1,20))-1
  inf_mat      = np.zeros((nsims,int(run_years),20))
  birth_mat    = np.zeros((nsims,int(run_years)   ))

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


  # Figures - Sims - CRS
  axs01 = fig01.add_subplot(1, 2, 1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_ylabel('Annual CRS Burden per 1k Births', fontsize=16)

  axs01.set_xlim(2020, 2050)
  axs01.set_ylim( 0.0,  5.0)

  axs01.set_yticks(ticks=np.arange(0,5.1,0.5))
  axs01.set_yticklabels(['0','','1','','2','','3','','4','','5'],fontsize=16)
  axs01.tick_params(axis='x', labelsize=16)

  for ri_val in ri_lev:
    if(ri_val not in [0.0, 0.6]):
      continue
    gidx        = (ri_vec==ri_val) & fidx
    inf_mat_avg = np.mean(inf_mat[gidx,:,:],axis=0)
    crs_mat     = inf_mat_avg*np.transpose(crs_prob_vec)
    ydat        = np.sum(crs_mat,axis=1)/birth_vec*norm_crs_timevec*1e3
    xdat        = np.arange(start_year, start_year+run_years) + 0.5

    axs01.plot(xdat,ydat,label='RI = {:3d}%'.format(int(100*ri_val)),
                         color='C{:d}'.format(ri_lev.index(ri_val)))


  # Figures - Sims - CRS Histogram
  axs01 = fig01.add_subplot(1, 2, 2)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_ylabel('Probability: 2040 to 2050', fontsize=16)
  axs01.set_xlabel('Annual CRS Burden per 1k Births', fontsize=16)

  xmaxv = 16
  xbinv =  0.1
  axs01.set_xlim(0.0, xmaxv)
  axs01.set_ylim(0.0, 10.0)
  axs01.set_yscale('symlog', linthresh=0.1)

  axs01.tick_params(axis='x', labelsize=16)
  axs01.tick_params(axis='y', labelsize=16)

  for ri_val in ri_lev:
    if(ri_val not in [0.0, 0.6]):
      continue
    gidx        = (ri_vec==ri_val) & fidx
    inf_mat_sub = inf_mat[gidx,:,:]
    crs_mat     = inf_mat_sub*np.transpose(crs_prob_vec)
    ydat        = np.sum(crs_mat,axis=2)/birth_vec*norm_crs_timevec*1e3
    ydat        = ydat[:,-10:].flatten()
    axs01.hist(ydat, bins=np.arange(0,xmaxv+xbinv,xbinv)-ri_val/20, density=True, alpha=0.7,
                     label='RI = {:3d}%'.format(int(100*ri_val)),
                     color='C{:d}'.format(ri_lev.index(ri_val)))

  axs01.legend(fontsize=14)


  plt.tight_layout()
  plt.savefig('fig_var_{:s}_01.png'.format(dirname))
  plt.close()


#*******************************************************************************
