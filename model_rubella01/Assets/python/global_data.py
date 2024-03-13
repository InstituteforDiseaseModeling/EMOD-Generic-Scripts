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

demog_object    = None

# Other stuff
first_call_bool = True

init_pop        = None

brate_mult_x    = None
brate_mult_y    = None

base_year       = 1900.0

#start_year      = 1980.0
#ri_offset       =   45.0
#run_years       =   90.0

start_year      = 2000.0
ri_offset       =   25.0
run_years       =   70.0



t_step_days     =    5.0

max_clock       =  180.0

#*******************************************************************************

