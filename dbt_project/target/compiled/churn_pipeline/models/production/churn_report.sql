SELECT
contractType,
COUNT(*) AS totalCustomers,
SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END) AS churnedCustomers,
AVG(monthlycharges) AS avgMonthlyCharge,
AVG(tenure) AS avgTenure
FROM "analytics"."staging"."stg_churn"
GROUP BY contractType