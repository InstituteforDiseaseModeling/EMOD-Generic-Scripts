#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import os, sys

import global_data as gd

ext_py_path = os.path.join('Assets','site-packages')
if(ext_py_path not in sys.path):
  sys.path.append(ext_py_path)

import numpy as np

#*******************************************************************************

def application(timestep):

  if(gd.first_call_bool):
    gd.first_call_bool = False
    timeval = float(timestep)
    print("Hello and goodbye from in-process at time {:.1f}".format(timeval))

  return None

#end-application

#*******************************************************************************
