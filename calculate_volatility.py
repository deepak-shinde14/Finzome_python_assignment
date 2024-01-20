import pandas as pd
import numpy as np

# Load the data from the CSV file
file_path = 'C:/Users/shind/Downloads/NIFTY 50.csv'
data = pd.read_csv(file_path)

# Calculate Daily Returns
data['Daily Returns'] = (data['Close '] / data['Close '].shift(1)) - 1

# Calculate Daily Volatility
daily_volatility = np.std(data['Daily Returns'])

# Calculate Annualized Volatility
annualized_volatility = daily_volatility * np.sqrt(len(data))

# Print the results
print("Daily Volatility:", daily_volatility)
print("Annualized Volatility:", annualized_volatility)