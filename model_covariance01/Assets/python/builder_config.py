# *****************************************************************************
#
# Configuration file for simulation.
#
# *****************************************************************************

import global_data as gdata

import numpy as np

# *****************************************************************************


def update_config_obj(config):

    # Variables for this simulation
    RUN_NUM = gdata.var_params['run_number']
    TIME_DELTA = gdata.var_params['num_tsteps']

    R0 = gdata.var_params['R0']
    R0_VAR = gdata.var_params['R0_variance']

    CORR_ACQ_TRANS = gdata.var_params['correlation_acq_trans']

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
    inf_prd_mean = 8.0
    inf_ln_mean = R0/inf_prd_mean
    inf_ln_var = R0_VAR/inf_prd_mean/inf_prd_mean
    inf_ln_sig = np.sqrt(np.log(inf_ln_var/inf_ln_mean/inf_ln_mean+1.0))
    inf_ln_mu = np.log(inf_ln_mean) - 0.5*inf_ln_sig*inf_ln_sig

    cp.Base_Infectivity_Distribution = 'LOG_NORMAL_DISTRIBUTION'
    cp.Base_Infectivity_Log_Normal_Mu = inf_ln_mu
    cp.Base_Infectivity_Log_Normal_Sigma = inf_ln_sig

    cp.Incubation_Period_Distribution = 'GAUSSIAN_DISTRIBUTION'
    cp.Incubation_Period_Gaussian_Mean = 3.0
    cp.Incubation_Period_Gaussian_Std_Dev = 0.8

    cp.Infectious_Period_Distribution = 'GAUSSIAN_DISTRIBUTION'
    cp.Infectious_Period_Gaussian_Mean = inf_prd_mean
    cp.Infectious_Period_Gaussian_Std_Dev = 0.8

    cp.Enable_Disease_Mortality = 0

    cp.Acquisition_Transmission_Correlation = CORR_ACQ_TRANS

    # Immunity
    cp.Enable_Immunity = 1
    cp.Enable_Immune_Decay = 0

    cp.Post_Infection_Acquisition_Multiplier = 0.0
    cp.Post_Infection_Transmission_Multiplier = 0.0
    cp.Post_Infection_Mortality_Multiplier = 0.0

    # Interventions
    cp.Enable_Interventions = 1
    cp.Campaign_Filename = gdata.camp_file

    # Adapted sampling
    cp.Individual_Sampling_Type = 'TRACK_ALL'

    # Demographics
    cp.Enable_Demographics_Builtin = 0
    cp.Age_Initialization_Distribution_Type = 'DISTRIBUTION_OFF'
    cp.Enable_Vital_Dynamics = 0
    cp.Enable_Acquisition_Heterogeneity = 1
    cp.Demographics_Filenames = gdata.demog_files

    # Reporting
    cp.Enable_Default_Reporting = 1
    cp.Custom_Reports_Filename = gdata.reports_file

    return config

# *****************************************************************************
