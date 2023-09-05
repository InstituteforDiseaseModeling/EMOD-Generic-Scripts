#********************************************************************************
#
# Static data module for embedded python in the DTK.
#
#********************************************************************************

# Control params
sim_index       = None
var_params      = dict()
schema_path     = 'Assets/schema.json'

# Filename params
demog_files     = list()
camp_file       = None
reports_file    = 'custom_dlls.json'

demog_dict      = dict()
demog_node      = dict()
demog_node_map  = dict()      # LGA:     [NodeIDs]
demog_object    = None
demog_min_pop   =  50
demog_use_10km  = False

# Other stuff
first_call_bool = True
prev_proc_time  = -1.0
max_node_id     = 0

data_vec_time   = None
data_vec_node   = None
data_vec_mcw    = None

adm01_list      = None
nobs_vec        = None

base_year       = 1900.0
start_year      = 2010.0
start_log       = 2016.0

max_clock       =  180.0

#*******************************************************************************

