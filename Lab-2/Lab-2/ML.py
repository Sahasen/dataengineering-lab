import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import os

# 1. Load dataset
df = pd.read_csv(r"C:\Users\PROMODH\Downloads\FDE lab\Lab-2\Lab-2\raw_data\sale_price.csv")

# 2. Preprocess data
df['quantity'] = df['quantity'].fillna(1).astype(int)
df['sale_price'] = df['sale_price'].replace(r'[\$,]', '', regex=True).astype(float)
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

# 3. Total purchase amount per transaction
df['total_amount'] = df['sale_price'] * df['quantity']

# 4. Aggregate customer-level metrics
customer_metrics = df.groupby('customer_id').agg(
    total_purchase_amount=('total_amount', 'sum'),
    purchase_frequency=('sale_id', 'count'),
    avg_transaction_value=('total_amount', 'mean')
).reset_index()

# 5. Fill missing values with 0
customer_metrics = customer_metrics.fillna(0)

# 6. Normalize features
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(
    customer_metrics[['total_purchase_amount', 'purchase_frequency', 'avg_transaction_value']]
)

# 7. Apply K-Means clustering
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
customer_metrics['cluster'] = kmeans.fit_predict(scaled_features)

# 8. Identify VIP cluster (highest spending)
vip_cluster = customer_metrics.groupby('cluster')['total_purchase_amount'].mean().idxmax()
customer_metrics['VIP_status'] = np.where(
    customer_metrics['cluster'] == vip_cluster, 'VIP', 'Non-VIP'
)

# 9. Merge VIP status back into main dataset
df = df.merge(customer_metrics[['customer_id', 'VIP_status']], on='customer_id', how='left')

# 10. Save enriched dataset
os.makedirs("data_warehouse", exist_ok=True)
file_path = "data_warehouse/sales_data_with_VIP.csv"
df.to_csv(file_path, index=False)

print(f"✅ VIP classification complete. File saved as '{file_path}'.")
