import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# NEW (Secure & Portable)
import os

db_password = os.getenv('DB_PASSWORD', 'YOUR_MYSQL_PASSWORD')
engine = create_engine(f'mysql+pymysql://root:{db_password}@localhost:3306/supply_chain')

# 2. Extract Data
query = """
SELECT date, units_sold, `holiday/promotion`, weather_condition, discount, price 
FROM inventory_data 
WHERE product_id = 'P0016' 
ORDER BY date;
"""
df = pd.read_sql(query, con=engine)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# 3. Feature Engineering
df['day_of_week'] = df.index.dayofweek
df['month'] = df.index.month
df['sales_lag_1'] = df['units_sold'].shift(1)
df['sales_lag_7'] = df['units_sold'].shift(7)
df['sales_roll_7'] = df['units_sold'].shift(1).rolling(7).mean()
df.dropna(inplace=True)

# 4. Encoding
df_ml = pd.get_dummies(df, columns=['holiday/promotion', 'weather_condition'], drop_first=True)

X = df_ml.drop('units_sold', axis=1)
y = df_ml['units_sold']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 5. Model 1: Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_preds)

# 6. Model 2: Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)
lr_mae = mean_absolute_error(y_test, lr_preds)

print("--- FORECAST COMPARISON ---")
print(f"30-Day Moving Average Baseline MAE: 87.92 units")
print(f"Linear Regression MAE:            {lr_mae:.2f} units")
print(f"Random Forest MAE:                {rf_mae:.2f} units")
print("---------------------------")

# 7. Print Feature Importances for Random Forest
importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nTop 5 Most Important Features in Random Forest:")
print(importances.head(5))