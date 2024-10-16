# *****************************************************************************

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join('..', 'refdat_namesets'))
from aux_namematch import reprule, tlc_dict

# *****************************************************************************


def make_pop_dat(TLC=''):

    # Parse CSVs
    wppf1 = 'WPP2022_POP_F02_1_POPULATION_BY_AGE_BOTH_SEXES_ESTIMATES.csv'
    with open(wppf1, errors='ignore') as fid01:
        flines_rev = [val.strip().split(',') for val in fid01.readlines()]

    wppf2 = 'WPP2022_POP_F02_1_POPULATION_BY_AGE_BOTH_SEXES_MEDIUM_VARIANT.csv'
    with open(wppf2, errors='ignore') as fid01:
        flines_fwd = [val.strip().split(',') for val in fid01.readlines()]

    # Construct output data structure
    pop_dat = np.zeros((0, 22), dtype=int)

    # Add values from retrospective estimates
    for row_val in flines_rev:
        if (reprule(row_val[2]) == tlc_dict[TLC]):
            year_val = int(row_val[10])
            if (year_val % 5):
                continue
            bin_pops = [int(1000*float(row_val[idx].replace(' ', ''))) for idx in range(11, 32)]
            pop_dat = np.vstack((pop_dat, np.array([year_val]+bin_pops)))

    # Add values from forward projections
    for row_val in flines_fwd:
        if (reprule(row_val[2]) == tlc_dict[TLC]):
            year_val = int(row_val[10])
            if (year_val % 5):
                continue
            if (year_val == pop_dat[-1, 0]):
                continue
            bin_pops = [int(1000*float(row_val[idx].replace(' ', ''))) for idx in range(11, 32)]
            pop_dat = np.vstack((pop_dat, np.array([year_val]+bin_pops)))

    # Write data files
    ofile_name = 'pop_dat_{:s}.csv'.format(TLC)
    np.savetxt(ofile_name, pop_dat.T, fmt='%d', delimiter=',')

# *****************************************************************************


if (__name__ == "__main__"):

    make_pop_dat('COD')

# *****************************************************************************
