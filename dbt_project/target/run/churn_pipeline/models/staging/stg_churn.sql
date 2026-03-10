
  create view "analytics"."staging"."stg_churn__dbt_tmp"
    
    
  as (
    SELECT
customerid,
age,
COALESCE(gender,'Unknown') AS gender,
COALESCE(tenure,0) AS tenure,
COALESCE(monthlycharges,0) AS monthlycharges,
contracttype,
internetservice,
COALESCE(totalcharges,0) AS totalcharges, 
techsupport,
churn
FROM raw.customer_churn_raw
  );