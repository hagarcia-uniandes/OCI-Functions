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
        logging.getLogger().info("Getting arguments.")
        body = json.loads(data.getvalue())
        logging.getLogger().info("Getting parameters.")
        id = body.get("id")
        raw_query = body.get("query")
        bscs_param = body.get("bscs_param")
        logging.getLogger().info(
            "Building query for ID: " + id + "; BSCS Parameter: " + bscs_param
        )
        query = raw_query.replace("{{{?}}}", id)
    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try", e)
    try:
        logging.getLogger().info(
            "Running against Oracle server:" + DB_IP + " SID:" + SID
        )
        dsn_tns = cx_Oracle.makedsn(DB_IP, DB_PORT, SID)

        with cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn_tns) as con:

            logging.getLogger().info("Database version:", con)
            cur = con.cursor()

            logging.getLogger().info("Quering from DB.")
            cur.execute(query)

            logging.getLogger().info("Fetching data.")
            res = cur.fetchall()

            logging.getLogger().info("Fetched data:", res)
            for row in res:
                logging.getLogger().info(row)
    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try", e)

    logging.getLogger().info("Returning response.")
    return response.Response(
        ctx,
        response_data=json.dumps({bscs_param: row[0]}),
        headers={"Content-Type": "application/json"},
    )
