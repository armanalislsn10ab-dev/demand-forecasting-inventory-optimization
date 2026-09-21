import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# NEW (Secure & Portable)
import os

db_password = os.getenv('DB_PASSWORD', 'YOUR_MYSQL_PASSWORD')
engine = create_engine(f'mysql+pymysql://root:{db_password}@localhost:3306/supply_chain')

# 2. Query only our top product: P0016
query = """
SELECT date, units_sold 
FROM inventory_data 
WHERE product_id = 'P0016' 
ORDER BY date;
"""

print("Fetching data for Product P0016 from MySQL...")
df = pd.read_sql(query, con=engine)

# 3. Data Prep: Convert date string to actual datetime
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# 4. Build the Baseline Forecasts (Moving Averages)
# A 7-day moving average looks at the past week to predict today
df['7_Day_MA'] = df['units_sold'].rolling(window=7).mean()

# A 30-day moving average looks at the past month
df['30_Day_MA'] = df['units_sold'].rolling(window=30).mean()

# 5. Visualize the Actual vs. Forecasted Demand
print("Generating Forecast Graph...")
plt.figure(figsize=(14, 6))

# Plot Actual Sales (Light and thin so it's in the background)
plt.plot(df.index, df['units_sold'], label='Actual Daily Sales', color='lightgrey', alpha=0.7)

# Plot Forecasts
plt.plot(df.index, df['7_Day_MA'], label='7-Day Moving Avg (Short-term trend)', color='blue', linewidth=1.5)
plt.plot(df.index, df['30_Day_MA'], label='30-Day Moving Avg (Long-term trend)', color='red', linewidth=2)

plt.title('Demand Forecasting: Moving Average Baseline for Product P0016', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Units Sold', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save the graph as a picture instead of opening a laggy window
plt.savefig('baseline_forecast.png', dpi=300)
print("Graph saved successfully as baseline_forecast.png!")