#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

import json

import numpy as np

#*******************************************************************************

# This script makes a json dictionary that is used by the pre-processing script
# in EMOD. Variable names defined here will be available to use in creating
# the input files. Please don't change the variable name for 'exp_name' or
# for 'num_sims' because those are also used in scripts outside of EMOD.

# The pre-process script will open the json dict created by this method. For
# everything in the 'EXP_VARIABLE' key, that script will assume a list and
# get a value from that list based on the sim index. For everything in the 
# 'EXP_CONSTANT' key, it will assume a single value and copy that value.



# ***** Setup *****
param_dict = dict()

param_dict['exp_name'] = 'ANG_Base_Age_UrbRur01'
param_dict['num_sims'] = 700
param_dict['EXP_VARIABLE'] = dict()
param_dict['EXP_CONSTANT'] = dict()

# Random number consistency
np.random.seed(4)

# Convenience naming
nsims = param_dict['num_sims']



# ***** Specify sim-variable parameters *****

param_dict['EXP_VARIABLE']['run_number']                   =   list(range(nsims))

param_dict['EXP_VARIABLE']['num_nodes']                    =  (np.random.choice([100,150,200,250], nsims)).tolist()


# ***** Constants for this experiment *****

param_dict['EXP_CONSTANT']['nTsteps']                      =          730

param_dict['EXP_CONSTANT']['ctext_val']                    =        'AFRO:ANG'

param_dict['EXP_CONSTANT']['totpop']                       =           1e6
param_dict['EXP_CONSTANT']['migration_coeff']              =          1e-3
param_dict['EXP_CONSTANT']['pop_power']                    =          1.00

param_dict['EXP_CONSTANT']['frac_rural']                   =          0.33

param_dict['EXP_CONSTANT']['age_effect_a']                 =          0.70
param_dict['EXP_CONSTANT']['age_effect_t']                 =          0.20


param_dict['EXP_CONSTANT']['R0']                           =          3.60


param_dict['EXP_CONSTANT']['trans_mat02']                  =  [1.00, 0.00, 0.50, 0.75]
param_dict['EXP_CONSTANT']['trans_mat03']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat04']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat05']                  =  [1.00, 0.00, 0.50, 0.90]

param_dict['EXP_CONSTANT']['trans_mat06']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat07']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat08']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat09']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat10']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat11']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat12']                  =  [1.00, 0.00, 0.50, 0.90]
param_dict['EXP_CONSTANT']['trans_mat13']                  =  [1.00, 0.00, 0.50, 0.90]

param_dict['EXP_CONSTANT']['start_day_trans_mat02']        =           75
param_dict['EXP_CONSTANT']['start_day_trans_mat03']        =          731
param_dict['EXP_CONSTANT']['start_day_trans_mat04']        =          731
param_dict['EXP_CONSTANT']['start_day_trans_mat05']        =          731

param_dict['EXP_CONSTANT']['start_day_trans_mat06']        =          731
param_dict['EXP_CONSTANT']['start_day_trans_mat07']        =          731+7
param_dict['EXP_CONSTANT']['start_day_trans_mat08']        =          731
param_dict['EXP_CONSTANT']['start_day_trans_mat09']        =          731+7
param_dict['EXP_CONSTANT']['start_day_trans_mat10']        =          731
param_dict['EXP_CONSTANT']['start_day_trans_mat11']        =          731+7
param_dict['EXP_CONSTANT']['start_day_trans_mat12']        =          731
param_dict['EXP_CONSTANT']['start_day_trans_mat13']        =          731+7

param_dict['EXP_CONSTANT']['spike_trans_mat02']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat03']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat04']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat05']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat06']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat07']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat08']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat09']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat10']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat11']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat12']            =          False
param_dict['EXP_CONSTANT']['spike_trans_mat13']            =          False

param_dict['EXP_CONSTANT']['nudge_trans_mat02']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat03']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat04']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat05']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat06']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat07']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat08']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat09']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat10']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat11']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat12']            =          False
param_dict['EXP_CONSTANT']['nudge_trans_mat13']            =          False

param_dict['EXP_CONSTANT']['household_sia02']              =          False
param_dict['EXP_CONSTANT']['household_sia03']              =          False
param_dict['EXP_CONSTANT']['household_sia04']              =          False
param_dict['EXP_CONSTANT']['household_sia05']              =          False
param_dict['EXP_CONSTANT']['household_sia06']              =          False
param_dict['EXP_CONSTANT']['household_sia07']              =          False
param_dict['EXP_CONSTANT']['household_sia08']              =          False
param_dict['EXP_CONSTANT']['household_sia09']              =          False
param_dict['EXP_CONSTANT']['household_sia10']              =          False
param_dict['EXP_CONSTANT']['household_sia11']              =          False
param_dict['EXP_CONSTANT']['household_sia12']              =          False
param_dict['EXP_CONSTANT']['household_sia13']              =          False

param_dict['EXP_CONSTANT']['HCW_PPE']                      =          0.95

param_dict['EXP_CONSTANT']['HCW_Walk']                     =          False
param_dict['EXP_CONSTANT']['HCW_Walk_Start']               =          160
param_dict['EXP_CONSTANT']['HCW_Walk_End']                 =          200

param_dict['EXP_CONSTANT']['Bob_Walk']                     =          False
param_dict['EXP_CONSTANT']['Bob_Frac']                     =            0.0007
param_dict['EXP_CONSTANT']['Bob_Walk_Start']               =          160
param_dict['EXP_CONSTANT']['Bob_Walk_End']                 =          200

param_dict['EXP_CONSTANT']['importations_start_day']       =           60
param_dict['EXP_CONSTANT']['importations_daily_rate']      =            1.2
param_dict['EXP_CONSTANT']['importations_duration']        =          365

param_dict['EXP_CONSTANT']['self_isolate_on_symp_frac']    =            0.1
param_dict['EXP_CONSTANT']['self_isolate_effectiveness']   =            0.8

param_dict['EXP_CONSTANT']['active_finding_start_day']     =          731
param_dict['EXP_CONSTANT']['active_finding_coverage']      =            0.0
param_dict['EXP_CONSTANT']['active_finding_effectiveness'] =            0.9
param_dict['EXP_CONSTANT']['active_finding_delay']         =            0.00



# ***** Write parameter dictionary *****

with open('param_dict.json','w') as fid01:
  json.dump(param_dict,fid01)



#*******************************************************************************
