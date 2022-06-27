#********************************************************************************
#
# Static data module for embedded python in the DTK.
#
#********************************************************************************

# Control params
sim_index       = 0
var_params      = dict()
schema_path     = 'Assets/schema.json'

start_time      = 365.0*(2008-1900)
start_log       = 365.0*(2011-1900)
base_year       = 1900

# Filename params
demog_files     = list()
camp_file       = None
reports_file    = None

demog_dict      = dict()
demog_node      = dict()
demog_node_map  = dict()      # LGA:     [NodeIDs]
demog_rep_index = dict()      # LGA:  Output row number
demog_object    = None
demog_min_pop   =  50

# Other stuff
first_call_bool = True
prev_proc_time  = -1.0
max_node_id     = 0

data_vec_time   = None
data_vec_node   = None
data_vec_mcw    = None

adm01_list      = None
nobs_vec        = None

#*******************************************************************************

