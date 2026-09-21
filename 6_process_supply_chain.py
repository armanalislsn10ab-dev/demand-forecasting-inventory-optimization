import pandas as pd
import numpy as np

# 1. Load full raw dataset
df = pd.read_csv('retail_store_inventory.csv', usecols=range(15))
df['date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.sort_values(['Product ID', 'Store ID', 'date'])

# 2. Rename columns to standard clean format
df = df.rename(columns={
    'Store ID': 'store_id',
    'Product ID': 'product_id',
    'Category': 'category',
    'Region': 'region',
    'Inventory Level': 'inventory_level',
    'Units Sold': 'units_sold',
    'Demand Forecast': 'ml_forecast',
    'Price': 'price',
    'Discount': 'discount',
    'Holiday/Promotion': 'holiday_promotion',
    'Weather Condition': 'weather_condition'
})

# 3. Calculate moving averages, safety stock, ROP, and recommended order quantities
df['baseline_ma_30'] = df.groupby(['product_id', 'store_id'])['units_sold'].transform(
    lambda x: x.rolling(30, min_periods=1).mean()
).round(1)

df['safety_stock'] = (df.groupby(['product_id', 'store_id'])['units_sold'].transform('std') * 1.65).fillna(50).round()
df['reorder_point'] = (df['baseline_ma_30'] * 2 + df['safety_stock']).round()
df['recommended_order'] = (df['reorder_point'] - df['inventory_level']).clip(lower=0)

# Assign stock alert statuses
conditions = [
    df['inventory_level'] <= df['safety_stock'],
    df['inventory_level'] <= df['reorder_point'],
    df['inventory_level'] > df['reorder_point']
]
choices = ['🔴 Critical Stockout Risk', '⚠️ Reorder Needed', '✅ Healthy Stock']
df['stock_status'] = np.select(conditions, choices, default='✅ Healthy Stock')

# 4. Filter columns and export to single master CSV
cols = ['date', 'store_id', 'product_id', 'category', 'region', 'inventory_level', 
        'units_sold', 'baseline_ma_30', 'ml_forecast', 'safety_stock', 
        'reorder_point', 'recommended_order', 'stock_status', 'price', 
        'discount', 'holiday_promotion', 'weather_condition']

df[cols].to_csv('fact_inventory.csv', index=False)
print("Done! Overwritten fact_inventory.csv with all 73,100 rows and 17 columns.")