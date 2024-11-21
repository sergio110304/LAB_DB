import csv
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

def create_table():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        conn.autocommit = True
        # Crear un cursor
        cursor = conn.cursor()

        # Crear una tablawith open('Backend\\src\\Resultados_Saber_11_R_Caribe_2015_2022.csv', 'r', encoding='ISO-8859-1') as f:
        print("Tabla creada correctamente.")

        # Leer el archivo CSV y insertar los datos
        with open('Backend\\src\\Resultados_Saber_11_R_Caribe_2015_2022.csv', 'r', encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Saltar la cabecera
            for row in reader:
                row = [None if x == '' or x.isspace() else x for x in row]
                # Convertir la fecha a 'YYYY-MM-DD'
                fecha = datetime.strptime(row[10], '%d/%m/%Y').strftime('%Y-%m-%d')
                row[10] = fecha
                cursor.execute(
                                """
                                INSERT INTO resultados_icfes (
                                    PERIODO,
                                    ESTU_TIPODOCUMENTO,
                                    ESTU_CONSECUTIVO,
                                    COLE_AREA_UBICACION,
                                    COLE_BILINGUE,
                                    COLE_CALENDARIO,
                                    COLE_COD_DEPTO_UBICACION,
                                    COLE_CODIGO_ICFES,
                                    COLE_DEPTO_UBICACION,
                                    COLE_GENERO,
                                    ESTU_FECHANACIMIENTO,
                                    ESTU_GENERO,
                                    ESTU_NACIONALIDAD,
                                    FAMI_ESTRATOVIVIENDA,
                                    FAMI_TIENEAUTOMOVIL,
                                    FAMI_TIENECOMPUTADOR,
                                    FAMI_TIENEINTERNET,
                                    FAMI_TIENELAVADORA,
                                    DESEMP_INGLES,
                                    PUNT_INGLES,
                                    PUNT_MATEMATICAS,
                                    PUNT_SOCIALES_CIUDADANAS,
                                    PUNT_C_NATURALES,
                                    PUNT_LECTURA_CRITICA,
                                    PUNT_GLOBAL,
                                    COLE_MCPIO_UBICACION,
                                    COLE_COD_MCPIO_UBICACION
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                row
                            )
        print("Datos insertados correctamente.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_table()
