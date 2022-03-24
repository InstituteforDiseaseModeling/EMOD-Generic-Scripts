#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

from builder_demographics import pop_age_days

#*******************************************************************************


DIRNAME = 'experiment_demog_WPP01'


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

nsims        = int(param_dict['NUM_SIMS'])
init_year    = int(param_dict['EXP_CONSTANT']['start_year'])
num_years    = int(param_dict['EXP_CONSTANT']['num_years'])
pop_dat_str  =     param_dict['EXP_CONSTANT']['pop_dat_file']

pyr_mat      = np.zeros((nsims,num_years+1,20))
year_vec     = np.arange(init_year, init_year+num_years+1)
chart_yrs    = year_vec[np.mod(year_vec,5)==0]
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])

fname_pop = os.path.join('..','Assets','data','pop_dat_{:s}.csv'.format(pop_dat_str))
pop_input = np.loadtxt(fname_pop, dtype=int, delimiter=',')

year_vec_dat  = pop_input[0, :]
pop_mat_dat   = pop_input[1:,:]
tpop_dat      = np.sum(pop_mat_dat,axis=0)

pyr_mat_avg   = np.mean(pyr_mat,axis=0)
tpop_avg      = np.sum(pyr_mat_avg,axis=1)


# Figures
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(1, 1, 1)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('Year', fontsize=14)
axs01.set_ylabel('Error - Total Population (%)', fontsize=14)

axs01.set_xlim(1950, 2090)
axs01.set_ylim( -12,   12)

ticloc = np.arange(1950,2100,10)
ticlab = ['1950', '', '1970', '', '1990', '', '2010', '',
          '2030', '', '2050', '', '2070', '', '2090']
axs01.set_xticks(ticks=ticloc)
axs01.set_xticklabels(ticlab)

ticloc = np.arange(-12,13,2)
ticlab = ['-12', '-10', '-8', '-6', '-4', '-2',
          '0', '2', '4', '6', '8', '10', '12']
axs01.set_yticks(ticks=ticloc)
axs01.set_yticklabels(ticlab)

axs01.plot([1950,2090],[0,0], c=[0.4,0.4,0.4])

yidx  = np.intersect1d(chart_yrs, year_vec, return_indices=True)[2]
y_sim = tpop_avg[yidx]

yidx  = np.intersect1d(chart_yrs, year_vec_dat, return_indices=True)[2]
y_ref = tpop_dat[yidx]

axs01.plot(chart_yrs, 100*(y_sim-y_ref)/y_ref, c='k', marker='.', ms=14)

plt.tight_layout()
plt.savefig('fig_err_{:s}_01.png'.format(pop_dat_str))
plt.close()


#*******************************************************************************