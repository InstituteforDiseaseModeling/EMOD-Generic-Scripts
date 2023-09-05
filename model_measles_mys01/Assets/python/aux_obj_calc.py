#*******************************************************************************
#
#*******************************************************************************

import numpy as np

#*******************************************************************************

EPS = np.finfo(float).eps

#*******************************************************************************

def norpois_vec(yobs, ysim, yscal=1.0):

  lliktot   = 0.0
  Gtot      = 0.0
  Htot      = 0.0
  mlam      = 0.1 

  for k1 in range(len(yobs)):
    yobsval = float(yobs[k1])
    ysimval = float(ysim[k1])
    llik    = 0.0
    G       = 0.0
    H       = 0.0

    if(yobsval>0):
      llik = yobsval*np.log((yscal*ysimval + mlam)/yobsval) \
             - yscal*ysimval - mlam + yobsval - 0.5*np.log(2.0*np.pi*yobsval)
      G    = yobsval - ysimval*yscal 
      H    =         - ysimval*yscal
    elif(yobs==0):
      llik = -ysimval*yscal - mlam
      G    = -ysimval*yscal
      H    = -ysimval*yscal

    lliktot = lliktot + llik
    Gtot    = Gtot + G
    Htot    = Htot + H

  if(Htot != 0.0):
    sstptot = Gtot/Htot
  else:
    sstptot = 0.0;

  return (lliktot,sstptot)

#*******************************************************************************

def norpois_opt(yobs, ysim):

  LLret = 0
  SFvec = []

  for k1 in range(len(yobs)):
    lyscal = 0.0
    yobs = yobs[k1]
  
    while(True):
      (lliktot,sstptot) = norpois_vec(yobs, ysim, np.exp(lyscal))

      if(abs(sstptot) > 5.0):
        sstptot = np.sign(sstptot)*5.0

      lyscal = lyscal - sstptot
      if(abs(sstptot) < 1.0e-4):
        break

    LLret = LLret + lliktot
    SFvec.append(np.exp(lyscal))

  return (LLret,SFvec)

#*******************************************************************************