import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import os
import json

# -----------------------------
# 1. Load datasets
# -----------------------------
patients_df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\patients_data_with_doctor.csv")
doctors_df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\doctors_info.csv")

with open(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\patient_feedback.json", "r") as f:
    feedback_data = json.load(f)

feedback_df = pd.DataFrame(feedback_data)

# Remove whitespace from column names (if any)
patients_df.columns = patients_df.columns.str.strip()
doctors_df.columns = doctors_df.columns.str.strip()
feedback_df.columns = feedback_df.columns.str.strip()

# -----------------------------
# 2. Preprocess treatment cost
# -----------------------------
patients_df['treatment_cost'] = pd.to_numeric(
    patients_df['treatment_cost'], errors='coerce'
).fillna(0)

# -----------------------------
# 3. Calculate patient-level metrics
# -----------------------------
patient_metrics = patients_df.groupby('patient_id').agg(
    total_treatment_cost=('treatment_cost', 'sum'),
    visit_frequency=('treatment_cost', 'count'),
    avg_treatment_value=('treatment_cost', 'mean')
).reset_index()

# Fill missing values
patient_metrics = patient_metrics.fillna(0)

# -----------------------------
# 4. Normalize features
# -----------------------------
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(
    patient_metrics[['total_treatment_cost', 'visit_frequency', 'avg_treatment_value']]
)

# -----------------------------
# 5. Apply K-Means clustering
# -----------------------------
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
patient_metrics['cluster'] = kmeans.fit_predict(scaled_features)

# -----------------------------
# 6. Identify VIP cluster
# -----------------------------
vip_cluster = patient_metrics.groupby('cluster')['total_treatment_cost'].mean().idxmax()
patient_metrics['VIP_status'] = np.where(
    patient_metrics['cluster'] == vip_cluster, 'VIP', 'Non-VIP'
)

# -----------------------------
# 7. Merge VIP status back (Reverse ETL)
# -----------------------------
patients_enriched = patients_df.merge(
    patient_metrics[['patient_id', 'VIP_status']], on='patient_id', how='left'
)

# Merge with doctors info
patients_enriched = patients_enriched.merge(doctors_df, on='doctor_id', how='left')

# Merge with feedback (if it contains patient_id)
if 'patient_id' in feedback_df.columns:
    patients_enriched = patients_enriched.merge(feedback_df, on='patient_id', how='left')

# -----------------------------
# 8. Save enriched dataset
# -----------------------------
os.makedirs("data_warehouse", exist_ok=True)
output_path = "data_warehouse/patient_data_with_VIP.csv"
patients_enriched.to_csv(output_path, index=False)

print(f"✅ VIP classification complete. File saved as '{output_path}'")
