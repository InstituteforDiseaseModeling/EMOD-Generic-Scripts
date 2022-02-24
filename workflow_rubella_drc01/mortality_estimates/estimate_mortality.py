import numpy as np 
import pandas as pd

root_path = "C:\\Users\\helen\\OneDrive\\Desktop\\Stanford\\W22\\CME 217\\EMOD-Generic\\workflow_rubella_drc01"
un_estimates = root_path + "\\data\\UN_population\\population_estimates_by_age_both_sexes.xlsx"
un_projections = root_path + "\\data\\UN_population\\population_projections_by_age_both_sexes.xlsx"

# read in population data for years up to 2020
pop_df1 = pd.read_excel(un_estimates, sheet_name='ESTIMATES', header=16)

# clean column names
pop_df1.rename(columns={'Region, subregion, country or area *': 'Region', 'Reference date (as of 1 July)': 'Year'}, inplace=True)
drop_cols = ['Index', 'Variant', 'Notes', 'Country code', 'Type', 'Parent code']
pop_df1.drop(drop_cols, axis=1, inplace=True)

# filter to DRC
pop_df1 = pop_df1[pop_df1['Region'] == 'Democratic Republic of the Congo']

# set year as index
pop_df1.set_index('Year', inplace=True)

# get population data for years after 2020
pop_df2 = pd.read_excel(un_projections, sheet_name='Median', header=16)
pop_df2.rename(columns={'Region, subregion, country or area *': 'Region', 'Unnamed: 7': 'Year'}, inplace=True)
drop_cols = ['Index', 'Variant', 'Notes', 'Unnamed: 4', 'Type', 'Unnamed: 6']
pop_df2.drop(drop_cols, axis=1, inplace=True)
pop_df2 = pop_df2[pop_df2['Region'] == 'Democratic Republic of the Congo']
pop_df2.set_index('Year', inplace=True)
pop_df2.drop(2020, inplace=True) # this aligns between the two files

# combine population estimates and projections
pop_data = pd.concat([pop_df1, pop_df2], axis=0)

# calculating mortality rates
cols = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34',
       '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74',
       '75-79', '80-84', '85-89', '90-94', '95-99', '100+']

for i in range(len(cols)-1):
    age = cols[i]
    pop_in_5_yrs = pop_data[cols[i+1]].shift(-1)
    new_col = 'mort_' + age
    pop_data[new_col] = (pop_data[age] - pop_in_5_yrs)/(pop_data[age] * 365 *5) # mortality per day

mortality_data = pop_data[['mort_0-4','mort_5-9', 'mort_10-14', 
...                           'mort_15-19', 'mort_20-24', 'mort_25-29',
...                           'mort_30-34', 'mort_35-39', 'mort_40-44', 'mort_45-49', 'mort_50-54',
...                           'mort_55-59', 'mort_60-64', 'mort_65-69', 'mort_70-74', 'mort_75-79',
...                           'mort_80-84', 'mort_85-89', 'mort_90-94', 'mort_95-99']]

mortality_data.to_excel("mortality_rates_intermediate.xlsx")