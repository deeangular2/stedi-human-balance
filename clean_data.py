# Load Data
import pandas as pd
import glob
import os

# Set your directory paths
accel_directory_path = "C:/Users/deird/Documents/stedi-human-balance/data/Raw/accelerometer/landing/"
cust_file_path = "C:/Users/deird/Documents/stedi-human-balance/data/Raw/customer/landing/customer-1691348231425.json"
step_trainer_directory_path = "C:/Users/deird/Documents/stedi-human-balance/data/Raw/step_trainer/landing/"

# Load all JSON files in accelerometer and step_trainer directories
all_accel_files = glob.glob(os.path.join(accel_directory_path, "*.json"))
all_step_trainer_files = glob.glob(os.path.join(step_trainer_directory_path, "*.json"))

# Read and combine accelerometer files
accel_df_list = [pd.read_json(file, lines=True) for file in all_accel_files]
accelerometer_df = pd.concat(accel_df_list, ignore_index=True)

# Read and combine step trainer files
step_trainer_df_list = [pd.read_json(file, lines=True) for file in all_step_trainer_files]
step_trainer_df = pd.concat(step_trainer_df_list, ignore_index=True)

# Read the single customer file
customer_df = pd.read_json(cust_file_path, lines=True)

# Inspect data
print("Customer Data:")
customer_df.info()
print(customer_df.isnull().sum(), "\n")

print("Accelerometer Data:")
accelerometer_df.info()
print(accelerometer_df.isnull().sum(), "\n")

print("Step Trainer Data:")
step_trainer_df.info()
print(step_trainer_df.isnull().sum(), "\n")

# 1. Add consent flag to customer data
# -------------------------------------
customer_df['hasConsented'] = customer_df[
    ['shareWithResearchAsOfDate', 'shareWithPublicAsOfDate', 'shareWithFriendsAsOfDate']
].notnull().any(axis=1)

# ------------------------------------------------
# 2. Filter only customers who consented
# ------------------------------------------------
opted_in_customers = customer_df[customer_df['hasConsented']]

# ------------------------------------------------
# 3. Convert all date columns from ms to datetime
# ------------------------------------------------
timestamp_cols = [
    'registrationDate', 'lastUpdateDate',
    'shareWithResearchAsOfDate', 'shareWithPublicAsOfDate', 'shareWithFriendsAsOfDate'
]
for col in timestamp_cols:
    opted_in_customers[col] = pd.to_datetime(opted_in_customers[col], unit='ms', errors='coerce')

# Optional: Convert 'birthDay' to datetime
opted_in_customers['birthDay'] = pd.to_datetime(opted_in_customers['birthDay'], errors='coerce')

# Ensure phone number is string
opted_in_customers['phone'] = opted_in_customers['phone'].astype(str)

# ------------------------------------------------
# 4. Merge with accelerometer and step trainer data
# ------------------------------------------------
merged_accel = pd.merge(accelerometer_df, opted_in_customers, left_on='user', right_on='email', how='inner')
merged_step = pd.merge(step_trainer_df, opted_in_customers, on='serialNumber', how='inner')

# Convert step_trainer timestamp (sensorReadingTime) to datetime
merged_step['sensorReadingTime'] = pd.to_datetime(merged_step['sensorReadingTime'], unit='ms', errors='coerce')

# ------------------------------------------------
# 5. Export as JSON Lines (.jsonl)
# ------------------------------------------------
output_dir = "./cleaned_output"
os.makedirs(output_dir, exist_ok=True)

# Save all as line-delimited JSON
opted_in_customers.to_json(f"{output_dir}/filtered_customers.json", orient="records", lines=True)
merged_accel.to_json(f"{output_dir}/merged_accelerometer.json", orient="records", lines=True)
merged_step.to_json(f"{output_dir}/merged_step_trainer.json", orient="records", lines=True)

print("✅ JSON export complete. Files saved to ./cleaned_output/")