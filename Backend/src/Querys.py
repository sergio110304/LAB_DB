import pandas as pd
from conexion_db import conectar_servidor

def realizar_consulta(conexion, query):
    if conexion:
        try:
            cursor = conexion.cursor()
            df_resultados = pd.read_sql(query, conexion)
            cursor.close()
            return df_resultados
        except Exception as e:
            print('Error al realizar la consulta:', e)
            return None
    else:
        return None

def consulta_todos_los_datos(conexion):
    query = 'SELECT * FROM Resultados_Saber_11_R_Caribe_2015_2022'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_periodo(conexion):
    query = 'SELECT PERIODO, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY PERIODO ORDER BY PERIODO'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_estrato(conexion):
    query = 'SELECT FAMI_ESTRATOVIVIENDA, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY FAMI_ESTRATOVIVIENDA'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_departamento(conexion):
    query = 'SELECT COLE_DEPTO_UBICACION, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY COLE_DEPTO_UBICACION'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_acceso_a_recursos(conexion):
    query = 'SELECT FAMI_TIENECOMPUTADOR, FAMI_TIENEINTERNET, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY FAMI_TIENEAUTOMOVIL, FAMI_TIENECOMPUTADOR, FAMI_TIENEINTERNET'
    return realizar_consulta(conexion, query)

# Main
if __name__ == "__main__":
    conexion = conectar_servidor()
    if conexion:
        df_all = consulta_todos_los_datos(conexion)
        if df_all is not None:
            print("Resultados de la consulta para todos los datos:")
            print(df_all.head())
        else:
            print('No se pudieron obtener los resultados para todos los datos')

        df_punt = consulta_puntaje_promedio_por_periodo(conexion)
        if df_punt is not None:
            print("\nResultados de la consulta para el puntaje promedio por periodo:")
            print(df_punt.head())
        else:
            print('No se pudieron obtener los resultados para el puntaje promedio por periodo')

        df_estrato = consulta_puntaje_promedio_por_estrato(conexion)
        if df_estrato is not None:
            print("\nResultados de la consulta para el puntaje promedio por estrato:")
            print(df_estrato.head())
        else:
            print('No se pudieron obtener los resultados para el puntaje promedio por estrato')

        df_depto = consulta_puntaje_promedio_por_departamento(conexion)
        if df_depto is not None:
            print("\nResultados de la consulta para el puntaje promedio por departamento:")
            print(df_depto.head())
        else:
            print('No se pudieron obtener los resultados para el puntaje promedio por departamento')

        df_acceso = consulta_puntaje_promedio_por_acceso_a_recursos(conexion)
        if df_acceso is not None:
            print("\nResultados de la consulta para el puntaje promedio por acceso a recursos:")
            print(df_acceso.head())
        else:
            print('No se pudieron obtener los resultados para el puntaje promedio por acceso a recursos')

        conexion.close()
    else:
        print('No se pudo establecer la conexión')
