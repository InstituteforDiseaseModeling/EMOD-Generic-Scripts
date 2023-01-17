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



with open(os.path.join(tpath,'param_dict_iters.json')) as fid01:
  param_dict = json.load(fid01)

with open(os.path.join(tpath,'data_brick_iters.json')) as fid01:
  data_brick = json.load(fid01)



# Create figure
fig01 = plt.figure(figsize=(8,6))

axs01 = fig01.add_subplot(1, 1, 1)
plt.sca(axs01)

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)


x1data = list()
x2data = list()
x3data = list()
x4data = list()
cdata  = list()



for iter_num_str in param_dict:

  nsims    = int(param_dict[iter_num_str]['NUM_SIMS'])

  x1data.extend(param_dict[iter_num_str]['EXP_VARIABLE']['log10_import_rate'])
  x2data.extend(param_dict[iter_num_str]['EXP_VARIABLE']['R0'])
  x3data.extend(param_dict[iter_num_str]['EXP_VARIABLE']['SIA_Coverage'])
  #x4data.extend(param_dict[iter_num_str]['EXP_VARIABLE']['R0_peak_day'])


  calib_vec = np.zeros(nsims) + 1
  for sim_idx_str in data_brick[iter_num_str]:
    if(sim_idx_str.isdecimal()):
      sim_idx = int(sim_idx_str)

      yvals = np.zeros(12*3)
      for kstr in data_brick[iter_num_str][sim_idx_str]:
        if(kstr.startswith('AFRO:DRCONGO')):
          yvals += np.array(data_brick[iter_num_str][sim_idx_str][kstr])
      (obj_val, scal_vec) = norpois_opt([ref_dat], yvals[:len(ref_dat)])
      calib_vec[sim_idx] = obj_val
  cdata.extend(calib_vec.tolist())

cdata  = np.array(cdata)
fidx   = (cdata<0)
cdata  = cdata[fidx]
x1data = np.array(x1data)[fidx]
x2data = np.array(x2data)[fidx]
x3data = np.array(x3data)[fidx]
#x4data = np.array(x4data)[fidx]
sidx   = np.argsort(cdata)

print(sidx[-1],x1data[sidx[-1]],x2data[sidx[-1]],x3data[sidx[-1]])
print(cdata[sidx[-1]])



yvals = np.zeros(12*3)
xvals = np.array(data_brick['05']['tstamps'])
for kstr in data_brick['05']['00153']:
  if(kstr.startswith('AFRO:DRCONGO')):
    yvals += np.array(data_brick['05']['00153'][kstr])

(obj_val, scal_vec) = norpois_opt([ref_dat], yvals[:len(ref_dat)])
print(obj_val,scal_vec)


#axs01.plot(xvals/365+1900,yvals*scal_vec)
axs01.plot(inft)

#axs01.scatter(x1data[sidx], x2data[sidx], c=cdata[sidx], vmin=-1.5e5)

# Save figure
plt.tight_layout()
plt.savefig('fig_calib_01.png')
plt.close()

#*******************************************************************************
