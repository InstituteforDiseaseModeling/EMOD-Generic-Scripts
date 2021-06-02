#********************************************************************************
#
# Pairwise distance matrix
#
# Python 3.6.0
#
#********************************************************************************

import os, sys

import numpy as np

#********************************************************************************

def pair_dist_mat(pos_vec=None):

  ret_mat = np.zeros((pos_vec.shape[0],pos_vec.shape[0]))

  for k1 in range(pos_vec.shape[0]):
    delt_vec = np.sqrt(np.sum(np.square(pos_vec - pos_vec[k1,:]),axis=1))
    ret_mat[k1,:] = delt_vec

  return ret_mat

#end-pair_dist_mat

#********************************************************************************
