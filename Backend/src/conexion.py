import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

def conectar_servidor():
    try:
        # Conectarse a PostgreSQL en la nube
        conexion = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print('Conexión exitosa')
        return conexion
    except OperationalError as oe:
        print('Error de operación:', oe)
        return None
    except Exception as e:
        print('Error inesperado:', e)
        return None