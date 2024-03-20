# *****************************************************************************
#
# Static data module for embedded python.
#
# *****************************************************************************

# Control params
sim_index = 0
var_params = dict()
schema_path = 'Assets/schema.json'

# Filename params
demog_files = list()
camp_file = 'campaign.json'
reports_file = 'custom_dlls.json'

demog_object = None

# Other stuff
first_call_bool = True

init_pop = None

brate_mult_x = None
brate_mult_y = None

base_year = 1900.0
max_clock = 180.0
t_step_days = 5.0

# *****************************************************************************
