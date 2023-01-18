#*******************************************************************************

import os, json

import numpy               as np
import matplotlib.pyplot   as plt

from aux_obj_calc     import     norpois_opt

ref_dat = [  175,   133,   155,   312,   179,   149,
             143,   216,   398,   498,   882,  2189,
            6472,  9046, 18093, 18482, 13197, 16998,
           20451, 12851,  6256,  4314,  4622,  2996,
            4164,  3985,  4558,  3635,  3188,  4695,
            5592,  7444,  6302, 11126, 10794,  8323]

#*******************************************************************************


DIRNAME = 'experiment_meas_cod_base01'


# Sim outputs
tpath = os.path.join('..',DIRNAME)



with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)



# Create figure
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(1, 1, 1)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)




nsims    = int(param_dict['NUM_SIMS'])

#x1data = np.array(param_dict['EXP_VARIABLE']['SIA_Coverage'])
#x2data = np.array(param_dict['EXP_VARIABLE']['net_inf_ln_mult'])
#x3data = np.array(param_dict['EXP_VARIABLE']['net_inf_power'])

#print(np.max(x1data))

cdata = np.zeros(nsims)
nplot = 0
meantra = np.zeros(7*365+1)
for sim_idx_str in data_brick:
  if(sim_idx_str.isdecimal()):
    sim_idx = int(sim_idx_str)
    if(#x1data[sim_idx] ==  0.80 and
       #x2data[sim_idx] == -1.2  and
       #x3data[sim_idx] ==  1.4 and
       nplot < 50):
    #if(sim_idx == 1327):
      if(data_brick[sim_idx_str]['cal_val'] < -9e4):
        continue
      sfac = data_brick[sim_idx_str]['rep_rate']
      if(sfac > 1):
        continue
      #print(x1data[sim_idx],x2data[sim_idx],x3data[sim_idx])
      mobins = np.zeros(3*12,dtype=float)
      for kstr in data_brick[sim_idx_str]:
        if kstr.startswith('AFRO:DRCONGO'):
          mobins += np.array(data_brick[sim_idx_str][kstr])*sfac
      axs01.plot(2010+((np.arange(3*12)+0.5)/12),mobins)#,c='C0')
      #axs01.plot(np.array(data_brick[sim_idx_str]['inf_trace'])*sfac)#,c='C0')
      #meantra += np.array(data_brick[sim_idx_str]['inf_trace'])
      nplot += 1
      print(data_brick[sim_idx_str]['cal_val'],sfac)
    cdata[sim_idx] = data_brick[sim_idx_str]['cal_val']

#axs01.plot(np.arange(meantra.shape[0])/365+2006,meantra)

fidx   = (cdata<0)
cdata  = cdata[fidx]
#x1data = x1data[fidx]
#x2data = x2data[fidx]
sidx   = np.argsort(cdata)

#print(sidx[-1],x1data[sidx[-1]],x2data[sidx[-1]],x3data[sidx[-1]])
print()
print(cdata[sidx[-1]])



#yvals = np.zeros(12*3)
#xvals = np.array(data_brick['05']['tstamps'])
#for kstr in data_brick['05']['00153']:
#  if(kstr.startswith('AFRO:DRCONGO')):
#    yvals += np.array(data_brick['05']['00153'][kstr])



#axs01.plot(xvals/365+1900,yvals*scal_vec)

#axs01.hist(cdata,bins=250)
#axs01.scatter(x1data[sidx], x2data[sidx], c=cdata[sidx], vmin=-1.5e5)

# Save figure
plt.tight_layout()
plt.savefig('fig_calib_02viz.png')
plt.close()

#*******************************************************************************
