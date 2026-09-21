import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. Connect to MySQL (Replace with your password!)
engine = create_engine('mysql+pymysql://root:Arman2005#@localhost:3306/supply_chain')

query = "SELECT date, units_sold FROM inventory_data WHERE product_id = 'P0016' ORDER BY date;"
df = pd.read_sql(query, con=engine)
df.set_index('date', inplace=True)

# 2. Calculate the 30-Day Moving Average
df['30_Day_MA'] = df['units_sold'].rolling(window=30).mean()

# 3. Drop empty rows (the first 29 days won't have a 30-day average)
df_clean = df.dropna()

# 4. Calculate the Mathematical Error
mae = mean_absolute_error(df_clean['units_sold'], df_clean['30_Day_MA'])
rmse = np.sqrt(mean_squared_error(df_clean['units_sold'], df_clean['30_Day_MA']))

print("\n--- BASELINE FORECAST ERROR (30-Day Moving Average) ---")
print(f"Mean Absolute Error (MAE): {mae:.2f} units")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f} units")
print("-------------------------------------------------------")
print("Our goal is to build a Machine Learning model that gets LOWER error scores than these!")