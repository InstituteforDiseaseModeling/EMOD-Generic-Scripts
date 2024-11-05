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

demog_dict = dict()
demog_node = dict()
demog_min_pop = 50
demog_node_map = dict()      # LGA:     [NodeIDs]
demog_rep_index = dict()      # LGA:  Output row number

seed_inf_loc = 'AFRO:NIGERIA:KANO:KANO_MUNICIPAL'
seed_inf_t_off = 370.0
seed_inf_num = 100

inf_dur_mean = 24.0
inf_dur_std = 11.3

boxes_nopv2 = 2
boxes_sabin2 = 7
rev_nopv2 = 0.0
rev_sabin2 = 0.0
sia_coverage = 0.80

base_year = 1900.0
run_years = 2.0
t_step_days = 5.0

max_clock = 180.0

# *****************************************************************************
