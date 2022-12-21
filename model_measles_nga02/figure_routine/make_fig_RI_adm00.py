#*******************************************************************************

import os, json, sys

sys.path.append(os.path.join('..','Assets','python'))

import numpy               as np
import matplotlib.pyplot   as plt

import global_data as gdata

#*******************************************************************************

icme_nga_ref_ri = [0.505,0.555,0.571,0.597,0.621]
icme_nga_ref_yr = [ 2015, 2016, 2017, 2018, 2019]

#*******************************************************************************


DIRNAME = 'experiment_demog01'


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

init_year    = int(gdata.start_year)
nsims        = int(param_dict['NUM_SIMS'])
num_years    = int(param_dict['EXP_CONSTANT']['num_years'])
change_ri    =     param_dict['EXP_CONSTANT']['change_RI']
pop_dat_var  =     param_dict['EXP_VARIABLE']['nga_state_name']
pop_dat_opt  = list(set(pop_dat_var))
pop_dat_var  = np.array(pop_dat_var)

tvals_mo     = data_brick.pop('tstamps_mo')
tvals_yr     = data_brick.pop('tstamps_yr')
riBlock      = np.zeros((nsims,len(tvals_yr)))-1
nbBlock      = np.zeros((nsims,len(tvals_yr)))

for sim_idx_str in data_brick:
  riBlock[int(sim_idx_str),:] = np.array(data_brick[sim_idx_str]['ri_yr'])
  nbBlock[int(sim_idx_str),:] = np.diff([0]+data_brick[sim_idx_str]['births_yr'])

fidx = (riBlock[:,0]>=0)


# Figure
fig01 = plt.figure(figsize=(8,6))
axs01 = fig01.add_subplot(111)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.tick_params(axis='both', which='major', labelsize=14)
axs01.set_axisbelow(True)


icme_nga_ref_yr.append(icme_nga_ref_yr[-1] + 1.0)
icme_nga_ref_ri.append(np.mean(icme_nga_ref_ri[-3:]))
for k2 in range(1,100):
  new_time = icme_nga_ref_yr[-1] + 1.0
  new_rate = max((1.0 - (1.0-icme_nga_ref_ri[-1]) * (1.0-change_ri)),0.0)
  icme_nga_ref_yr.append(new_time)
  icme_nga_ref_ri.append(new_rate)

axs01.plot(np.array(icme_nga_ref_yr)+0.5,100*np.array(icme_nga_ref_ri),
           'k.-',lw=2.0,ms=8.0,label='Reference')

ri_tot = np.zeros(len(tvals_yr))
nb_tot = np.zeros(len(tvals_yr))
for pop_dat_str in pop_dat_opt:
  gidx = (pop_dat_var==pop_dat_str)
  ri_tot += np.mean(riBlock[fidx&gidx,:],axis=0)
  nb_tot += np.mean(nbBlock[fidx&gidx,:],axis=0)
yval = ri_tot/nb_tot
xval = np.array(tvals_yr)/365+1900

axs01.bar(xval,100*yval, color='C0',edgecolor='k', width=1.0, label='Simulated')
axs01.set_ylabel('MCV RI Coverage (%)',fontsize=18)

axs01.set_xlim(2015, 2045)
axs01.set_ylim(  46,   64)

ticloc = np.arange(46,65,2)
ticlab = ['46','48','50','52','54','56','58','60','62','64']
axs01.set_yticks(ticks=ticloc)
axs01.set_yticklabels(ticlab)

axs01.legend()

# Save figure
plt.tight_layout()
plt.savefig('fig_RI_NGA_01.png')
plt.close()


#*******************************************************************************