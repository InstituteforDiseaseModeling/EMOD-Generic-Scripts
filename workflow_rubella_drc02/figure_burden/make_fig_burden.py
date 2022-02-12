#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process      import  tpop_2020

EPS = np.finfo(float).eps

# Probability vector (20 age bins, 5yr each) that a rubella infection will
# result in a case of congenital rubella syndrome (CRS).
crs_prob_vec  = np.ones(20)           # Start with uniform, unity probability
crs_prob_vec  = crs_prob_vec * 0.5    # Probability female


fe_frtr_dhs   = [  0,   0,   9, 148,  # DHS fertility rate (FE_FRTR_W)
                 379, 388, 292, 331,  # (births per 1k women per 3yrs)
                  98,   9,   0,   0,
                   0,   0,   0,   0,
                   0,   0,   0,   0]


fe_frtr_dhs   = np.array(fe_frtr_dhs)/1000.0  # Births, per-woman, per 3yrs
fe_frtr_dhs   = fe_frtr_dhs/3.0               # Births, per-woman, per yr
fe_frtr_dhs   = fe_frtr_dhs*(9.0/12.0)        # Fraction pregnant, per-woman, per-year
fe_frtr_dhs   = fe_frtr_dhs*(0.85*13/39 + 0.50*13/39 + 0.50*4/39)
                                              # Probability of CRS during pregnancy

crs_prob_vec  = crs_prob_vec * fe_frtr_dhs

#*******************************************************************************


DIRNAME = 'experiment_sweepRI_noSIAs'


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

nsims        = int(param_dict['NUM_SIMS'])
ntstp        = int(param_dict['EXP_CONSTANT']['num_tsteps'])
pop_dat_str  = param_dict['EXP_CONSTANT']['pop_dat_file']

try: 
  ri_vec   = np.array(param_dict['EXP_VARIABLE']['RI_rate'])
except:
  ri_vec   = np.ones(nsims) * param_dict['EXP_CONSTANT']['RI_rate']

ri_lev   = sorted(list(set(ri_vec.tolist())))


pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])

inf_mat = np.zeros((nsims,int(ntstp/365),20))
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  inf_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['inf_data'])

fname_pop = os.path.join('..','Assets','data','pop_data_{:s}.csv'.format(pop_dat_str))
pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

year_vec  = pop_input[0,:]
pop_mat   = pop_input[1:,:]

diff_ratio = pop_mat[1:,1:]/(pop_mat[:-1,:-1]+EPS)
pow_vec    = 365.0*np.diff(year_vec)
mortvecs   = 1.0-np.power(diff_ratio,1.0/pow_vec)
tot_pop    = np.sum(pop_mat,axis=0)

brate_vec    = np.round(pop_mat[0,1:]/tot_pop[:-1]/5.0*1000.0,1)
br_base_val  = brate_vec[0]
br_mult_xvec = year_vec[:-1].tolist()
br_mult_yvec = (brate_vec/br_base_val).tolist()

pyr_mat_avg = np.mean(pyr_mat,axis=0)
ref_rat     = tpop_2020/np.sum(pyr_mat_avg[20,:])
pop_tot     = np.sum(pyr_mat_avg,axis=1)
pop_tot     = np.diff(pop_tot)/2.0 + pop_tot[:-1]

br_force    = np.interp(np.arange(2000.5,2050),br_mult_xvec,br_mult_yvec)
birth_vec   = pop_tot*br_base_val*br_force/1000


# Figures
fig01 = plt.figure(figsize=(16,6))


# Figures - Sims - Infections
axs01 = fig01.add_subplot(121, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('Total Infections per 100k', fontsize=14)

axs01.set_xlim(  20,   50)
axs01.set_ylim(   0, 6000)

ticloc = [20, 30, 40, 50]
ticlab = ['2020', '2030', '2040', '2050']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

for ri_val in ri_lev:
  gidx        = (ri_vec==ri_val)
  inf_mat_avg = np.mean(inf_mat[gidx,:,:],axis=0)
  ydat        = np.sum(inf_mat_avg,axis=1)/pop_tot*1e5
  xdat        = np.arange(0,50) + 0.5

  axs01.plot(xdat,ydat,label='RI = {:3d}%'.format(int(100*ri_val)))

axs01.legend()


# Figures - Sims - CRS
axs01 = fig01.add_subplot(122, label=None)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('CRS Burden per 1k Births', fontsize=14)

axs01.set_xlim(  20.0, 50.0)
#axs01.set_ylim(   0.0,  1.2)
ticloc = [20, 30, 40, 50]
ticlab = ['2020', '2030', '2040', '2050']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

for ri_val in ri_lev:
  gidx        = (ri_vec==ri_val)
  inf_mat_avg = np.mean(inf_mat[gidx,:,:],axis=0)
  crs_mat     = inf_mat_avg*crs_prob_vec
  ydat        = np.sum(crs_mat,axis=1)/birth_vec*1e3
  xdat        = np.arange(0,50) + 0.5

  axs01.plot(xdat,ydat,label='RI = {:3d}%'.format(int(100*ri_val)))

axs01.legend()

plt.tight_layout()
plt.savefig('fig_inf_set_01.png')
plt.close()



#*******************************************************************************
