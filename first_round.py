import numpy as np
import pandas as pd
from dataprep.eda import create_report

file = 'raw_data/OECD.SDD.NAD.SEEA,DSD_AIR_TRANSPORT@DF_AIR_TRANSPORT,1.0+all.csv'

data = pd.read_csv(file)
#time period Observation value

# ['Time period', 'Observation value', 'OBS_STATUS', 'Observation status'],
excluded_from_list = ['Time period', 'Observation value', 'OBS_STATUS', 'Observation status']

data.drop(excluded_from_list, axis=1, inplace=True)


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
    reference_df = data[[code_column, name_column]].drop_duplicates()
    
    # Merge the reference DataFrame with your original DataFrame
    merged_df = pd.merge(data, reference_df, on=code_column, how='left')
    
    # Update the original DataFrame with the merged column
    data[code_column] = data[code_column].astype('category')

data['UNIT_MULT'] = data['UNIT_MULT'].replace([0, -999], np.nan)

create_report(data)
