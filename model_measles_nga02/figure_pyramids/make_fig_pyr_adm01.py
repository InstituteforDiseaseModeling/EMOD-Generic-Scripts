#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

import global_data as gdata

from builder_demographics import pop_age_days

#*******************************************************************************


DIRNAME = 'experiment_demog01'


CM    = np.array([ 70,130,180])/255
CF    = np.array([238,121,137])/255


STATE_DIR = 'adm01_pyramids'
if(not os.path.exists(STATE_DIR)):
  os.mkdir(STATE_DIR)


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

init_year    = int(gdata.start_year)
nsims        = int(param_dict['NUM_SIMS'])
num_years    = int(param_dict['EXP_CONSTANT']['num_years'])
pop_dat_var  =     param_dict['EXP_VARIABLE']['nga_state_name']
pop_dat_opt  = list(set(pop_dat_var))
pop_dat_var  = np.array(pop_dat_var)

tvals_mo     = data_brick.pop('tstamps_mo')
tvals_yr     = data_brick.pop('tstamps_yr')

pyr_mat      = np.zeros((nsims,num_years+1,20))-1
year_vec     = np.arange(init_year, init_year+num_years+1)
chart_yrs    = year_vec[np.mod(year_vec,10)==5]
num_charts   = chart_yrs.shape[0]

for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  pyr_mat[sim_idx,:,:] = np.array(data_brick[sim_idx_str]['pyr_data'])

fidx = (pyr_mat[:,0,0]>=0)


for pop_dat_str in pop_dat_opt:

  fig01 = plt.figure(figsize=(7*num_charts,6))

  sidx = (pop_dat_var==pop_dat_str)

  pyr_mat_avg = np.mean(pyr_mat[fidx&sidx,:,:],axis=0)
  pyr_mat_std = np.std(pyr_mat[fidx&sidx,:,:],axis=0)

  # Figures - Sims
  for k1 in range(num_charts):

    gidx  = np.argwhere(year_vec==chart_yrs[k1])[0][0]

    axs01 = fig01.add_subplot(1, num_charts, k1+1)
    plt.sca(axs01)

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Percentage', fontsize=14)
    axs01.set_ylabel('Age (yrs)', fontsize=14)

    if(k1 == num_charts-1):
      axs02 = axs01.twinx()
      axs02.set_ylabel('Simulation', fontsize=24)
      axs02.set_yticks(ticks=[0,1])
      axs02.set_yticklabels(['',''])

    axs01.set_xlim( -12,  12)
    axs01.set_ylim(   0, 100)

    ticloc = [-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12]
    ticlab = ['12', '10', '8', '6', '4', '2', '0', '2', '4', '6', '8', '10', '12']
    axs01.set_xticks(ticks=ticloc)
    axs01.set_xticklabels(ticlab)

    ydat        = np.array(pop_age_days)/365.0 - 2.5
    pop_dat     = pyr_mat_avg[gidx,:]
    pop_dat_err = pyr_mat_std[gidx,:]
    tpop        = np.sum(pop_dat)

    pop_dat_n     = 100*pop_dat/tpop
    pop_dat_n_err = 100*pop_dat_err/tpop

    axs01.barh(ydat[1:],  pop_dat_n/2.0, height=4.75, xerr=pop_dat_n_err, color=CF)
    axs01.barh(ydat[1:], -pop_dat_n/2.0, height=4.75, xerr=pop_dat_n_err, color=CM)

    axs01.text( -11, 87.5, '{:s}\n{:04d}'.format(pop_dat_str.replace('_',' '),
                                                 year_vec[gidx]), fontsize=18)
    axs01.text(   5, 87.5, 'Total Pop\n {:4.1f}M'.format(tpop/1e6), fontsize=18)

  # Save figure
  plt.tight_layout()
  plt.savefig(os.path.join(STATE_DIR,'fig_pyr_{:s}_01.png'.format(pop_dat_str)))
  plt.close()


#*******************************************************************************