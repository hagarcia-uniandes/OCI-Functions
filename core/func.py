import io
import json
import logging
import oci
from fdk import response

def handler(ctx, data: io.BytesIO=None):
    config = oci.config.from_file()
    try:
        body = json.loads(data.getvalue())
        function_endpoint = body.get("function_endpoint")
        function_ocid = body.get("function_ocid")
        function_body = body.get("function_body")
    except (Exception) as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise
    
    signer = oci.auth.signers.get_resource_principals_signer()
    client = oci.functions.FunctionsInvokeClient(config=config, signer=signer, service_endpoint=function_endpoint)
    logging.getLogger().info('client')
    resp = client.invoke_function(function_id=function_ocid, invoke_function_body=function_body, fn_intent="httprequest", fn_invoke_type="detached")
    logging.getLogger().info('resp')
    #print(resp.data.text, flush=True)

    return response.Response(
        ctx, 
        response_data=resp.data.text,
        headers={"Content-Type": "application/json"}
    )

