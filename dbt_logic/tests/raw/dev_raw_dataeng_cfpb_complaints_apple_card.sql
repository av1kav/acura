select * from {{ ref('dev_raw_dataeng_cfpb_complaints_apple_card') }}
where date_sent_to_company > date_received_at_company