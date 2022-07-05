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
            EFLGCLIREC = "select decode(count(1), 0, 0, 1)\
                         from sysadm.customer_all cusa,\
                         sysadm.contract_all cona\
                         where cusa.customer_id = cona.customer_id\
                         and cusa.custnum = '" + id +\
                         "' and cona.tmcode = 3\
                         and cona.ch_status in ('a', 's')"

            cur.execute(EFLGCLIREC)
            res = cur.fetchall()
            logging.getLogger().info(res)
            for row in res:
                logging.getLogger().info(row)

            return response.Response(
                ctx, response_data=json.dumps(
                    {"EFLGCLIREC": row[0]}),
                headers={"Content-Type": "application/json"}
            )
                
     
    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try",e)
    
