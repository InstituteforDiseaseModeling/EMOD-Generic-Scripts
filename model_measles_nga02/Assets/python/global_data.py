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
reports_file    = None

demog_object    = None
demog_min_pop   =    1

# Other stuff
first_call_bool = True

init_pop        = None

brate_mult_x    = None
brate_mult_y    = None

start_log       = 365.0*(2015-1900)

base_year       = 1900.0
start_year      = 2015.0
max_clock       =  180.0

#*******************************************************************************

