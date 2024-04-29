import psycopg2
from psycopg2 import OperationalError

def create_database():
    try:
        # Conectarse a PostgreSQL en la nube
        conn = psycopg2.connect(
            dbname="defaultdb",
            user="avnadmin",
            password="AVNS_lVvSfnZ_z2Bnmfj5ASI",
            host="pg-ed88bff-srodriguezcabana-914d.h.aivencloud.com",
            port="23178"
        )
        conn.autocommit = True
        # Crear un cursor
        cursor = conn.cursor()
        
        # Crear una nueva base de datos
        cursor.execute("CREATE DATABASE LAB_ICFES")
        print("Base de datos creada correctamente.")

    except OperationalError as e:
        print(f"Error: {e}")

create_database()