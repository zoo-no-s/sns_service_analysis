WITH user_ AS (
    SELECT id, created_at, group_id 
    FROM {{ source('raw_accounts', 'accounts_user') }}
),
group_ AS (
    SELECT id, grade, school_id 
    FROM {{ source('raw_accounts', 'accounts_group') }}
),
school_ AS (
    SELECT id, address, school_type 
    FROM {{ source('raw_accounts', 'accounts_school') }}
)

SELECT user_.id AS user_id
        , user_.created_at AS signup_date
        , user_.group_id
        , group_.grade
        , group_.school_id
        , school_.address
        , school_.school_type
FROM user_
INNER JOIN group_
ON user_.group_id = group_.id
INNER JOIN school_
ON group_.school_id = school_.id