import boto3
import uuid
import os
import json

def log_info(data):
    print(json.dumps({
        "tipo": "INFO",
        "log_datos": data
    }))

def log_error(data):
    print(json.dumps({
        "tipo": "ERROR",
        "log_datos": data
    }))

def lambda_handler(event, context):
    try:
        # ====== LOG DE ENTRADA ======
        log_info({"evento_recibido": event})

        # Extracción segura de datos
        body = event.get("body")
        if isinstance(body, str):  # Por si llega como string desde API Gateway
            body = json.loads(body)

        tenant_id = body["tenant_id"]
        pelicula_datos = body["pelicula_datos"]
        nombre_tabla = os.environ["TABLE_NAME"]

        # ====== PROCESO ======
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            "tenant_id": tenant_id,
            "uuid": uuidv4,
            "pelicula_datos": pelicula_datos
        }

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(nombre_tabla)

        response = table.put_item(Item=pelicula)

        # ====== LOG DE SALIDA EXITOSA ======
        log_info({"pelicula_insertada": pelicula})

        return {
            "statusCode": 200,
            "pelicula": pelicula,
            "response": response
        }

    except Exception as e:
        # ====== LOG DE ERROR ======
        log_error({
            "mensaje": str(e),
            "event": event
        })

        return {
            "statusCode": 500,
            "error": str(e)
        }
