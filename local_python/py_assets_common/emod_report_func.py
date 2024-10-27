# *****************************************************************************
#
# *****************************************************************************


from emod_constants import RST_FILE

# *****************************************************************************


def report_strain(report_dict):

    rst_str = RST_FILE.split('.')[0]

    report_dict['Custom_Reports'][rst_str] = {'Enabled': 1,
                                              'Reports': list()}

    repDic = {'Report_Name': RST_FILE}

    report_dict['Custom_Reports'][rst_str]['Reports'].append(repDic)

    return None

# *****************************************************************************
