#********************************************************************************
#
# Static data module for embedded python in the DTK.
#
#********************************************************************************

# Control params
sim_index       = 0
var_params      = dict()
schema_path     = 'Assets/schema.json'

# Filename params
demog_files     = list()
camp_file       = None
reports_file    = None

demog_dict      = dict()
demog_node      = dict()
demog_min_pop   = 0
demog_node_map  = dict()      # LGA:     [NodeIDs]
demog_rep_index = dict()      # LGA:  Output row number
demog_object    = None

max_node_id     = 0

# Other stuff
first_call_bool = True
prev_proc_time  = -1.0

data_vec_time   = None
data_vec_node   = None
data_vec_mcw    = None

adm01_list      = None
nobs_vec        = None

#*******************************************************************************

