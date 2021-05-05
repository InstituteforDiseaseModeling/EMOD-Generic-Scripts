#*******************************************************************************

import numpy               as np
import matplotlib.pyplot   as plt

#*******************************************************************************

N        = 1000


# Figure
fig01 = plt.figure(figsize=(12,9))

axs00 = fig01.add_subplot(111)
axs00.spines['top'].set_color('none')
axs00.spines['bottom'].set_color('none')
axs00.spines['left'].set_color('none')
axs00.spines['right'].set_color('none')
axs00.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

#axs00.set_title('')

rep_set  = [ 221, 222, 223, 224]
acq_set  = [ 0.0, 0.5, 0.5, 0.5]
inf_set  = [ 0.5, 0.5, 0.5, 0.5]
cor_set  = [ 0.0, 0.0, 0.5, 1.0]
clr_set  = [   0,   1,   2,   3]

for k1 in range(len(rep_set)):
  axs01 = fig01.add_subplot(rep_set[k1],label=None)
  plt.sca(axs01)

  axs01.grid(b=True, which='major', ls='-', lw=0.5, label='')
  axs01.grid(b=True, which='minor', ls=':', lw=0.1)
  axs01.set_axisbelow(True)

  axs01.set_xlabel('Acquision Risk')
  axs01.set_ylabel('Transmit Risk')

  axs01.set_xlim(0,6)
  axs01.set_ylim(0,6)

  AQ_VAR   = acq_set[k1]
  BI_SIG   = inf_set[k1]
  rho      = cor_set[k1]

  LNSIG  = np.sqrt(np.log(AQ_VAR+1.0))
  LNMU   = -0.5*LNSIG*LNSIG
  BIMU   = -0.5*BI_SIG*BI_SIG

  risk_vec   = np.random.lognormal(mean=LNMU, sigma=LNSIG,  size=N)
  inf_vec    = np.random.lognormal(mean=BIMU, sigma=BI_SIG, size=N)
  corr_vec   = inf_vec*(1 + rho*(risk_vec - 1))

  #print(np.mean(risk_vec),np.var(risk_vec))
  #print(np.mean(inf_vec), np.var(inf_vec))
  #print(np.mean(corr_vec),np.var(corr_vec))
  #print(np.cov(risk_vec,corr_vec))

  axs01.plot(risk_vec,corr_vec,marker='.',lw=0.0,color='C{:d}'.format(clr_set[k1]))


plt.savefig('fig_distributions01.png')
plt.savefig('fig_distributions01.svg')

plt.close()

#*******************************************************************************