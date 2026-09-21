import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Connect to your database
conn = sqlite3.connect('supply_chain.db')

# 2. Write a SQL query to get the total daily demand
query = """
SELECT date, SUM(units_sold) as total_daily_sales
FROM inventory_data
GROUP BY date
ORDER BY date;
"""

print("Fetching data from SQL...")
df_trend = pd.read_sql_query(query, conn)

# 3. Convert the 'date' column to actual datetime objects for plotting
df_trend['date'] = pd.to_datetime(df_trend['date'])

# 4. Create a Time-Series Plot
print("Generating graph...")
plt.figure(figsize=(14, 6))
sns.lineplot(x='date', y='total_daily_sales', data=df_trend, color='teal', linewidth=1.5)

# Formatting the chart to look professional
plt.title('Total Daily Units Sold Over Time (All Products)', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Units Sold', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Show the plot
plt.show()

# Close the database connection
conn.close()