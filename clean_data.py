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
# -------------------------------------
# 1. Add consent flag to customer data
# -------------------------------------
customer_df['hasConsented'] = customer_df[
    ['shareWithResearchAsOfDate', 'shareWithPublicAsOfDate', 'shareWithFriendsAsOfDate']
].notnull().any(axis=1)

# ------------------------------------------------
# 2. Create filtered view of customers who consented
# ------------------------------------------------
opted_in_customers = customer_df[customer_df['hasConsented']]

# ------------------------------------------------
# 3. Merge with Accelerometer Data (user ↔ email)
# ------------------------------------------------
merged_accel = pd.merge(
    accelerometer_df,
    opted_in_customers,
    left_on='user',
    right_on='email',
    how='inner'
)

# ------------------------------------------------
# 4. Merge with Step Trainer Data (serialNumber)
# ------------------------------------------------
merged_step = pd.merge(
    step_trainer_df,
    opted_in_customers,
    on='serialNumber',
    how='inner'
)

# ------------------------------------------------
# 5. Export Cleaned/Filtered Data
# ------------------------------------------------
output_dir = "./cleaned_output"
os.makedirs(output_dir, exist_ok=True)

opted_in_customers.to_csv(f"{output_dir}/filtered_customers.csv", index=False)
merged_accel.to_csv(f"{output_dir}/merged_accelerometer.csv", index=False)
merged_step.to_csv(f"{output_dir}/merged_step_trainer.csv", index=False)

print("✅ Export complete. Files saved in ./cleaned_output/")