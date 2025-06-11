BEGIN;

DROP TABLE IF EXISTS public.cc_comp_info;

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

COMMIT;

BEGIN;

-- Copy data from the CSV file into the 'cc_comp_info' table
COPY public.cc_comp_info(card_name, annual_fee, card_type, recommended_credit_score, intro_apr_rate, intro_apr_duration, ongoing_apr_fixed, ongoing_apr_variable, foreign_transaction_fee)
FROM '/var/lib/postgresql/mock_data/credit_cards_comparison.csv'
DELIMITER ','
CSV HEADER;

COMMIT;
