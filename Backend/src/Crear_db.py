import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

def create_database():
    try:
        # Conectarse a PostgreSQL en la nube
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME_dflt"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
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