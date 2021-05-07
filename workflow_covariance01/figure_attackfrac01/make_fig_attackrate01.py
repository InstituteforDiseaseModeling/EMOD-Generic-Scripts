#*******************************************************************************

import os, json

import numpy              as np
import scipy.optimize     as spopt
import matplotlib.pyplot  as plt

#*******************************************************************************


DIRNAME = 'experiment_covariance01'


# Figure setup
fig01 = plt.figure(figsize=(8,6))
axs01 = fig01.add_subplot(111,label=None)
plt.sca(axs01)

axs01.grid(b=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(b=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('R$_{\mathrm{0}}$',fontsize=16)
axs01.set_ylabel('Attack Rate',fontsize=16)

axs01.set_xlim( 0.0, 2.0 )
axs01.set_ylim(-0.02,0.82)

axs01.plot([1,1],[0,1],'k--')
axs01.plot([0,2],[0,0],'k-')


# Reference trajectory (Kermack-McKendric analytic solution)
def KMlimt (x,R0):
  return 1-x-np.exp(-x*R0)

xref = np.linspace(1.01,2.0,200)
yref = np.zeros(xref.shape)
for k1 in range(yref.shape[0]):
  yref[k1] = spopt.brentq(KMlimt, 1e-5, 1, args=(xref[k1]))
axs01.plot(xref,yref,'k-',lw=5.0)


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
R0       = np.array(param_dict['EXP_VARIABLE']['R0'])
ACQ_VAR  = np.array(param_dict['EXP_VARIABLE']['indiv_variance_acq'])
COR_VAL  = np.array(param_dict['EXP_VARIABLE']['correlation_acq_trans'])

inf_mat = np.zeros(param_dict['num_sims'])
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  inf_mat[sim_idx] = np.array(data_brick[sim_idx_str])

gidx      = (ACQ_VAR == 0.0) & (COR_VAL == 0.0)
label_str = 'Acq = 0.0; Corr = 0.0'
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str)

gidx = (ACQ_VAR == 0.5) & (COR_VAL == 0.0)
label_str = 'Acq = 0.5; Corr = 0.0'
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str)

gidx = (ACQ_VAR == 0.5) & (COR_VAL == 0.5)
label_str = 'Acq = 0.5; Corr = 0.5'
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str)

gidx = (ACQ_VAR == 0.5) & (COR_VAL == 1.0)
label_str = 'Acq = 0.5; Corr = 1.0'
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str)

axs01.legend()

# Generate figures
plt.savefig(os.path.join('fig_attack01.png'))
plt.savefig(os.path.join('fig_attack01.svg'))


plt.close()

#*******************************************************************************
