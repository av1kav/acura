select 
    card_name,
    annual_fee,
    card_type,
    recommended_credit_score,
    intro_apr_rate,
    ongoing_apr_fixed
FROM {{ ref('dev_raw_dataeng_cc_comp_info') }}