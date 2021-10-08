#********************************************************************************
#
# Python 3.6.0
#
#********************************************************************************

# Control params
sim_index       = 0
var_params      = dict()
schema_path     = 'Assets/schema.json'

# Filename params
demog_files     = ['demographics.json']
camp_file       = None
reports_file    = None

start_off       = 120.0
demog_dict      = dict()
demog_node      = dict()
demog_min_pop   = 0
demog_node_map  = dict()      # LGA:     [NodeIDs]
demog_rep_index = dict()      # LGA:  Output row number
demog_object    = None

# Other stuff
first_call_bool = True

#*******************************************************************************

