import io
import json
import logging
import cx_Oracle

from fdk import response


DB_IP = "10.84.7.6"
SID = "EBSCSPP11"
DB_PORT = 1590
DB_USER = "FUNCTIOS"
DB_PASSWORD = "enT3l.2022##"

def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Invoked function bscs-emoncon")

    try:
        body = json.loads(data.getvalue())
        id = body.get("id")
        logging.getLogger().info('Running against Oracle server:' + DB_IP + ' SID:' + SID)
        dsn_tns = cx_Oracle.makedsn(DB_IP, DB_PORT, SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn_tns) as con:
            print("Database version:", con)

            cur = con.cursor()
            EMONCON	= "select nvl(round(sum(amounttotal),0),0)\
                from (\
                    select cu.custnum, nvl(sum(round(tmb.accessfee, 1)), 1)  amounttotal\
                    from sysadm.customer_all cu,\
                        sysadm.profile_service ps\
                    inner join pr_serv_spcode_hist psph using (co_id)\
                    inner join pr_serv_status_hist psth using (co_id)\
                    inner join contract_all ca using (co_id)\
                    inner join mpusptab sp on psph.spcode = sp.spcode\
                    inner join mpusntab sn on sn.sncode = ps.sncode\
                    inner join mpulktmb tmb on psth.sncode = tmb.sncode\
                    where cu.customer_id = ca.customer_id\
                    and ps.spcode_histno = psph.histno\
                    and ps.status_histno = psth.histno\
                    and ps.sncode = psph.sncode\
                    and psph.sncode = psth.sncode\
                    and sp.spcode = tmb.spcode\
                    and tmb.accessfee > 0\
                    and psth.status <> 'D'\
                    and tmb.tmcode = 3\
                    and ca.ch_status in ('a', 's')\
                    and ca.contract_type_id = 1\
                    and cu.custnum = '" + id +\
                    "' and tmb.vscode = (select max(x.vscode) from mpulktmb x where x.tmcode = tmb.tmcode)\
                    group by cu.custnum\
                    union all\
                    select custnum,sum(amounttotal)\
                    from\
                    (\
                        select ca.custnum,nvl(sum(amount_gross),0)/count(1) as amounttotal\
                        from sysadm.fees fe,\
                            sysadm.customer_all ca\
                        where fe.sncode in (select sncode from mpusntab where shdes = 'SVEPP')\
                        and fe.customer_id = ca.customer_id\
                        and ca.custnum = '" + id +\
                        "' and period > 0\
                        group by ca.custnum,amount_gross\
                    )\
                    group by custnum\
                    union all\
                    select cu.custnum, nvl(sum(round(ps.accessfee, 1)), 1)  amounttotal\
                    from sysadm.customer_all cu,\
                        sysadm.profile_service ps\
                    inner join pr_serv_spcode_hist psph using (co_id)\
                    inner join pr_serv_status_hist psth using (co_id)\
                    inner join contract_all ca using (co_id)\
                    where cu.customer_id = ca.customer_id\
                    and ps.spcode_histno = psph.histno\
                    and ps.status_histno = psth.histno\
                    and ps.sncode = psph.sncode\
                    and psph.sncode = psth.sncode\
                    and ps.accessfee > 0\
                    and psth.status <> 'D'\
                    and ca.tmcode = 12\
                    and ca.ch_status in ('a', 's')\
                    and ca.contract_type_id = 1\
                    and cu.custnum = '" + id +\
                    "' group by cu.custnum\
                )"
            cur.execute(EMONCON)
            res = cur.fetchall()
            logging.getLogger().info(res)
            for row in res:
                logging.getLogger().info(row)
            
            return response.Response(
            ctx, response_data=json.dumps(
                {"EMONCON": row[0]}),
            headers={"Content-Type": "application/json"}
            )

    except Exception as e:  # work on python 3.x
        print('Failed: ' + str(e))

    
