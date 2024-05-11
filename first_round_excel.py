import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
file = 'raw_data/unwto-all-data-download_112023.xlsx'

data_excel = pd.read_excel(file, sheet_name="Inbound Tourism-Regions")

file = 'raw_data/OECD.SDD.NAD.SEEA,DSD_AIR_TRANSPORT@DF_AIR_TRANSPORT,1.0+all.csv'

data_csv = pd.read_csv(file)
excluded_from_list = ['Time period', 'Observation value', 'OBS_STATUS', 'Observation status']

data_csv.drop(excluded_from_list, axis=1, inplace=True)


columns_mapping = {
    'REF_AREA': 'Reference area',
    'FREQ' :'Frequency of observation',
    'MEASURE': 'Measure',
    'UNIT_MEASURE': 'Unit of measure',
    'ADJUSTMENT': 'Adjustment',
    'POLLUTANT': 'Pollutants',
    'FLIGHT_TYPE':'Flight type',
    'EMISSIONS_SOURCE':'Emissions source',
    'DECIMALS':'Decimals'
}

# Iterate over the columns and perform the operations
for code_column, name_column in columns_mapping.items():
    # Create a reference DataFrame for the current column
    reference_df = data_csv[[code_column, name_column]].drop_duplicates()
    
    # Merge the reference DataFrame with your original DataFrame
    merged_df = pd.merge(data_csv, reference_df, on=code_column, how='left')
    
    # Update the original DataFrame with the merged column
    data_csv[code_column] = data_csv[code_column].astype('category')

data_csv['UNIT_MULT'] = data_csv['UNIT_MULT'].replace([0, -999], np.nan)


combined_data = pd.concat([data_excel, data_csv])
print(combined_data.dtypes)