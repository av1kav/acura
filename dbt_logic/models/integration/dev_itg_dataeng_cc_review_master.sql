SELECT
    card_name,
    platform_name,
    review_timestamp,
    review_id,
    review_customer_id,
    review_customer_name,
    review_rating_maximum,
    CASE 
        WHEN review_rating_given <= 1 THEN 1
        WHEN review_rating_given >= 5 THEN 5
        ELSE review_rating_given::int
    END AS review_rating_given,
    review_raw_text
FROM {{ ref('dev_raw_dataeng_cc_review_events') }}