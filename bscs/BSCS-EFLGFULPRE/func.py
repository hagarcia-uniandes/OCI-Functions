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
            EFLGFULPRE =	"select count(1)\
                                                from sysadm.customer_all a,\
                                                    sysadm.contract_all b\
                                                where a.customer_id = b.customer_id\
                                                and a.custnum = '" + id +\
                                                "' and b.tmcode in (4)\
                                                and b.ch_status in ('a', 's')"

            cur.execute(EFLGFULPRE)
            res = cur.fetchall()
            logging.getLogger().info(res)
            for row in res:
                logging.getLogger().info(row)
                
            return response.Response(
                ctx, response_data=json.dumps(
                    {"EFLGFULPRE": row[0]}),
                headers={"Content-Type": "application/json"}
            )

   
    except Exception as e:  # work on python 3.x
        print('Failed: ' + str(e))

    
