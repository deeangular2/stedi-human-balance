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

# Read and combine accelerometer files with error handling
accel_df_list = []
for file in all_accel_files:
    try:
        df = pd.read_json(file, lines=True)
        accel_df_list.append(df)
    except ValueError as e:
        print(f" Failed to read accelerometer file {file}: {e}")
accelerometer_df = pd.concat(accel_df_list, ignore_index=True)

# Read and combine step trainer files with error handling
step_trainer_df_list = []
for file in all_step_trainer_files:
    try:
        df = pd.read_json(file, lines=True)
        step_trainer_df_list.append(df)
    except ValueError as e:
        print(f" Failed to read step trainer file {file}: {e}")
step_trainer_df = pd.concat(step_trainer_df_list, ignore_index=True)

# Read the single customer file
customer_df = pd.read_json(cust_file_path, lines=True)

# 1. Add consent flag to customer data
customer_df['hasConsented'] = customer_df[
    ['shareWithResearchAsOfDate', 'shareWithPublicAsOfDate', 'shareWithFriendsAsOfDate']
].notnull().any(axis=1)

# 2. Filter only customers who consented
opted_in_customers = customer_df[customer_df['hasConsented']].copy()

# 3. Convert date columns from ms to datetime
timestamp_cols = [
    'registrationDate', 'lastUpdateDate',
    'shareWithResearchAsOfDate', 'shareWithPublicAsOfDate', 'shareWithFriendsAsOfDate'
]
for col in timestamp_cols:
    opted_in_customers[col] = pd.to_datetime(opted_in_customers[col], unit='ms', errors='coerce')
opted_in_customers['birthDay'] = pd.to_datetime(opted_in_customers['birthDay'], errors='coerce')
opted_in_customers['phone'] = opted_in_customers['phone'].astype(str)

# 4. Merge with accelerometer and step trainer data
merged_accel = pd.merge(accelerometer_df, opted_in_customers, left_on='user', right_on='email', how='inner')
merged_step = pd.merge(step_trainer_df, opted_in_customers, on='serialNumber', how='inner')
merged_step['sensorReadingTime'] = pd.to_datetime(merged_step['sensorReadingTime'], unit='ms', errors='coerce')

#  Clean merged data: drop rows with critical missing values
merged_accel.dropna(subset=['user', 'email', 'timestamp'], inplace=True)
merged_step.dropna(subset=['serialNumber', 'sensorReadingTime'], inplace=True)

#  Drop duplicates
merged_accel.drop_duplicates(inplace=True)
merged_step.drop_duplicates(inplace=True)

# 5. Export as JSON Lines (.jsonl)
output_dir = "./cleaned_output"
os.makedirs(output_dir, exist_ok=True)

opted_in_customers.to_json(f"{output_dir}/filtered_customers.json", orient="records", lines=True)
merged_accel.to_json(f"{output_dir}/merged_accelerometer.json", orient="records", lines=True)
merged_step.to_json(f"{output_dir}/merged_step_trainer.json", orient="records", lines=True)

print(" JSON export complete. Files saved to ./cleaned_output/")

# 6. Validate a few records from each output
print("\ Sample Output:")
print("Customers:", pd.read_json(f"{output_dir}/filtered_customers.json", lines=True).head(2), "\n")
print("Accelerometer:", pd.read_json(f"{output_dir}/merged_accelerometer.json", lines=True).head(2), "\n")
print("Step Trainer:", pd.read_json(f"{output_dir}/merged_step_trainer.json", lines=True).head(2), "\n")

