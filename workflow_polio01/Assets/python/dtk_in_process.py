#********************************************************************************
#
#********************************************************************************

import os, sys

import global_data as gd

import numpy as np

#*******************************************************************************

def application(timestep):

  if(gd.first_call_bool):
    gd.first_call_bool = False
    timeval = float(timestep)
    print("Hello and goodbye from in-process at time {:.1f}".format(timeval))

  return None

#*******************************************************************************
