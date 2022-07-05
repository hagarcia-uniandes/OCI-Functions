import io
import json
import logging
import cx_Oracle

from fdk import response

DB_IP = "172.30.18.45"
SID = "OCRMPP01"
DB_PORT = 1521
DB_USER = "FUNCTIOS"
DB_PASSWORD = "enT3l.2022##"


def handler(ctx, data: io.BytesIO = None):
    # global query
    # global response
    logging.getLogger().info("Invoked function siebel")

    try:
        logging.getLogger().info("Getting arguments.")
        body = json.loads(data.getvalue())
        logging.getLogger().info("Getting parameters.")
        tid = body.get("tid")
        numid = body.get("id")
        logging.getLogger().info("Building query for TID: " + tid + "; NUMID: " + numid)
        with open("query.sql", "r") as query_file:
            raw_query = query_file.read()
        query = raw_query.replace("{{{tid}}}", tid).replace("{{{numid}}}", numid)
        logging.getLogger().info("Builed callproc:")

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
        response_data=json.dumps(
            {
                "siebel": {
                    "TIPODOC": query_response[0],
                    "NRODOC": query_response[1],
                    "NOMBRES": query_response[2],
                    "APELLIDOS": query_response[3],
                    "FECHANACIM": str(query_response[4]),
                    "JOB": query_response[5],
                    "CREACIONREGCLIENTE": str(query_response[6]),
                    "CLIENTEACTIVO": query_response[7],
                    "DEMANDA": query_response[8],
                    "CUENTABSCS": query_response[9],
                    "PADRE": query_response[10],
                    "TIPO": query_response[11],
                }
            }
        ),
        headers={"Content-Type": "application/json"},
    )
