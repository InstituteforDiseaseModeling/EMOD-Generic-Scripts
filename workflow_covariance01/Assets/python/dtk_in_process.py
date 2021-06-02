#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import os, sys, json

import global_data as gdata

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
