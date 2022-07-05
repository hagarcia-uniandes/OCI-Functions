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
    logging.getLogger().info("Invoked function core")

    try:
        body = json.loads(data.getvalue())
        id = body.get("id")
        logging.getLogger().info('Running against Oracle server:' + DB_IP + ' SID:' + SID)
        dsn_tns = cx_Oracle.makedsn(DB_IP, DB_PORT, SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn_tns) as con:
            print("Database version:", con)

            cur = con.cursor()
            EMONCONMOV	= "select nvl(round(sum(ACCESSFEE),0),0) Monto\
                from (select cu.custnum, tmb.*\
                        from sysadm.customer_all cu, sysadm.profile_service ps\
                            inner join pr_serv_spcode_hist psph using (co_id)\
                            inner join pr_serv_status_hist psth using (co_id)\
                            inner join contract_all ca using (co_id)\
                            inner join mpusptab sp on psph.spcode = sp.spcode\
                            inner join mpusntab sn on sn.sncode = ps.sncode\
                            inner join mpulktmb tmb on psth.sncode = tmb.sncode\
                            inner join ccontact_all cc on ca.customer_id = cc.customer_id\
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
                                    "' and cc.ccseq = (select max(xx.ccseq)\
                            from  sysadm.ccontact_all xx\
                                    where xx.customer_id = cc.customer_id)\
                                    and tmb.vscode = (select max(x.vscode) from mpulktmb x where x.tmcode = tmb.tmcode)\
                                )"

            cur.execute(EMONCONMOV)
            res = cur.fetchall()
            logging.getLogger().info(res)
            for row in res:
                logging.getLogger().info(row)

            return response.Response(
                ctx, response_data=json.dumps(
                    {"EMONCONMOV": row[0]}),
            headers={"Content-Type": "application/json"}
            )

    except Exception as e:  # work on python 3.x
        print('Failed: ' + str(e))

    
