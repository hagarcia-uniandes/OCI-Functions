[3:17 PM] Holman Alberto García Orozco
    
import io
import json
import logging
import cx_Oracle


from fdk import response


DB_IP = "172.21.78.12"
SID = "UEBSLM"
DB_PORT = 1522
DB_USER = "FUNCTIOS"
DB_PASSWORD = "enT3l.2022##"


def handler(ctx, data: io.BytesIO = None):
    logging.getLogger().info("Invoked function ebs")
    try:
        logging.getLogger().info("Getting arguments.")
        body = json.loads(data.getvalue())
        logging.getLogger().info("Getting parameters.")
        avch_tipo_doc_identidad = body.get("tid")
        avch_nro_doc_identidad = body.get("id")
    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try", e)

    try:

        logging.getLogger().info('Running against Oracle server:' + DB_IP + ' SID:' + SID)
        dsn_tns = cx_Oracle.makedsn(DB_IP, DB_PORT, SID)
        with cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn_tns) as con:
            logging.getLogger().info("Database version:", con)
            cur = con.cursor()
            
            logging.getLogger().info("Setting output parameters.")
            anum_deuda_vencida_servicios = cur.var(int)
            anum_deuda_vencida_equipos = cur.var(int)
            anum_deuda_castigada = cur.var(int)
            anum_deuda_castigada_band = cur.var(int)
            anum_interes_castigado = cur.var(int)
            anum_deuda_venc_serv_otro_doc = cur.var(int)
            anum_deuda_venc_eq_otro_doc = cur.var(int)
            avch_deuda_cast_otro_doc = cur.var(int)
            avch_deuda_band_cast_otro_doc = cur.var(int)
            anum_interes_cast_otro_doc = cur.var(int)
            avch_out_cod_rpta = cur.var(str)
            avch_out_msg_rpta = cur.var(str)

            logging.getLogger().info("Performing CALLPROC method.")
            cur.callproc(
                "XXBOL.PKG_CL_CONS_CRED_PCO.SP_CL_CA_CONSDEUDA", 
                [
                    avch_tipo_doc_identidad, 
                    avch_nro_doc_identidad, 
                    anum_deuda_vencida_servicios, 
                    anum_deuda_vencida_equipos, 
                    anum_deuda_castigada, 
                    anum_deuda_castigada_band, 
                    anum_interes_castigado, 
                    anum_deuda_venc_serv_otro_doc, 
                    anum_deuda_venc_eq_otro_doc, 
                    avch_deuda_cast_otro_doc, 
                    avch_deuda_band_cast_otro_doc, 
                    anum_interes_cast_otro_doc, 
                    avch_out_cod_rpta, 
                    avch_out_msg_rpta
                ]
            )

    except Exception as e:  # work on python 3.x
        logging.getLogger().error("Entrando al try",e)

    return response.Response(
        ctx, response_data=json.dumps(
            {​​​​​​
                "anum_deuda_vencida_servicios": anum_deuda_vencida_servicios.getvalue(),
                "anum_deuda_vencida_equipos": anum_deuda_vencida_equipos.getvalue(),
                "anum_deuda_castigada": anum_deuda_castigada.getvalue(),
                "anum_interes_castigado": anum_interes_castigado.getvalue()
            }
        ​​​​​​),
        headers={​​​​​​"Content-Type": "application/json"}​​​​​​
    )

