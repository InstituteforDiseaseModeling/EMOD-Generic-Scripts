#********************************************************************************
#
# Static data module for embedded python in the DTK.
#
#********************************************************************************

# Control params
sim_index       = 0
var_params      = dict()
schema_path     = 'Assets/schema.json'

start_year      = 2006
start_time      =  365.0*(start_year-1900)
start_log       =  365.0*(2009-1900)
base_year       = 1900
check_abort     =  365.0*(2009-1900+0.5)

max_clock       =  240.0

# Filename params
demog_files     = list()
camp_file       = None
reports_file    = 'custom_dlls.json'

demog_dict      = dict()
demog_node      = dict()
demog_node_map  = dict()      # Zone:     [NodeIDs]

demog_object    = None
demog_min_pop   =  100

# Other stuff
first_call_bool = True
pass_abort      = False
prev_proc_time  =   -1.0
max_node_id     =    0

init_pop        =    0

data_vec_time   = None
data_vec_node   = None
data_vec_mcw    = None

brate_mult_list = list()

#*******************************************************************************

