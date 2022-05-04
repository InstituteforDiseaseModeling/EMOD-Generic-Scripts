#*******************************************************************************

import os, json

import numpy              as np
import scipy.optimize     as spopt
import matplotlib.pyplot  as plt

#*******************************************************************************


DIRNAME = 'experiment_transtree01'


def rec_tree(targ_id):

  subdat  = tree_dat[tree_dat[:,3]==targ_id,:]
  subtree = list()

  for k1 in range(subdat.shape[0]):
    addleaf = rec_tree(subdat[k1,2])
    subtree.append([subdat[k1,0], addleaf])

  return subtree


def print_branch(axs_id, leaf_list, c_yval, pxy=None):

  sort_leaf = sorted(leaf_list, key=lambda val: val[0], reverse=True)

  for leaf_val in sort_leaf:
    axs_id.plot(leaf_val[0], c_yval, marker='.', lw=0, c='r', ms=0.5)
    new_pxy = (leaf_val[0], c_yval)
    if(pxy):
      if(pxy[0] < new_pxy[0]):
        xdat = [pxy[0]+0.25, pxy[0]+0.5, pxy[0]+0.5, new_pxy[0]-0.25]
        ydat = [pxy[1],      pxy[1],     new_pxy[1], new_pxy[1]]
      else: # Secondary infection on same timestep; edge case from seeding
        xdat = [pxy[0],   new_pxy[0]]
        ydat = [pxy[1]+1, new_pxy[1]-1]
      axs_id.plot(xdat, ydat, lw=0.5, c='k')
    c_yval = print_branch(axs_id, leaf_val[1], c_yval+5, new_pxy)

  return c_yval


# Sim outputs
tpath = os.path.join('..',DIRNAME)

with open(os.path.join(tpath,'data_brick.json')) as fid01:
  data_brick = json.load(fid01)

with open(os.path.join(tpath,'param_dict.json')) as fid01:
  param_dict = json.load(fid01)

BI_VAR = np.array(param_dict['EXP_VARIABLE']['base_inf_stddev_mult'])

sim_idx_list = sorted(data_brick.keys())
tree_list    = list()
for k1 in range(len(sim_idx_list)):
  if(k1 != int(sim_idx_list[k1])):
    raise Exception('Sim index mismatch')
  tree_list.append(np.array(data_brick[sim_idx_list[k1]]))


# Simulations with outbreak
obr_bool = np.array([tree.shape[0]>100 for tree in tree_list])

# Number of simulations at each level
sim_num  = np.array([np.sum(BI_VAR==0.0), np.sum(BI_VAR==1.0)])

# Number of simulations with outbreak at each level
obr_num  = np.array([np.sum(obr_bool[BI_VAR==0.0]),np.sum(obr_bool[BI_VAR==1.0])])

print(np.around(obr_num/sim_num, 3))

gdex0 = np.argwhere(obr_bool & (BI_VAR==0.0))[0,0]
gdex1 = np.argwhere(obr_bool & (BI_VAR==1.0))[0,0]


# Figure setup
fig01 = plt.figure(figsize=(48,36))

axs01 = fig01.add_subplot(121,label=None)
plt.sca(axs01)
axs01.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

tree_dat = tree_list[gdex0]
x_max    = np.max(tree_dat[:,0])
axs01.set_xlabel('Time',fontsize=14)
axs01.set_title('Constant Rate\nSecondary Infection',fontsize=16)
axs01.set_xlim(-10, x_max + 10)

t_struct = rec_tree(0)
print_branch(axs01, t_struct, 0)


axs01 = fig01.add_subplot(122,label=None)
plt.sca(axs01)
axs01.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

tree_dat = tree_list[gdex1]
x_max    = np.max(tree_dat[:,0])
axs01.set_xlabel('Time',fontsize=14)
axs01.set_title('Exponential Rate\nSecondary Infection',fontsize=16)
axs01.set_xlim(-10, x_max + 10)

t_struct = rec_tree(0)
print_branch(axs01, t_struct, 0)


# Generate figures
plt.tight_layout()
plt.savefig('fig_transtree_01.png')
plt.close()

#*******************************************************************************
