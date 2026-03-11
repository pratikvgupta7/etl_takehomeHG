select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select contracttype
from "analytics"."staging"."stg_churn"
where contracttype is null



      
    ) dbt_internal_test