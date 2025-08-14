# -------------------------------
#  Data Analyst Task - Healthcare
# -------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
patients_df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\patients_data_with_doctor.csv")
doctors_df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\doctors_info.csv")
feedback_df = pd.read_json(r"C:\Users\PROMODH\Downloads\FDE lab\lab 2-patient\raw data\patient_feedback.json")

# Merge patients with doctors
df = patients_df.merge(doctors_df, on="doctor_id", how="left")

# Merge with patient feedback (only on patient_id because JSON has no doctor_id)
df = df.merge(feedback_df, on="patient_id", how="left")

# 1. Aggregate: top 5 doctors by average feedback score
top_doctors = (
    df.groupby(['doctor_id', 'doctor_name'])['patient_feedback_score']
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

# 2. Merge with patient count
patient_counts = (
    df.groupby('doctor_id')['patient_id']
    .nunique()
    .reset_index()
    .rename(columns={'patient_id': 'patient_count'})
)

report_df = top_doctors.merge(patient_counts, on='doctor_id', how='left')

# 3. Visualizations

# Plot 1: Bar chart for Average Feedback Score
plt.figure(figsize=(8, 5))
plt.bar(report_df['doctor_name'], report_df['patient_feedback_score'], color='skyblue')
plt.title('Top 5 Doctors by Average Feedback Score')
plt.xlabel('Doctor Name')
plt.ylabel('Average Feedback Score')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 2: Line plot for Patient Count
plt.figure(figsize=(8, 5))
plt.plot(report_df['doctor_name'], report_df['patient_count'], color='green', marker='o', linewidth=2)
plt.title('Patient Count for Top 5 Doctors')
plt.xlabel('Doctor Name')
plt.ylabel('Patient Count')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Feedback to Data Engineer
print("\n--- Feedback to Data Engineer ---")
if df['patient_feedback_score'].isnull().sum() > 0:
    print("Some feedback scores are missing. Consider improving data collection.")
if df['doctor_name'].isnull().sum() > 0:
    print("Some doctor names are missing. Check doctor_id consistency.")

print("\n--- Final Report ---")
print(report_df)
