#*******************************************************************************
#
#*******************************************************************************

import os, copy

import numpy as np

#*******************************************************************************

def next_point_alg(gen_param, sum_data, ex_val):

  # Control parameters
  radFrac  = 0.05 #0.35
  dimReq   = 8    #3
  frac_opt = 0.95


  # Local copy of parameters
  NUM_SIMS   = gen_param['NUM_SIMS']
  nSampOpt   =  int(frac_opt*NUM_SIMS)
  nSampRand  =  NUM_SIMS - nSampOpt

  pNames     =  copy.deepcopy(gen_param['VAR_NAMES'])
  pRanges    =  copy.deepcopy(gen_param['VAR_RANGES'])
  nDim       =  len(pNames)


  # Get summary values
  LLVec   = np.array(sum_data['OBJ_FUN'])


  # Prep output parameter dictionary
  paramDic = dict()
  for pName in pNames:
    paramDic[pName] = list()


  # Vectorize data
  datVec  = np.transpose(np.array([sum_data[pName] for pName in pNames]))
  datMin  = np.array([pRange[0] for pRange in pRanges])
  datMax  = np.array([pRange[1] for pRange in pRanges])
  datSpan = datMax-datMin


  # Exclude out of range samples
  if(nDim>0):
    inVec  = np.logical_and(np.all(datVec>datMin,axis=1),
                            np.all(datVec<datMax,axis=1))
    LLVec  = LLVec[inVec]
    datVec = datVec[inVec]


  # Copies of input/output 
  datVecExt = np.copy(datVec)
  LLVecSamp = np.copy(LLVec)


  # Bubble bobble
  while(nSampOpt > 0):

    # Apportion sample
    nsOpt = min(dimReq*nDim,nSampOpt)
    nSampOpt = nSampOpt - nsOpt

    # Attribute point density
    stillThinking = True
    while(stillThinking):
      # Choose best current point
      cPointOld = datVecExt[np.argmax(LLVecSamp),:]

      # No place left to optimize
      if(np.max(LLVecSamp)==ex_val):
        nSampRand = nSampRand + nSampOpt
        nSampOpt  = 0
        break

      # Calculate sample density around best point
      distVec  = np.linalg.norm((datVecExt-cPointOld)/datSpan,axis=1)
      localVec = datVecExt[(distVec<=radFrac),:]

      # Evaluate local point density
      if(localVec.shape[0] >= dimReq*nDim):
        # Sufficient point density; extrapolate
        A  = np.hstack((localVec/datSpan,np.ones((localVec.shape[0],1))))
        b  = LLVecSamp[(distVec<=radFrac)]
        x  = np.linalg.lstsq(A,b,rcond=None)[0][:-1]
        xN = 2.0*x/np.linalg.norm(x)
        cPointNew = cPointOld + xN*(radFrac*datSpan)

        # Create exclusion zone around old center
        LLVecSamp[(distVec<=radFrac)] = ex_val

        # Truncate target center
        cPointNew = np.maximum(cPointNew,datMin)
        cPointNew = np.minimum(cPointNew,datMax)

        # Calculate sample density around target center
        distVec  = np.linalg.norm((datVecExt-cPointNew)/datSpan,axis=1)
        localVec = datVecExt[(distVec<=radFrac),:]

        # Evaluate local point density
        if(localVec.shape[0] >= dimReq*nDim):
          # Already sampled; go somewhere else
          pass
        else:
          # Good target region
          stillThinking = False

      else:
        # Insufficient point density; no extrapolation
        cPointNew = cPointOld
        stillThinking = False

    #end-while

    # Sample locally
    optSamp = np.random.randn(nsOpt,nDim)
    optSamp = optSamp/np.linalg.norm(optSamp,axis=1)[:,None]
    optSamp = optSamp*np.power(np.random.rand(nsOpt,1),1.0/float(nDim))
    optSamp = optSamp*(datSpan*radFrac)
    optSamp = optSamp+cPointNew
 
    # Truncate local samples
    optSamp = np.maximum(optSamp,datMin)
    optSamp = np.minimum(optSamp,datMax)

    # Attach new samples
    datVecExt = np.vstack((datVecExt,optSamp))
    LLVecSamp = np.append(LLVecSamp, nsOpt*[ex_val])

    # Copy to output dictionary
    for k1 in range(nDim):
      paramDic[pNames[k1]].extend((optSamp[:,k1]).tolist())

  #end-nsOpt


  # Add some random global samples
  randSamp = np.random.rand(nSampRand,nDim)
  randSamp = randSamp*datSpan
  randSamp = randSamp+datMin


  # Copy to output dictionary
  for k1 in range(nDim):
    paramDic[pNames[k1]].extend((randSamp[:,k1]).tolist())


  # Return next parameter set
  return paramDic

#*******************************************************************************
