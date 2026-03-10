CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS production;

CREATE TABLE raw.customer_churn_raw(
CustomerID TEXT,
Age INTEGER,
Gender TEXT,
Tenure INTEGER,
MonthlyCharges FLOAT,
ContractType TEXT,
InternetService TEXT,
TotalCharges FLOAT,
TechSupport TEXT,
Churn TEXT,
ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)