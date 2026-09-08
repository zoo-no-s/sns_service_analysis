{{ config(materialized='view') }}

WITH user_base AS (

    SELECT
        id AS user_id,
        created_at AS signup_at
    FROM {{ source('sns_analysis', 'accounts_user') }}

),

questionset_summary AS (

    SELECT
        user_id,
        COUNT(*) AS questionset_count,
        MIN(opening_time) AS first_questionset_at,
        MAX(opening_time) AS last_questionset_at
    FROM {{ source('sns_analysis', 'polls_questionset') }}
    GROUP BY user_id

),

vote_summary AS (

    SELECT
        user_id,
        COUNT(*) AS vote_count,
        MIN(created_at) AS first_vote_at,
        MAX(created_at) AS last_vote_at
    FROM {{ source('sns_analysis', 'accounts_userquestionrecord') }}
    GROUP BY user_id

),

selected_summary AS (

    SELECT
        chosen_user_id AS user_id,
        COUNT(*) AS selected_count,
        COUNTIF(has_read = 1) AS read_selected_count,
        MIN(created_at) AS first_selected_at
    FROM {{ source('sns_analysis', 'accounts_userquestionrecord') }}
    GROUP BY chosen_user_id

),

payment_summary AS (

    SELECT
        user_id,
        COUNT(*) AS payment_count,
        MIN(created_at) AS first_payment_at,
        MAX(created_at) AS last_payment_at
    FROM {{ source('sns_analysis', 'accounts_paymenthistory') }}
    GROUP BY user_id

)

SELECT
    u.user_id,
    u.signup_at,

    q.questionset_count,
    q.first_questionset_at,
    q.last_questionset_at,

    v.vote_count,
    v.first_vote_at,
    v.last_vote_at,

    s.selected_count,
    s.read_selected_count,
    s.first_selected_at,

    p.payment_count,
    p.first_payment_at,
    p.last_payment_at

FROM user_base u

LEFT JOIN questionset_summary q
    ON u.user_id = q.user_id

LEFT JOIN vote_summary v
    ON u.user_id = v.user_id

LEFT JOIN selected_summary s
    ON u.user_id = s.user_id

LEFT JOIN payment_summary p
    ON u.user_id = p.user_id