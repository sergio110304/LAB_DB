import psycopg2
from psycopg2 import OperationalError

def conectar_servidor():
    try:
        # Conectarse a PostgreSQL en la nube
        conexion = psycopg2.connect(
            dbname="lab_icfes",
            user="avnadmin",
            password="AVNS_lVvSfnZ_z2Bnmfj5ASI",
            host="pg-ed88bff-srodriguezcabana-914d.h.aivencloud.com",
            port="23178"
        )
        print('Conexión exitosa')
        return conexion
    except OperationalError as oe:
        print('Error de operación:', oe)
        return None
    except Exception as e:
        print('Error inesperado:', e)
        return None