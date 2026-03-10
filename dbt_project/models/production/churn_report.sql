SELECT
contractType,
COUNT(*) AS totalCustomers,
SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END) AS churnedCustomers,
AVG(monthlycharges) AS avgMonthlyCharge,
AVG(tenure) AS avgTenure
FROM {{ ref('stg_churn') }}
GROUP BY contractType