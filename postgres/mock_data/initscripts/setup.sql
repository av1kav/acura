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

DROP SCHEMA IF EXISTS raw;
CREATE SCHEMA raw;

DROP SCHEMA IF EXISTS integration;
CREATE SCHEMA integration;

DROP SCHEMA IF EXISTS presentation;
CREATE SCHEMA presentation;

COMMIT;

BEGIN;

COPY public.cc_comp_info(card_name, annual_fee, card_type, recommended_credit_score, intro_apr_rate, intro_apr_duration, ongoing_apr_fixed, ongoing_apr_variable, foreign_transaction_fee)
FROM '/var/lib/postgresql/mock_data/credit_cards_comparison.csv'
DELIMITER ','
CSV HEADER;

COMMIT;
