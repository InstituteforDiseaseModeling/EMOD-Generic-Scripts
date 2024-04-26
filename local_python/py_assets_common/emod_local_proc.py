# *****************************************************************************
#
# *****************************************************************************

import numpy as np

from py_assets_common.emod_constants import POP_AGE_DAYS, CLR_M, CLR_F

# *****************************************************************************

PYR_TLOCS = [-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12]
PYR_TLABS = [str(abs(val)) for val in PYR_TLOCS]

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
    tot_fem = np.transpose((np.diff(pyr_mat_avg, axis=0)/2.0 +
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


def pyr_chart(axs01, pop_dat, pop_dat_err, yr_lab):

    axs01.grid(visible=True, which='major', ls='-', lw=0.5, label='')
    axs01.grid(visible=True, which='minor', ls=':', lw=0.1)
    axs01.set_axisbelow(True)

    axs01.set_xlabel('Percentage', fontsize=14)
    axs01.set_ylabel('Age (yrs)', fontsize=14)

    pdat_yr = np.array(POP_AGE_DAYS)/365.0

    axs01.set_xlim(min(PYR_TLOCS), max(PYR_TLOCS))
    axs01.set_ylim(pdat_yr[0], pdat_yr[-1])

    axs01.set_xticks(ticks=PYR_TLOCS)
    axs01.set_xticklabels(PYR_TLABS)

    ydat = pdat_yr - 2.5
    tpop = np.sum(pop_dat)

    pop_dat_n = 100*pop_dat/tpop
    pop_dat_n_err = 100*pop_dat_err/tpop

    axs01.barh(ydat[1:], pop_dat_n/2.0, height=4.75,
               xerr=pop_dat_n_err, color=CLR_F)
    axs01.barh(ydat[1:], -pop_dat_n/2.0, height=4.75,
               xerr=pop_dat_n_err, color=CLR_M)

    tpop_str = 'Total Pop\n{:5.1f}M'.format(tpop/1e6)
    axs01.text(-11, 92.5, '{:04d}'.format(yr_lab), fontsize=18)
    axs01.text(5, 87.5, tpop_str, fontsize=18)

    return None

# *****************************************************************************
