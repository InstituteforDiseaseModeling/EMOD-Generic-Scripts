# *****************************************************************************
#
# Configuration file for simulation.
#
# *****************************************************************************

import global_data as gdata

# *****************************************************************************


def update_config_obj(config):

    # Variables for this simulation
    RUN_NUM = gdata.var_params['run_number']
    TIME_DELTA = gdata.var_params['num_tsteps']

    NET_INF_COEF = gdata.var_params['net_coef']
    NET_INF_DPOW = gdata.var_params['net_exp']
    MAX_FRAC = gdata.var_params['max_export']
    MIN_CONNECT = gdata.var_params['min_connect']

    # Config parameters object (read only dictionary)
    cp = config.parameters

    # Random number seed
    cp.Run_Number = RUN_NUM

    # Time
    cp.Start_Time = 0.0
    cp.Simulation_Duration = TIME_DELTA

    cp.Enable_Termination_On_Zero_Total_Infectivity = 1
    cp.Minimum_End_Time = 50.0

    # Intrahost
    cp.Base_Infectivity_Distribution = 'CONSTANT_DISTRIBUTION'
    cp.Base_Infectivity_Constant = 0.5

    cp.Incubation_Period_Distribution = 'CONSTANT_DISTRIBUTION'
    cp.Incubation_Period_Constant = 3.0

    cp.Infectious_Period_Distribution = 'CONSTANT_DISTRIBUTION'
    cp.Infectious_Period_Constant = 3.0

    config.parameters.Enable_Disease_Mortality = 0

    # Interventions
    cp.Enable_Network_Infectivity = 1
    cp.Network_Infectivity_Max_Export_Frac = MAX_FRAC
    cp.Network_Infectivity_Min_Connection = MIN_CONNECT

    cp.Network_Infectivity_Coefficient = [NET_INF_COEF]
    cp.Network_Infectivity_Exponent = [NET_INF_DPOW]

    # Immunity
    cp.Enable_Immunity = 1
    cp.Enable_Immune_Decay = 0

    cp.Post_Infection_Acquisition_Multiplier = 0.0
    cp.Post_Infection_Transmission_Multiplier = 0.0
    cp.Post_Infection_Mortality_Multiplier = 0.0

    # Interventions *****
    cp.Enable_Interventions = 1
    cp.Campaign_Filename = gdata.camp_file

    # Adapted sampling
    cp.Individual_Sampling_Type = 'TRACK_ALL'

    # Demographic parameters
    cp.Enable_Demographics_Builtin = 1

    cp.Default_Geography_Initial_Node_Population = 1000
    cp.Default_Geography_Torus_Size = 25

    cp.Enable_Vital_Dynamics = 0

    # Reporting
    cp.Enable_Default_Reporting = 1
    cp.Enable_Spatial_Output = 1
    cp.Spatial_Output_Channels = ["New_Infections"]
    cp.Custom_Reports_Filename = gdata.reports_file

    return config

# *****************************************************************************
