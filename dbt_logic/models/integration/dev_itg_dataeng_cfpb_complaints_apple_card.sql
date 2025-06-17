select
-- Complaint information
_source_complaint_id as complaint_id,
_source_product as product,
_source_sub_product as sub_product,
_source_issue as issue,
_source_sub_issue as sub_issue,
_source_complaint_what_happened	as complaint_raw_text,
-- Complaint metadata
_source_tags as complaint_tags,
case
    when _source_has_narrative = 'True' then 1
    else 0 
end as has_narrative_flag,
case
    when _source_timely = 'Yes' then 1
    else 0
end as source_timely_flag,
_source_submitted_via as submitted_via,
-- Company information
_source_company as company,
_source_date_sent_to_company as date_sent_to_company,
_source_date_received as date_received_at_company,
_source_company_response as company_response,
case 
    when _source_consumer_disputed = 'N/A' then 0
    else 1
end as consumer_disputed,
_source_company_public_response as company_public_response_to_complaint,
-- Customer information
_source_state as customer_state,
_source_zip_code as zip_code
from {{ ref('dev_raw_dataeng_cfpb_complaints_apple_card') }}