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

axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
axs01.set_axisbelow(True)

axs01.set_xlabel('R$_{\mathrm{0}}$',fontsize=16)
axs01.set_ylabel('Population Fraction',fontsize=16)

axs01.set_xlim( 0.50, 1.75)
axs01.set_ylim(-0.01, 0.81)

axs01.plot([1,1],[0,1],'k--')
axs01.plot([0,2],[0,0],'k-')


# Reference trajectory (Kermack-McKendric analytic solution)
def KMlimt (x,R0):
  return 1-x-np.exp(-x*R0)

xref = np.linspace(1.01,2.0,200)
yref = np.zeros(xref.shape)
for k1 in range(yref.shape[0]):
  yref[k1] = spopt.brentq(KMlimt, 1e-5, 1, args=(xref[k1]))
axs01.plot(xref,yref,'k-',lw=5.0,label='Attack Rate')


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

ntstp    = int(param_dict['EXP_CONSTANT']['num_tsteps'])
R0       = np.array(param_dict['EXP_VARIABLE']['R0'])
R0_VAR   = np.round(np.array(param_dict['EXP_VARIABLE']['R0_variance']),2)
ACQ_VAR  = np.round(np.array(param_dict['EXP_VARIABLE']['indiv_variance_acq']),2)
COR_VAL  = np.round(np.array(param_dict['EXP_VARIABLE']['correlation_acq_trans']),2)

r0_var_lev  = sorted(list(set(np.round(R0_VAR,2).tolist())))
acq_var_lev = sorted(list(set(np.round(ACQ_VAR,2).tolist())))
cor_lev     = sorted(list(set(np.round(COR_VAL,2).tolist())))
inf_var_lev = [0.5]

inf_mat  = np.zeros(param_dict['NUM_SIMS'])
hrd_mat  = np.zeros(param_dict['NUM_SIMS'])
for sim_idx_str in data_brick:
  sim_idx = int(sim_idx_str)
  inf_mat[sim_idx] = np.array(data_brick[sim_idx_str]['atk_frac'])
  hrd_mat[sim_idx] = np.array(data_brick[sim_idx_str]['herd_frac'])

gidx      = (R0_VAR == r0_var_lev[2]) & (ACQ_VAR == acq_var_lev[0]) & (COR_VAL == cor_lev[0])
str_set   = ['{:3.1f}'.format(inf_var_lev[0]),'{:3.1f}'.format(acq_var_lev[0]),'{:3.1f}'.format(cor_lev[0])]
label_str = 'Var$_{trans}$='+str_set[0]+'; Var$_{acq}$='+str_set[1]+'; Corr='+str_set[2]
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str, c='C0')

gidx      = (R0_VAR == r0_var_lev[2]) & (ACQ_VAR == acq_var_lev[1]) & (COR_VAL == cor_lev[0])
str_set   = ['{:3.1f}'.format(inf_var_lev[0]),'{:3.1f}'.format(acq_var_lev[1]),'{:3.1f}'.format(cor_lev[0])]
label_str = 'Var$_{trans}$='+str_set[0]+'; Var$_{acq}$='+str_set[1]+'; Corr='+str_set[2]
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str, c='C1')

gidx      = (R0_VAR == r0_var_lev[1]) & (ACQ_VAR == acq_var_lev[1]) & (COR_VAL == cor_lev[1])
str_set   = ['{:3.1f}'.format(inf_var_lev[0]),'{:3.1f}'.format(acq_var_lev[1]),'{:3.1f}'.format(cor_lev[1])]
label_str = 'Var$_{trans}$='+str_set[0]+'; Var$_{acq}$='+str_set[1]+'; Corr='+str_set[2]
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str, c='C2')

gidx      = (R0_VAR == r0_var_lev[0]) & (ACQ_VAR == acq_var_lev[1]) & (COR_VAL == cor_lev[2])
str_set   = ['{:3.1f}'.format(inf_var_lev[0]),'{:3.1f}'.format(acq_var_lev[1]),'{:3.1f}'.format(cor_lev[2])]
label_str = 'Var$_{trans}$='+str_set[0]+'; Var$_{acq}$='+str_set[1]+'; Corr='+str_set[2]
axs01.plot(R0[gidx], inf_mat[gidx], lw=0.0, marker='.', label=label_str, c='C3')

#axs01.legend()


# Generate figures
plt.tight_layout()
plt.savefig(os.path.join('fig_attackrate01.png'))
plt.close()


#*******************************************************************************
