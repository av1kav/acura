BEGIN;

DROP TABLE IF EXISTS public.my_first_dbt_model CASCADE;
DROP TABLE IF EXISTS public.my_second_dbt_model CASCADE;

DROP TABLE IF EXISTS public.cc_comp_info CASCADE;
CREATE TABLE public.cc_comp_info (
    card_name VARCHAR(255),
    annual_fee VARCHAR(255),
    card_type VARCHAR(255),
    recommended_credit_score VARCHAR(255),
    intro_apr_rate FLOAT,
    intro_apr_duration VARCHAR(255),
    ongoing_apr_fixed FLOAT,
    ongoing_apr_variable FLOAT,
    foreign_transaction_fee FLOAT
);

DROP TABLE IF EXISTS public.cc_review_events CASCADE;
CREATE TABLE public.cc_review_events (
    card_name VARCHAR(255),
    platform_name VARCHAR(255),
    review_timestamp TIMESTAMP,
    review_id VARCHAR(255),
    review_customer_id VARCHAR(255),
    review_customer_name VARCHAR(255),
    review_rating_maximum NUMERIC(1,0),
    review_rating_given NUMERIC(1,0),
    review_raw_text VARCHAR(255)
);


DROP SCHEMA IF EXISTS raw;
DROP SCHEMA IF EXISTS integration;
DROP SCHEMA IF EXISTS presentation;

COMMIT;

BEGIN;

-- Credit card comparison info from the web
COPY public.cc_comp_info(card_name, annual_fee, card_type, recommended_credit_score, intro_apr_rate, intro_apr_duration, ongoing_apr_fixed, ongoing_apr_variable, foreign_transaction_fee)
FROM '/var/lib/postgresql/mock_data/credit_cards_comparison.csv'
DELIMITER ','
CSV HEADER;

-- Credit card reviews
COPY public.cc_review_events(card_name, platform_name, review_timestamp, review_id, review_customer_id, review_customer_name, review_rating_maximum, review_rating_given, review_raw_text)
FROM '/var/lib/postgresql/mock_data/credit_cards_reviews.csv'
DELIMITER ','
CSV HEADER;

COMMIT;
