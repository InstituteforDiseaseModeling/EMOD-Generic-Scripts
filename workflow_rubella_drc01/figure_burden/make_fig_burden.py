#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from dtk_post_process      import  tpop_2020

from builder_demographics  import  br_base_val

# TO DO: Build this vector in asset files
# (probability an infection in age-bracket results in CRS)
conv_vec = [0.0,                    0.0,
            0.0005639423076923077,  0.009273717948717949,
            0.02374823717948718,    0.024312179487179489,
            0.018296794871794875,   0.020740544871794873,
            0.006140705128205128,   0.0005639423076923077,
            0.0,                    0.0,
            0.0,                    0.0,
            0.0,                    0.0,
            0.0,                    0.0,
            0.0,                    0.0]

#*******************************************************************************

DIRNAME = 'experiment_sweepRI_noSIAs'


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

nsims    = int(param_dict['NUM_SIMS'])
ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
ri_vec   = np.array(param_dict['EXP_VARIABLE']['RI_rate'])
ri_lev   = sorted(list(set(ri_vec.tolist())))


pyr_mat = np.zeros((nsims,int(ntstp/365)+1,20))
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])

inf_mat = np.zeros((nsims,int(ntstp/365),20))
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  inf_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['inf_data'])




pyr_mat_avg = np.mean(pyr_mat,axis=0)
ref_rat     = tpop_2020/np.sum(pyr_mat_avg[20,:])
pop_tot     = np.sum(pyr_mat_avg,axis=1)
pop_tot     = np.diff(pop_tot)/2.0 + pop_tot[:-1]

birth_vec   = pop_tot*br_base_val/1000


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
axs01.set_ylim(   0.0,  1.2)
ticloc = [20, 30, 40, 50]
ticlab = ['2020', '2030', '2040', '2050']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

for ri_val in ri_lev:
  gidx        = (ri_vec==ri_val)
  inf_mat_avg = np.mean(inf_mat[gidx,:,:],axis=0)
  crs_mat     = inf_mat_avg*conv_vec
  ydat        = np.sum(crs_mat,axis=1)/birth_vec*1e3
  xdat        = np.arange(0,50) + 0.5

  axs01.plot(xdat,ydat,label='RI = {:3d}%'.format(int(100*ri_val)))

axs01.legend()

plt.tight_layout()
plt.savefig('fig_inf_set_01.png')
plt.close()



#*******************************************************************************
