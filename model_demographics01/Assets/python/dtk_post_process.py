#********************************************************************************
#
#********************************************************************************

import os, sys, json

import global_data as gdata

import numpy as np

#********************************************************************************

pop_age_days = [     0,   1825,   3650,   5475,   7300,   9125,  10950,  12775,
                 14600,  16425,  18250,  20075,  21900,  23725,  25550,  27375,
                 29200,  31025,  32850,  34675,  36500]

uk_1950_frac = [0.0000, 0.0863, 0.0719, 0.0663, 0.0631, 0.0680, 0.0768, 0.0691,
                0.0769, 0.0766, 0.0713, 0.0625, 0.0546, 0.0482, 0.0410, 0.0319,
                0.0206, 0.0103, 0.0036, 0.0008, 0.0001]

uk_1960_frac = [0.0000, 0.0783, 0.0718, 0.0814, 0.0693, 0.0632, 0.0627, 0.0653,
                0.0716, 0.0644, 0.0703, 0.0688, 0.0631, 0.0519, 0.0423, 0.0330,
                0.0228, 0.0131, 0.0050, 0.0012, 0.0002]

uk_1970_frac = [0.0000, 0.0839, 0.0849, 0.0729, 0.0683, 0.0763, 0.0641, 0.0592,
                0.0580, 0.0606, 0.0655, 0.0572, 0.0613, 0.0576, 0.0485, 0.0353,
                0.0239, 0.0142, 0.0063, 0.0018, 0.0003]

uk_1980_frac = [0.0000, 0.0602, 0.0687, 0.0814, 0.0843, 0.0729, 0.0673, 0.0740,
                0.0617, 0.0570, 0.0556, 0.0572, 0.0600, 0.0503, 0.0504, 0.0423,
                0.0298, 0.0166, 0.0075, 0.0024, 0.0004]

tpop_xval = [     0.0,      1.0,      2.0,      3.0,      4.0,      5.0,
                  6.0,      7.0,      8.0,      9.0,     10.0,     11.0,
                 12.0,     13.0,     14.0,     15.0,     16.0,     17.0,
                 18.0,     19.0,     20.0,     21.0,     22.0,     23.0,
                 24.0,     25.0,     26.0,     27.0,     28.0,     29.0,
                 30.0]

tpop_yval = [50616014, 50601935, 50651280, 50750976, 50890915, 51063902,
             51265880, 51495702, 51754673, 52045662, 52370602, 52727768,
             53109399, 53500716, 53882751, 54240850, 54568868, 54866534,
             55132596, 55367947, 55573453, 55748531, 55892418, 56006296,
             56092066, 56152333, 56188348, 56203595, 56205913, 56205083,
             56209171]

#********************************************************************************

def application(output_path):

  SIM_IDX       = gdata.sim_index

  # ***** Get variables for this simulation *****
  TIME_DELTA     = gdata.var_params['num_tsteps']


  # Prep output dictionary
  key_str    = '{:05d}'.format(SIM_IDX)
  parsed_dat = {key_str: dict()}


  # Sample population pyramid every year
  with open(os.path.join(output_path,'DemographicsSummary.json')) as fid01:
    demog_output = json.load(fid01)

  age_key_list = [   '<5',   '5-9', '10-14', '15-19', '20-24', '25-29',
                  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
                  '60-64', '65-69', '70-74', '75-79', '80-84', '85-89',
                  '90-94', '95-99']
  pyr_dat      = np.zeros((int(np.floor(TIME_DELTA/365.0))+1,len(age_key_list)))

  for k1 in range(len(age_key_list)):
    age_key_str = 'Population Age {:s}'.format(age_key_list[k1])
    age_vec_dat = np.array(demog_output['Channels'][age_key_str]['Data'])
    pyr_dat[0,  k1] = age_vec_dat[0]
    pyr_dat[1:, k1] = age_vec_dat[364::365]

  parsed_dat[key_str]['pyr_dat'] = pyr_dat.tolist()


  # Calculate calibration score
  err_score = 0

  global tpop_yval
  sim_pop     = np.sum(pyr_dat, axis=1)
  ref_pop     = 100000*np.array(tpop_yval)/tpop_yval[0]
  err_score   = err_score + np.sqrt(np.sum(np.power(100*(sim_pop-ref_pop)/ref_pop,2.0)))

  global uk_1950_frac
  simpyr1950  = pyr_dat[ 0,:]/np.sum(pyr_dat[ 0,:])
  refpyr1950  = np.array(uk_1950_frac[1:])
  err_score   = err_score + np.sqrt(np.sum(np.power(100*(simpyr1950-refpyr1950),2.0)))

  global uk_1960_frac
  simpyr1960  = pyr_dat[10,:]/np.sum(pyr_dat[10,:])
  refpyr1960  = np.array(uk_1960_frac[1:])
  err_score   = err_score + np.sqrt(np.sum(np.power(100*(simpyr1960-refpyr1960),2.0)))

  global uk_1970_frac
  simpyr1970  = pyr_dat[20,:]/np.sum(pyr_dat[20,:])
  refpyr1970  = np.array(uk_1970_frac[1:])
  err_score   = err_score + np.sqrt(np.sum(np.power(100*(simpyr1970-refpyr1970),2.0)))

  global uk_1980_frac
  simpyr1980  = pyr_dat[30,:]/np.sum(pyr_dat[30,:])
  refpyr1980  = np.array(uk_1980_frac[1:])
  err_score   = err_score + np.sqrt(np.sum(np.power(100*(simpyr1980-refpyr1980),2.0)))

  parsed_dat[key_str]['cal_val'] = -float(err_score)


  # Write output dictionary
  with open('parsed_out.json','w') as fid01:
    json.dump(parsed_dat, fid01)


  return None

#*******************************************************************************
