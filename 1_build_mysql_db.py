import pandas as pd
from sqlalchemy import create_engine

# NEW (Safe for GitHub)
import os

db_password = os.getenv('DB_PASSWORD', 'YOUR_MYSQL_PASSWORD')
engine = create_engine(f'mysql+pymysql://root:{db_password}@localhost:3306/supply_chain')

print("Loading retail_store_inventory.csv in chunks to MySQL...")

# 2. Read and upload in chunks to prevent memory crashes
chunk_size = 10000 
for i, chunk in enumerate(pd.read_csv('retail_store_inventory.csv', chunksize=chunk_size, engine='python', on_bad_lines='skip')):
    
    # Clean column names
    chunk.columns = chunk.columns.str.replace(' ', '_').str.lower()
    
    # Push to MySQL
    if i == 0:
        chunk.to_sql('inventory_data', con=engine, if_exists='replace', index=False)
    else:
        chunk.to_sql('inventory_data', con=engine, if_exists='append', index=False)
    
    print(f"Successfully loaded chunk {i+1} into MySQL...")

print("\nMySQL Database Building Complete! 📦🚀")

# 3. Test the connection by pulling the data back out
query = "SELECT date, product_id, units_sold, inventory_level FROM inventory_data LIMIT 5;"
test_df = pd.read_sql(query, con=engine)
print("\n--- MySQL Database Ready! First 5 Rows ---")
print(test_df)