#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

ext_py_path = os.path.join('Assets','site-packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy as np

#*******************************************************************************

def application(timestep):

  # Example interface for in-processing;
  if(gdata.first_call_bool):
    gdata.first_call_bool = False

    timeval = float(timestep)
    print("Hello and goodbye from in-process at time {:.1f}".format(timeval))


  return None

#*******************************************************************************
