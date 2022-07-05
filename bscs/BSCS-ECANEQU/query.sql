SELECT
  count(1)
FROM
  sysadm.customer_all cusa,
  sysadm.contract_all cona
WHERE
  cusa.customer_id = cona.customer_id
  AND cusa.CUSTNUM = '{{{?}}}'
  AND cona.tmcode = 3
  AND cona.ch_status IN ('a', 's')