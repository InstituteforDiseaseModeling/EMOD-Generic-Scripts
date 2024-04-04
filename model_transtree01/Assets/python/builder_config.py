# *****************************************************************************
#
# Configuration file for simulation.
#
# *****************************************************************************

import global_data as gdata

from emod_constants import CAMP_FILE, REPORTS_FILE

# *****************************************************************************


def update_config_obj(config):

    # Variables for this simulation
    RUN_NUM = gdata.var_params['run_number']
    TIME_DELTA = gdata.var_params['num_tsteps']
    BI_STD = gdata.var_params['base_inf_stddev_mult']

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
    if (BI_STD > 0.01):
        cp.Base_Infectivity_Distribution = 'GAMMA_DISTRIBUTION'
        cp.Base_Infectivity_Scale = 0.5*BI_STD*BI_STD
        cp.Base_Infectivity_Shape = 1.0/BI_STD/BI_STD
    else:
        cp.Base_Infectivity_Distribution = 'CONSTANT_DISTRIBUTION'
        cp.Base_Infectivity_Constant = 0.5

    cp.Incubation_Period_Distribution = 'GAUSSIAN_DISTRIBUTION'
    cp.Incubation_Period_Gaussian_Mean = 3.0
    cp.Incubation_Period_Gaussian_Std_Dev = 1.0

    cp.Infectious_Period_Distribution = 'GAUSSIAN_DISTRIBUTION'
    cp.Infectious_Period_Gaussian_Mean = 3.0
    cp.Infectious_Period_Gaussian_Std_Dev = 1.0

    cp.Enable_Disease_Mortality = 0

    # Strain Tracking
    cp.Enable_Strain_Tracking = 1
    cp.Enable_Label_By_Infector = 1

    # Interventions
    cp.Enable_Network_Infectivity = 1
    cp.Network_Infectivity_Coefficient = [1.0]
    cp.Network_Infectivity_Exponent = [0.0]

    # Immunity
    cp.Enable_Immunity = 1
    cp.Enable_Immune_Decay = 0

    cp.Post_Infection_Acquisition_Multiplier = 0.0
    cp.Post_Infection_Transmission_Multiplier = 0.0
    cp.Post_Infection_Mortality_Multiplier = 0.0

    # Interventions
    cp.Enable_Interventions = 1
    cp.Campaign_Filename = CAMP_FILE

    # Adapted sampling
    cp.Individual_Sampling_Type = 'TRACK_ALL'

    # Demographic parameters
    cp.Enable_Demographics_Builtin = 1

    cp.Default_Geography_Initial_Node_Population = 312
    cp.Default_Geography_Torus_Size = 4

    cp.Enable_Vital_Dynamics = 0

    # Reporting
    cp.Enable_Default_Reporting = 1
    cp.Enable_Event_DB = 1
    cp.SQL_Events = ["NewInfection"]

    cp.Custom_Reports_Filename = REPORTS_FILE

    return config

# *****************************************************************************
