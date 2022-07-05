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
        dsn_tns = cx_Oracle.makedsn(DB_IP, DB_PORT, SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn_tns) as con:
            print("Database version:", con)

            cur = con.cursor()
            EMONCONVEPV	= "SELECT nvl(sum(amount_gross),0) Monto\
                FROM sysadm.fees fe,\
                    sysadm.customer_all ca\
                WHERE fe.sncode IN (select sncode from mpusntab where shdes = 'SVEPP')\
                AND fe.customer_id = ca.customer_id\
                AND ca.custnum = ?\
                AND period > 0"
            cur.execute(EMONCONVEPV)
            res = cur.fetchall()
            for row in res:
                print(row)
                
            return response.Response(
            ctx, response_data=json.dumps(
                {"res": res}),
            headers={"Content-Type": "application/json"}
            )


    except Exception as e:  # work on python 3.x
        print('Failed: ' + str(e))

    