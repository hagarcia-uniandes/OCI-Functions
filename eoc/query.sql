select
    count(1)
from
    (
        select
            distinct oi.ordernum
        from
            eoc.cworderinstance oi,
            eoc.eoc_running_order ro,
            eoc.om_order_header_postpaid oh
        where
            oi.ordernum = ro.requestnumber
            and oi.ordernum = oh.requestnumber
            and ro.state = 'RUNNING'
            and oh.requesttype in (
                'Cambio',
                'Migracion Prepago a Postpago',
                'Portabilidad',
                'Cesion de Linea',
                'Activacion de Linea',
                'Venta',
                'Cambio de Plan Retencion'
            )
            and oi.customerid = '{{{numid}}}'
    )