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
    R0 = gdata.var_params['R0']
    RUN_NUM = gdata.var_params['run_number']
    TIME_DELTA = gdata.var_params['nTsteps']

    # Config parameters object (read only dictionary)
    cp = config.parameters

    # Random number seed
    cp.Run_Number = RUN_NUM

    # Time
    cp.Start_Time = 365.0*(2020-1900)+1
    cp.Simulation_Duration = TIME_DELTA

    # Intrahost
    inf_prd_mean = 8.0
    inf_prd_scale = 4.0
    cp.Base_Infectivity_Distribution = 'EXPONENTIAL_DISTRIBUTION'
    cp.Base_Infectivity_Exponential = R0/inf_prd_mean

    cp.Incubation_Period_Distribution = 'GAUSSIAN_DISTRIBUTION'
    cp.Incubation_Period_Gaussian_Mean = 4.0
    cp.Incubation_Period_Gaussian_Std_Dev = 1.0

    cp.Infectious_Period_Distribution = 'GAMMA_DISTRIBUTION'
    cp.Infectious_Period_Shape = inf_prd_mean/inf_prd_scale
    cp.Infectious_Period_Scale = inf_prd_scale

    cp.Symptomatic_Infectious_Offset = 2.0
    cp.Enable_Disease_Mortality = 0

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
    cp.Individual_Sampling_Type = 'ADAPTED_SAMPLING_BY_IMMUNE_STATE'
    cp.Base_Individual_Sample_Rate = 1.0
    cp.Relative_Sample_Rate_Immune = 0.1
    cp.Immune_Threshold_For_Downsampling = 1.0e-5
    cp.Immune_Downsample_Min_Age = 0.0

    # Demographic parameters
    cp.Enable_Demographics_Builtin = 0

    cp.Age_Initialization_Distribution_Type = 'DISTRIBUTION_OFF'
    cp.Enable_Vital_Dynamics = 0
    cp.Enable_Infection_Rate_Overdispersion = 1
    cp.Demographics_Filenames = gdata.demog_files

    cp.Enable_Heterogeneous_Intranode_Transmission = 1

    # Migration / Spatial parameters
    cp.Migration_Model = 'FIXED_RATE_MIGRATION'
    cp.Migration_Pattern = 'SINGLE_ROUND_TRIPS'
    cp.Enable_Regional_Migration = 1
    cp.Regional_Migration_Filename = 'regional_migration.bin'
    cp.Regional_Migration_Roundtrip_Duration = 0.01
    cp.Regional_Migration_Roundtrip_Probability = 1.0

    # Reporting
    cp.Enable_Default_Reporting = 1
    cp.Enable_Property_Output = 1
    cp.Custom_Reports_Filename = REPORTS_FILE

    return config

# *****************************************************************************
