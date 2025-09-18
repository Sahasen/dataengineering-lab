
# Lab 5 – Building a Data Lake

## Overview
This lab demonstrates how to set up an open-source data lake environment locally using **Docker, MinIO, Hive Metastore, Trino Query Engine, and DBeaver. The setup allows storing structured/unstructured data in MinIO (S3-compatible object storage) and querying it using Trino with Hive metadata.

🔧 Prerequisites
- Windows 10/11 with **Docker Desktop** installed  
  👉 [Install Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)  
- Docker Compose installed  
- DBeaver Community Edition installed  
  👉 [Download DBeaver](https://dbeaver.io/download/)  


 🚀 Procedure

 1. Start Services Using Docker Compose
- Open Command Prompt.  
- Navigate to the directory containing your `docker-compose.yml`.  
- Run:  
  ```bash
  docker-compose up
  ```  
- ✅ This will start MinIO, Trino, and Hive Metastore services.  


---

 2. Access MinIO Console
- Open browser → [http://localhost:9001](http://localhost:9001)  
- Login with:  
  - Username: `minio_access_key`  
  - Password: `minio_secret_key`  


---

 3. Access Trino UI
- Open browser → [http://localhost:8086](http://localhost:8086)  
- Login with:  
  - Username: `trino`  

---

4. Connect to Trino Using DBeaver
- Open DBeaver.  
- Create a new connection → Select Trino.  
- Provide connection details:  
  - Host: `localhost`  
  - Port: `8086`  
  - User: `trino`  
- Test connection → Finish.  

---

 5. Create Schema in Hive Metastore
Run in DBeaver SQL editor:  
```sql
CREATE SCHEMA IF NOT EXISTS hive.sales 
WITH (location = 's3a://sales/');
```  
---

 6. Create Table in MinIO (Parquet Format)
```sql
CREATE TABLE IF NOT EXISTS minio.sales.sales_tz (
    productcategoryname      VARCHAR,
    productsubcategoryname   VARCHAR,
    productname              VARCHAR,
    country                  VARCHAR,
    salesamount              DOUBLE,
    orderdate                TIMESTAMP
)
WITH (
    external_location = 's3a://sales/',
    format = 'PARQUET'
);
```  
---

 7. Query the Data
```sql
SELECT * FROM minio.sales.sales_tz LIMIT 10;
```  


---
