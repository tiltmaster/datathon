import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
file = 'raw_data/unwto-all-data-download_112023.xlsx'

data_transport = pd.read_excel(file, sheet_name="Inbound Tourism-Transport")
data_accomodation = pd.read_excel(file, sheet_name="Inbound Tourism-Accommodation")