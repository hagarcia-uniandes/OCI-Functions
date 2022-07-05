import io
import json
import logging
import cx_Oracle

from fdk import response

DB_IP = "10.84.7.134"
SID = "EEOCMPP11"
DB_PORT = 1590
DB_USER = "FUNCTIOS"
DB_PASSWORD = "enT3l.2022##"
global query


def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Invoked function eoc")

    try:
        logging.getLogger().info("Getting arguments.")
        body = json.loads(data.getvalue())
        logging.getLogger().info("Getting parameters.")
        numid = body.get("id")
        logging.getLogger().info("Building query for NUMID: " + numid)
        with open("query.sql", "r") as query_file:
            raw_query = query_file.read()
        query = raw_query.replace("{{{numid}}}", numid)
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

            query_response = res[0]
            for row in res:
                logging.getLogger().info(row)

    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try", e)

    return response.Response(
        ctx,
        response_data=json.dumps({"EOC": query_response[0]}),
        headers={"Content-Type": "application/json"},
    )
