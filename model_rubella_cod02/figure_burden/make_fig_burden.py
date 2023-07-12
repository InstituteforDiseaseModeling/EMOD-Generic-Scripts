#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

# Probability vector (20 age bins, 5yr each) that a rubella infection will
# result in a case of congenital rubella syndrome (CRS).
crs_prob_vec  = np.ones(20)           # Start with uniform, unity probability
crs_prob_vec  = crs_prob_vec * 0.5    # Probability female


fe_frtr_dhs   = [  0,   0,   9, 148,  # DHS fertility rate (FE_FRTR_W)
                 379, 388, 292, 331,  # (births per 1k women; avg over 3yrs)
                  98,   9,   0,   0,
                   0,   0,   0,   0,
                   0,   0,   0,   0]


fe_frtr_dhs   = np.array(fe_frtr_dhs)/1000.0  # Births per-woman
fe_bak        = fe_frtr_dhs
fe_frtr_dhs   = fe_frtr_dhs*(9.0/12.0)        # Fraction pregnant, per-woman, per-year
fe_frtr_dhs   = fe_frtr_dhs*(0.85*13/39 + 0.50*13/39 + 0.50*4/39)
                                              # Probability of CRS during pregnancy

crs_prob_vec  = crs_prob_vec * fe_frtr_dhs

#*******************************************************************************


DIRNAMES = ['experiment_sweepRI_noSIAs_popEQL',
            'experiment_sweepRI_noSIAs_popMED']


INIT_YR        = 2000
MAX_DAILY_MORT = 0.01


for dirname in DIRNAMES:
  # Sim outputs
  tpath = os.path.join('..',dirname)

  with open(os.path.join(tpath,'data_brick.json')) as fid01:
    data_brick = json.load(fid01)

  with open(os.path.join(tpath,'param_dict.json')) as fid01:
    param_dict = json.load(fid01)

  nsims        = int(param_dict['NUM_SIMS'])
  ntstp        = int(param_dict['EXP_CONSTANT']['num_tsteps'])
  pop_dat_str  =     param_dict['EXP_CONSTANT']['pop_dat_file']

  try: 
    ri_vec = np.array(param_dict['EXP_VARIABLE']['RI_rate'])
  except:
    ri_vec = np.ones(nsims) * param_dict['EXP_CONSTANT']['RI_rate']

  ri_lev       = sorted(list(set(ri_vec.tolist())))
  pyr_mat      = np.zeros((nsims,int(ntstp/365)+1,20))-1
  inf_mat      = np.zeros((nsims,int(ntstp/365),20))

  for sim_idx_str in data_brick:
    sim_idx = int(sim_idx_str)
    pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])

  for sim_idx_str in data_brick:
    sim_idx = int(sim_idx_str)
    inf_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['inf_data'])

  fidx = (pyr_mat[:,0,0]>=0)

  fname_pop = os.path.join('..','Assets','data','pop_dat_{:s}.csv'.format(pop_dat_str))
  pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

  year_vec   = pop_input[0,:]
  pop_mat    = pop_input[1:,:] + 0.1

  diff_ratio = (pop_mat[:-1,:-1]-pop_mat[1:,1:])/pop_mat[:-1,:-1]
  t_delta    = np.diff(year_vec)
  pow_vec    = 365.0*t_delta
  mortvecs   = 1.0-np.power(1.0-diff_ratio,1.0/pow_vec)
  mortvecs   = np.minimum(mortvecs, MAX_DAILY_MORT)
  mortvecs   = np.maximum(mortvecs,            0.0)
  tot_pop    = np.sum(pop_mat,axis=0)
  tpop_mid   = (tot_pop[:-1]+tot_pop[1:])/2.0
  pop_corr   = np.exp(-mortvecs[0,:]*pow_vec/2.0)

  brate_vec    = np.round(pop_mat[0,1:]/tpop_mid/t_delta*1000.0,1)/pop_corr
  br_base_val  = np.interp(INIT_YR, year_vec[:-1], brate_vec)

  yrs_off    = year_vec[:-1]-INIT_YR
  yrs_dex    = (yrs_off>0)

  brmultx_01 = np.array([0.0] + (365.0*yrs_off[yrs_dex]).tolist())
  brmulty_01 = np.array([1.0] + (brate_vec[yrs_dex]/br_base_val).tolist())
  brmultx_02 = np.zeros(2*len(brmultx_01)-1)
  brmulty_02 = np.zeros(2*len(brmulty_01)-1)

  brmultx_02[0::2] = brmultx_01[0:]
  brmulty_02[0::2] = brmulty_01[0:]
  brmultx_02[1::2] = brmultx_01[1:]-0.5
  brmulty_02[1::2] = brmulty_01[0:-1]

  br_mult_xvec = brmultx_02.tolist()
  br_mult_yvec = brmulty_02.tolist() 

  pyr_mat_avg = np.mean(pyr_mat[fidx,:,:],axis=0)
  pop_tot     = np.sum(pyr_mat_avg,axis=1)
  pop_tot     = np.diff(pop_tot)/2.0 + pop_tot[:-1]

  # Annual crude births implied by fertility distribution
  frt_dist_br = np.sum(pyr_mat_avg/2.0*fe_bak,axis=1)
  frt_dist_br = np.diff(frt_dist_br)/2.0 + frt_dist_br[:-1]

  # Annual crude births simulated in model
  yrs_vec     = np.arange(0, int(ntstp/365)) + 0.5
  br_force    = np.interp(yrs_vec,br_mult_xvec,br_mult_yvec)
  birth_vec   = pop_tot*br_base_val*br_force/1000

  # Normalization timeseries required for CRS calculation
  norm_crs_timevec = birth_vec/frt_dist_br


  # Figures
  fig01 = plt.figure(figsize=(16,6))


  # Figures - Sims - Infections
  axs01 = fig01.add_subplot(1, 2, 1)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  #axs01.set_xlabel('Year', fontsize=14)
  axs01.set_ylabel('Annual Rubella Infections per 100k', fontsize=16)

  axs01.set_xlim(2020, 2050)
  axs01.set_ylim(   0, 6000)

  axs01.set_yticks(ticks=np.arange(0,6001,1000))
  axs01.set_yticklabels(['0','1k','2k','3k','4k','5k','6k'],fontsize=16)
  axs01.tick_params(axis='x', labelsize=16)

  for ri_val in ri_lev:
    gidx        = (ri_vec==ri_val) & fidx
    inf_mat_avg = np.mean(inf_mat[gidx,:,:],axis=0)
    ydat        = np.sum(inf_mat_avg,axis=1)/pop_tot*1e5
    xdat        = np.arange(INIT_YR, INIT_YR+int(ntstp/365)) + 0.5

    axs01.plot(xdat,ydat,label='RI = {:3d}%'.format(int(100*ri_val)))

  axs01.legend(fontsize=14)


  # Figures - Sims - CRS
  axs01 = fig01.add_subplot(1, 2, 2)
  plt.sca(axs01)

  axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  #axs01.set_xlabel('Year', fontsize=14)
  axs01.set_ylabel('Annual CRS Burden per 1k Births', fontsize=16)

  axs01.set_xlim(2020, 2050)
  axs01.set_ylim( 0.0,  4.0)

  axs01.set_yticks(ticks=np.arange(0,4.1,0.5))
  axs01.set_yticklabels(['0','','1','','2','','3','','4'],fontsize=16)
  axs01.tick_params(axis='x', labelsize=16)

  for ri_val in ri_lev:
    gidx        = (ri_vec==ri_val) & fidx
    inf_mat_avg = np.mean(inf_mat[gidx,:,:],axis=0)
    crs_mat     = inf_mat_avg*crs_prob_vec
    ydat        = np.sum(crs_mat,axis=1)/birth_vec*norm_crs_timevec*1e3
    xdat        = np.arange(INIT_YR, INIT_YR+int(ntstp/365)) + 0.5

    axs01.plot(xdat,ydat,label='RI = {:3d}%'.format(int(100*ri_val)))

  axs01.legend(fontsize=14)

  plt.tight_layout()
  plt.savefig('fig_inf_{:s}_01.png'.format(pop_dat_str))
  plt.close()


#*******************************************************************************
