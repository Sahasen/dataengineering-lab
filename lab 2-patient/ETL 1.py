import pandas as pd
import os

# Ensure warehouse folder exists
os.makedirs("data_warehouse", exist_ok=True)

# 1. Ingestion
patients_df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\patients_data_with_doctor.csv")
doctors_df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\doctors_info.csv")
feedback_df = pd.read_json(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\patient_feedback.json")
print(feedback_df.columns)
# 2. Cleansing
# Calculate total charges from treatment and room cost
patients_df['total_charges'] = (
    pd.to_numeric(patients_df['treatment_cost'], errors='coerce').fillna(0) +
    pd.to_numeric(patients_df['room_cost'], errors='coerce').fillna(0)
)

# Standardize date formats
patients_df['treatment_date'] = pd.to_datetime(patients_df['treatment_date'], errors='coerce')
feedback_df['review_date'] = pd.to_datetime(feedback_df['review_date'], errors='coerce')


# 3. Transformation
# Merge patients with doctor info
merged_df = patients_df.merge(doctors_df, on='doctor_id', how='left')

# Keep latest feedback per patient
feedback_df = feedback_df.sort_values('review_date').drop_duplicates(
    subset=['patient_id'], keep='last'
)

# Merge feedback into patient-doctor data
merged_df = merged_df.merge(feedback_df, on='patient_id', how='left')

# Remove invalid rows (e.g., zero charges or missing doctor)
merged_df = merged_df[(merged_df['total_charges'] > 0) & (merged_df['doctor_id'].notna())]

# 4. Loading to warehouse
processed_path = "data_warehouse/processed_patient_data.csv"
merged_df.to_csv(processed_path, index=False)

print(f"✅ Processed data saved to {processed_path}")
