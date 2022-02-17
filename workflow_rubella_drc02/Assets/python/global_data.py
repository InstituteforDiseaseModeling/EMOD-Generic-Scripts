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

demog_object    = None

# Other stuff
first_call_bool = True

brate_mult_x    = None
brate_mult_y    = None

start_time      = 365.0*(2000-1900)
max_clock       = 180.0

#*******************************************************************************

