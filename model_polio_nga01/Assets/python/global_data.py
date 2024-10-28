# *****************************************************************************
#
# Static data module for embedded python.
#
# *****************************************************************************

# Control params
sim_index = 0
var_params = dict()

# Filename params
demog_files = list()

demog_object = None

# Other stuff
first_call_bool = True



start_off = 365.0*(2016-1900)+120.0
demog_dict = dict()
demog_node = dict()
demog_min_pop = 0
demog_node_map = dict()      # LGA:     [NodeIDs]
demog_rep_index = dict()      # LGA:  Output row number
schema_path = 'Assets/schema.json'



boxes_nopv2 = 2
boxes_sabin2 = 7
rev_nopv2 = 0.0
rev_sabin2 = 0.0

run_years = 2.0
t_step_days = 1.0

max_clock = 180.0

# *****************************************************************************
