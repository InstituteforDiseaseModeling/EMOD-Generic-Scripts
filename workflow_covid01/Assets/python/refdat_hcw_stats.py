#********************************************************************************
#
# Supporting data for file construction
#
# Python 3.6.0
#
#********************************************************************************


#********************************************************************************

def hcw_stats_fun(arg_key=str()):

  narg_key1 = arg_key
  while(len(narg_key1) > 0 and narg_key1 not in age_pyr_hcw):
    narg_key1 = narg_key1.rsplit(':',1)[0]

  narg_key2 = arg_key
  while(len(narg_key2) > 0 and narg_key2 not in tot_frk_hcw):
    narg_key2 = narg_key2.rsplit(':',1)[0]

  narg_key3 = arg_key
  while(len(narg_key3) > 0 and narg_key3 not in wrk_cts_hcw):
    narg_key3 = narg_key3.rsplit(':',1)[0]

  return(age_pyr_hcw[narg_key1],
         tot_frk_hcw[narg_key2],
         wrk_cts_hcw[narg_key3])

#end-hcw_stats_fun

#********************************************************************************

age_pyr_hcw = dict()
tot_frk_hcw = dict()
wrk_cts_hcw = dict()


age_pyr_hcw['AFRO:ANG'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

# World Bank Report No. 66218; Box 1.6; based on 29k total HCW
age_pyr_hcw['AFRO:ETH'] = \
    [0.00000,0.00000,0.00000,0.00000,0.28463,0.23440,0.14733,0.12466,
     0.08275,0.06928,0.03042,0.02390,0.00148,0.00115,0.00000,0.00000]

age_pyr_hcw['EMRO:PAK'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

age_pyr_hcw['EURO:UKR'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

age_pyr_hcw['EURO:ITA'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

age_pyr_hcw['PAHO:ECU'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

age_pyr_hcw['SEARO:IND'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

age_pyr_hcw['SEARO:NPL'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]

age_pyr_hcw['WPRO:LAO'] = \
    [0.00000,0.00000,0.00000,0.00000,0.20000,0.20000,0.15000,0.15000,
     0.10000,0.10000,0.05000,0.05000,0.00000,0.00000,0.00000,0.00000]


tot_frk_hcw['AFRO:ANG']  = 0.001
tot_frk_hcw['AFRO:ETH']  = 0.001
tot_frk_hcw['EMRO:PAK']  = 0.001
tot_frk_hcw['EURO:UKR']  = 0.001
tot_frk_hcw['EURO:ITA']  = 0.001
tot_frk_hcw['PAHO:ECU']  = 0.001
tot_frk_hcw['SEARO:IND'] = 0.001
tot_frk_hcw['SEARO:NPL'] = 0.001
tot_frk_hcw['WPRO:LAO']  = 0.001


wrk_cts_hcw['AFRO:ANG'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

# BMCResNote 2019 v12 e239; Table 1; based on hospitalization rates
wrk_cts_hcw['AFRO:ETH'] = \
    [0.00126,0.00126,0.06658,0.06658,0.14824,0.14824,0.09548,0.09548,
     0.09421,0.09421,0.03141,0.03141,0.03141,0.03141,0.03141,0.03141]

wrk_cts_hcw['EMRO:PAK'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

wrk_cts_hcw['EURO:UKR'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

wrk_cts_hcw['EURO:ITA'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

wrk_cts_hcw['PAHO:ECU'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

wrk_cts_hcw['SEARO:IND'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

wrk_cts_hcw['SEARO:NPL'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

wrk_cts_hcw['WPRO:LAO'] = \
    [0.01000,0.01000,0.05000,0.05000,0.15000,0.15000,0.10000,0.10000,
     0.10000,0.10000,0.03000,0.03000,0.03000,0.03000,0.03000,0.03000]

#********************************************************************************
