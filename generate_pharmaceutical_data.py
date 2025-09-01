import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker for realistic data
fake = Faker()
Faker.seed(0)  # For reproducibility
np.random.seed(0) # For numpy randomness reproducibility
random.seed(0) # For random module reproducibility

# --- 1. drugs.csv (Dimension Table) ---
num_drugs = 200  # 200 unique drugs
drug_ids = [f'DRUG{i:03d}' for i in range(1, num_drugs + 1)]
drug_names = [fake.unique.word().capitalize() + 'Tab' for _ in range(num_drugs)]
therapeutic_areas = ['Cardiology', 'Oncology', 'Neurology', 'Dermatology']
# Correctly re-adding DrugType as planned, while ensuring AvgCostPerUnit remains
drug_types = ['Tablet', 'Injectable', 'Capsule', 'Solution', 'Cream'] # Added more variety

drugs_data = []
for i in range(num_drugs):
    market_launch_date = fake.date_between(start_date='-10y', end_date='today')
    avg_cost_per_unit = round(random.uniform(5.0, 500.0), 2) # Ensure AvgCostPerUnit is here

    drugs_data.append({
        'DrugID': drug_ids[i],
        'DrugName': drug_names[i],
        'TherapeuticArea': random.choice(therapeutic_areas),
        'DrugType': random.choice(drug_types), # This is the new column
        'MarketLaunchDate': market_launch_date.strftime('%Y-%m-%d'),
        'AvgCostPerUnit': avg_cost_per_unit # This column is now correctly included
    })

df_drugs = pd.DataFrame(drugs_data)
df_drugs.loc[df_drugs.sample(frac=0.05).index, 'TherapeuticArea'] = np.nan  # 5% missing
df_drugs.to_csv('drugs.csv', index=False)
print(f"Generated drugs.csv with {len(df_drugs)} records.")

# --- 2. sales.csv (Fact Table) ---
num_sales = 100000
sales_data = []
for i in range(num_sales):
    sale_date = fake.date_between(start_date='-3y', end_date='today')
    date_format = random.choice(['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y'])
    
    sales_data.append({
        'SaleID': f'SALE{i:06d}',
        'SaleDate': sale_date.strftime(date_format),
        'DrugID': random.choice(drug_ids),
        'Region': random.choice(['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Oceania']), # Re-added Region
        'UnitsSold': random.randint(10, 1000) if random.random() > 0.01 else 99999,  # Outliers
        'Revenue': round(random.uniform(100, 10000), 2) if random.random() > 0.03 else np.nan  # 3% missing
    })

df_sales = pd.DataFrame(sales_data)
df_sales.to_csv('sales.csv', index=False)
print(f"Generated sales.csv with {len(df_sales)} records.")

# --- 3. manufacturing_batches.csv (Fact Table) ---
num_batches = 100000
manufacturing_plants = [f'PLANT{i:02d}' for i in range(1, 11)] # 10 plants
statuses = ['Completed', 'Failed', 'Discarded']
failure_reasons = ['Contamination', 'Equipment Malfunction', 'Raw Material Defect', 'Human Error', None]

batch_data = []
for i in range(num_batches):
    manufacturing_date = fake.date_between(start_date='-2y', end_date='today')
    date_format = random.choice(['%Y-%m-%d', '%d/%m/%Y']) # Mixed date formats
    
    status = random.choice(statuses)
    reason = None
    if status == 'Failed':
        reason = random.choice([r for r in failure_reasons if r is not None])
        if random.random() < 0.1: # 10% missing failure reason for failed
            reason = np.nan
    elif status == 'Discarded': # Discarded batches also have reasons
        reason = random.choice([r for r in failure_reasons if r is not None])
        if random.random() < 0.05: # 5% missing reason for discarded
            reason = np.nan

    batch_size = random.randint(1000, 50000)
    if random.random() < 0.005: # Outlier batch sizes
        batch_size = random.randint(100000, 500000)

    batch_data.append({
        'BatchID': f'BATCH{i:06d}',
        'DrugID': random.choice(drug_ids),
        'ManufacturingDate': manufacturing_date.strftime(date_format), # NEW
        'ManufacturingPlantID': random.choice(manufacturing_plants),  # NEW
        'BatchSizeUnits': batch_size,                                 # NEW
        'status': status,
        'FailureReason': reason
    })

df_batches = pd.DataFrame(batch_data)
# Inconsistent casing for status (10% chance)
df_batches['status'] = df_batches['status'].apply(lambda x: x.upper() if random.random() < 0.1 else x)
# Introduce some inconsistent failure reasons
df_batches.loc[df_batches.sample(frac=0.01).index, 'FailureReason'] = 'OTHER'
df_batches.to_csv('manufacturing_batches.csv', index=False)
print(f"Generated manufacturing_batches.csv with {len(df_batches)} records.")

print("\n--- Data Generation Complete! ---")
print("You can now find 'drugs.csv', 'sales.csv', and 'manufacturing_batches.csv' in your current directory.")
print("Proceed to update your Power BI model!")
