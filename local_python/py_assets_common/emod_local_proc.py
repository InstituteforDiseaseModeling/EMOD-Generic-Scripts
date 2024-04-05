# *****************************************************************************
#
# *****************************************************************************

import numpy as np

# *****************************************************************************


def crs_proc(fert_file, XDAT, pyr_mat_avg, ss_demog=False):

    # Load UN WPP fertility distribution data
    fert_dat = np.loadtxt(fert_file, delimiter=',')
    fert_yr = fert_dat[0, :]
    fert_mat = fert_dat[1:, :]

    # Fertility distributions interpolated for years simulated
    fert_set = np.zeros((fert_mat.shape[0], XDAT.shape[0]))
    for k1 in range(fert_set.shape[0]):
        fert_set[k1, :] = np.interp(XDAT, fert_yr, fert_mat[k1, :])
    fert_set = fert_set/1000.0  # births/woman/year

    # Annual births implied by fertility distribution
    tot_fem = np.transpose((np.diff(pyr_mat_avg, axis=0)/2.0 + \
                            pyr_mat_avg[:-1, :])/2.0)
    fertopt = fert_set
    if (ss_demog):
        fertopt = fert_set[:, 0]
        fertopt = fertopt[:, np.newaxis]
    fert_births = np.sum(fertopt*tot_fem, axis=0)

    # Calculate CRS probabilities
    crs_prob_vec = np.ones(fertopt.shape)       # P = 1
    crs_prob_vec = crs_prob_vec * 0.5           # P(female)
    crs_prob_vec = crs_prob_vec * fertopt       # P(gave birth during year)
    crs_prob_vec = crs_prob_vec * 9.0/12.0      # P(pregnant during year)
    crs_prob_vec = crs_prob_vec * (0.85*13/39 + 0.50*13/39 + 0.50*4/39)
                                                # P(infection leads to CRS)

    return (fert_births, crs_prob_vec)

# *****************************************************************************
