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
    INIT_AGENT = gdata.var_params['num_agents']

    # Config parameters object (read only dictionary)
    cp = config.parameters

    # Random number seed
    cp.Run_Number = RUN_NUM

    # Time
    cp.Start_Time = 365.0*(gdata.start_year-gdata.base_year)
    cp.Simulation_Duration = 365.0*gdata.run_years
    cp.Simulation_Timestep = gdata.t_step_days

    # Intrahost
    cp.Base_Infectivity_Distribution = 'CONSTANT_DISTRIBUTION'
    cp.Base_Infectivity_Constant = 0.0

    cp.Incubation_Period_Distribution = 'CONSTANT_DISTRIBUTION'
    cp.Incubation_Period_Constant = 0.0

    cp.Infectious_Period_Distribution = 'CONSTANT_DISTRIBUTION'
    cp.Infectious_Period_Constant = 0.0

    cp.Enable_Disease_Mortality = 0

    # Immunity
    cp.Enable_Immunity = 0

    # Interventions
    cp.Enable_Interventions = 1
    cp.Campaign_Filename = CAMP_FILE

    # Adapted sampling
    cp.Individual_Sampling_Type = 'FIXED_SAMPLING'
    cp.Base_Individual_Sample_Rate = INIT_AGENT/gdata.init_pop

    # Demographic parameters
    cp.Enable_Demographics_Builtin = 0
    cp.Enable_Vital_Dynamics = 1
    cp.Enable_Birth = 1
    cp.Birth_Rate_Dependence = 'POPULATION_DEP_RATE'
    cp.Enable_Aging = 1
    cp.Age_Initialization_Distribution_Type = 'DISTRIBUTION_COMPLEX'
    cp.Enable_Natural_Mortality = 1
    enum_str = 'NONDISEASE_MORTALITY_BY_YEAR_AND_AGE_FOR_EACH_GENDER'
    cp.Death_Rate_Dependence = enum_str

    cp.Demographics_Filenames = gdata.demog_files

    # Reporting
    cp.Enable_Default_Reporting = 1
    cp.Enable_Demographics_Reporting = 1
    cp.Custom_Reports_Filename = REPORTS_FILE

    return config

# *****************************************************************************
