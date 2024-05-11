import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
file = 'raw_data/OECD.SDD.NAD.SEEA,DSD_AIR_TRANSPORT@DF_AIR_TRANSPORT,1.0+all.csv'

data = pd.read_csv(file)
#time period Observation value

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
# Calculate the count of each category in the REF_AREA column
ref_area_counts = data['REF_AREA'].value_counts()

# Select the top 20 categories based on their count
top_20_ref_areas = ref_area_counts.nlargest(30).index

# Filter the data to include only the observations corresponding to the top 20 categories
data_top_20 = data[data['REF_AREA'].isin(top_20_ref_areas)]

# Create the countplot for the top 20 categories
plt.figure(figsize=(12, 8))  # Adjust figure size if needed
sns.countplot(data=data_top_20, x='REF_AREA', order=top_20_ref_areas)

# Add title and axis labels
plt.title('Number of Observations by Top 20 Reference Areas')
plt.xlabel('Reference area')
plt.ylabel('Count')

plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.savefig('graphs/observation_areas.png', dpi=300) 

plt.figure(figsize=(8, 6))
sns.countplot(data=data, x='Frequency of observation')

# Add title and axis labels
plt.title('Count of Frequency')
plt.xlabel('Frequency Category')
plt.ylabel('Count')

# Show the plot
plt.tight_layout()
plt.savefig('graphs/frequency.png', dpi=300) 

plt.figure(figsize=(8, 6))
sns.countplot(data=data, x='Flight type')

# Add title and axis labels
plt.title('Count of Flight Types')
plt.xlabel('Flight Types')
plt.ylabel('Count')

# Show the plot
plt.tight_layout()
plt.savefig('graphs/flight_types.png', dpi=300) 

data['TIME_PERIOD'] = pd.to_datetime(data['TIME_PERIOD'])

# Create the line plot
plt.figure(figsize=(12, 8))
sns.lineplot(data=data, x='TIME_PERIOD', y='Reference area')

# Add title and axis labels
plt.title('Number of Observations by Reference Area Over Time')
plt.xlabel('Time Period')
plt.ylabel('Count of Observations')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.savefig('graphs/time_period.png', dpi=300)  # Adjust file name and dpi if needed

