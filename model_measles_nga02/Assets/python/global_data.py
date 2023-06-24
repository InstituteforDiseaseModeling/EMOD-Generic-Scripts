#********************************************************************************
#
# Static data module for embedded python in the DTK.
#
#********************************************************************************

# Control params
sim_index       = None
var_params      = dict()
schema_path     = 'Assets/schema.json'

start_year      = 2015.0
start_log       =  365.0*(2015-1900)
base_year       = 1900.0

max_clock       =  180.0

# Filename params
demog_files     = list()
camp_file       = None
reports_file    = 'custom_dlls.json'

demog_object    = None
demog_min_pop   =    1

# Other stuff
first_call_bool = True

init_pop        =    0

brate_mult_x    = None
brate_mult_y    = None

#*******************************************************************************

