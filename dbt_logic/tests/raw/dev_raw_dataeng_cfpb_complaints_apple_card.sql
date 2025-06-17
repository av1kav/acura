select * from {{ ref('dev_itg_dataeng_cfpb_complaints_apple_card') }}
where date_sent_to_company > date_received_at_company