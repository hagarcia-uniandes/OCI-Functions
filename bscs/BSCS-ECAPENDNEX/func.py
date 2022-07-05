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

            logging.getLogger().info("Database version:", con)
            cur = con.cursor()
            ECAPENDNEX =	"select nvl(sum(amount_gross),0)\
                                from sysadm.fees fe,\
                                    sysadm.customer_all ca\
                                where fe.sncode in (select sncode from mpusntab where shdes = 'SVEPP')\
                                and fe.customer_id = ca.customer_id\
                                and ca.custnum = '" + id +\
                                "'and period > 0 "

            cur.execute(ECAPENDNEX)
            res = cur.fetchall()
            logging.getLogger().info(res)
            for row in res:
                logging.getLogger().info(row)

            return response.Response(
                ctx, response_data=json.dumps(
                    {"ECAPENDNEX": row[0]}),
                headers={"Content-Type": "application/json"}
            )
                
     
    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try",e)
    
