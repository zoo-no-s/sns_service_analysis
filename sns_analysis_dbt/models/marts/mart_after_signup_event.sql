{{ config(materialized='table') }}

SELECT p.user_id
      , e.event_datetime
      , e.event_key
      , e.item_name
      , e.page_name
      , e.friend_count
      , e.votes_count
      , e.heart_balance
      , e.question_id
FROM {{source('raw_accounts', 'hackle_events')}} AS e
INNER JOIN {{source('raw_accounts', 'hackle_properties')}} AS p
ON e.session_id = p.session_id
WHERE p.user_id IN (
    SELECT DISTINCT(p.user_id) FROM {{source('raw_accounts', 'hackle_events')}} AS e
  INNER JOIN {{source('raw_accounts', 'hackle_properties')}} AS p
  ON e.session_id = p.session_id
  WHERE e.event_key = 'complete_signup'
)