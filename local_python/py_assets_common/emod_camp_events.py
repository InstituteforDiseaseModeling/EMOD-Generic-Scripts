# *****************************************************************************
#
# *****************************************************************************

from emod_api import schema_to_class as s2c
from emod_api.interventions import utils

from emod_constants import SPATH, YR_DAYS

# *****************************************************************************


def ce_import_pressure(node_list,
                       start_day=0.0, duration=1.0,
                       magnitude=1.0, age_yrs=40.0):

    # Import pressure
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SPATH)
    camp_iv = s2c.get_class_with_defaults('ImportPressure', SPATH)

    node_set = utils.do_nodes(SPATH, node_list)

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv

    camp_iv.Durations = [duration]
    camp_iv.Daily_Import_Pressures = [magnitude]
    camp_iv.Import_Age = age_yrs*YR_DAYS

    return camp_event

# *****************************************************************************


def ce_br_force(node_list, times, values,
                start_day=0.0):

    # Birth rate multiplier
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SPATH)
    camp_iv = s2c.get_class_with_defaults('NodeBirthRateMult', SPATH)

    node_set = utils.do_nodes(SPATH, node_list)

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv

    camp_iv.Multiplier_By_Duration.Times = times
    camp_iv.Multiplier_By_Duration.Values = values

    return camp_event

# *****************************************************************************


def ce_vax_AMT(node_list,
               start_day=0.0, only_group=None, coverage=1.0,
               acq_eff=0.0, mrt_eff=0.0, trn_eff=0.0):

    # Vaccine
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SPATH)
    camp_iv = s2c.get_class_with_defaults('Vaccine', SPATH)

    node_set = utils.do_nodes(SPATH, node_list)

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv

    if (only_group):
        camp_coord.Property_Restrictions_Within_Node = only_group

    camp_iv.Vaccine_Take = coverage
    camp_iv.Acquire_Config.Initial_Effect = acq_eff
    camp_iv.Mortality_Config.Initial_Effect = mrt_eff
    camp_iv.Transmit_Config.Initial_Effect = trn_eff

    return camp_event

# *****************************************************************************


def ce_quarantine(node_list, trigger,
                  start_day=0.0, coverage=1.0, delay=0.0, effect=0.0):

    CHWEC = 'CommunityHealthWorkerEventCoordinator'

    # Vaccine
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults(CHWEC, SPATH)
    camp_iv = s2c.get_class_with_defaults('Vaccine', SPATH)

    node_set = utils.do_nodes(SPATH, node_list)

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv
    camp_coord.Trigger_Condition_List = [trigger]
    camp_coord.Duration = 1000
    camp_coord.Waiting_Period = 1000
    camp_coord.Max_Distributed_Per_Day = 1e9
    camp_coord.Days_Between_Shipments = 1000
    camp_coord.Amount_In_Shipment = 0
    camp_coord.Initial_Amount_Distribution = 'CONSTANT_DISTRIBUTION'
    camp_coord.Initial_Amount_Constant = 1e9

    camp_iv.Vaccine_Take = coverage

    camp_iv.Transmit_Config.Initial_Effect = 1.0
    camp_iv.Transmit_Config.Durability_Map.Times = [0.0, delay]
    camp_iv.Transmit_Config.Durability_Map.Values = [0.0, effect]

    return camp_event

# *****************************************************************************


def ce_matrix_swap(node_list, prop_name, matrix,
                   start_day=0.0):

    # ChangeIPMatrix
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SPATH)
    camp_iv = s2c.get_class_with_defaults('ChangeIPMatrix', SPATH)

    node_set = utils.do_nodes(SPATH, node_list)

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv

    camp_iv.Property_Name = prop_name
    camp_iv.New_Matrix = matrix

    return camp_event

# *****************************************************************************


def ce_visit_nodes(node_orig, node_dest,
                   start_day=0.0, only_group=None, fraction=0.0, duration=1.0):

    # MigrateIndividuals
    camp_event = s2c.get_class_with_defaults('CampaignEvent', SPATH)
    camp_coord = s2c.get_class_with_defaults('StandardEventCoordinator', SPATH)
    camp_iv = s2c.get_class_with_defaults('MigrateIndividuals', SPATH)

    node_set = utils.do_nodes(SPATH, [node_orig])

    camp_event.Event_Coordinator_Config = camp_coord
    camp_event.Start_Day = start_day
    camp_event.Nodeset_Config = node_set

    camp_coord.Intervention_Config = camp_iv
    camp_coord.Demographic_Coverage = fraction

    if (only_group):
        camp_coord.Property_Restrictions_Within_Node = only_group

    camp_iv.NodeID_To_Migrate_To = node_orig
    camp_iv.Duration_Before_Leaving_Distribution = 'CONSTANT_DISTRIBUTION'
    camp_iv.Duration_Before_Leaving_Constant = 0
    camp_iv.Duration_At_Node_Distribution = 'CONSTANT_DISTRIBUTION'
    camp_iv.Duration_At_Node_Constant = duration

    return camp_event

# *****************************************************************************
