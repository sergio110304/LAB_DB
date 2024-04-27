import streamlit as st
import pandas as pd

def realizar_consulta(conexion, query):
    if conexion:
        try:
            cursor = conexion.cursor()
            df_resultados = pd.read_sql(query, conexion)
            cursor.close()
            return df_resultados
        except Exception as e:
            st.error(f'Error al realizar la consulta: {e}')
            return None
    else:
        st.error('No se pudo establecer la conexión')
        return None

def consulta_todos_los_datos(conexion):
    query = '''
            SELECT TOP (100) [PERIODO]
                ,[ESTU_TIPODOCUMENTO]
                ,[ESTU_CONSECUTIVO]
                ,[COLE_AREA_UBICACION]
                ,[COLE_BILINGUE]
                ,[COLE_CALENDARIO]
                ,[COLE_COD_DEPTO_UBICACION]
                ,[COLE_CODIGO_ICFES]
                ,[COLE_DEPTO_UBICACION]
                ,[COLE_GENERO]
                ,[ESTU_FECHANACIMIENTO]
                ,[ESTU_GENERO]
                ,[ESTU_NACIONALIDAD]
                ,[FAMI_ESTRATOVIVIENDA]
                ,[FAMI_TIENEAUTOMOVIL]
                ,[FAMI_TIENECOMPUTADOR]
                ,[FAMI_TIENEINTERNET]
                ,[FAMI_TIENELAVADORA]
                ,[DESEMP_INGLES]
                ,[PUNT_INGLES]
                ,[PUNT_MATEMATICAS]
                ,[PUNT_SOCIALES_CIUDADANAS]
                ,[PUNT_C_NATURALES]
                ,[PUNT_LECTURA_CRITICA]
                ,[PUNT_GLOBAL]
                ,[COLE_MCPIO_UBICACION]
                ,[COLE_COD_MCPIO_UBICACION]
            FROM [LAB_ICFES].[dbo].[Resultados_Saber_11_R_Caribe_2015_2022]
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_periodo(conexion):
    query = '''
            SELECT PERIODO, AVG(PUNT_GLOBAL) AS Puntaje_Promedio 
            FROM Resultados_Saber_11_R_Caribe_2015_2022 
            GROUP BY PERIODO 
            ORDER BY PERIODO
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_estrato(conexion):
    query = '''
            SELECT FAMI_ESTRATOVIVIENDA, AVG(PUNT_GLOBAL) AS Puntaje_Promedio 
            FROM Resultados_Saber_11_R_Caribe_2015_2022 
            GROUP BY FAMI_ESTRATOVIVIENDA
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_departamento(conexion):
    query = '''
            SELECT PERIODO, COLE_DEPTO_UBICACION, AVG(PUNT_GLOBAL) AS Puntaje_Promedio
            FROM Resultados_Saber_11_R_Caribe_2015_2022 
            GROUP BY PERIODO, COLE_DEPTO_UBICACION
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_genero(conexion):
    query = '''
            SELECT ESTU_GENERO,
                AVG(PUNT_INGLES) AS Promedio_Puntaje_Ingles,
                AVG(PUNT_C_NATURALES) AS Promedio_Puntaje_Ciencias_Naturales,
                AVG(PUNT_LECTURA_CRITICA) AS Promedio_Puntaje_Lectura_Critica,
                AVG(PUNT_MATEMATICAS) AS Promedio_Puntaje_Matematicas,
                AVG(PUNT_SOCIALES_CIUDADANAS) AS Promedio_Puntaje_Sociales_Ciudadanas,
                AVG(PUNT_GLOBAL) AS Puntaje_Promedio_Total
            FROM Resultados_Saber_11_R_Caribe_2015_2022
            GROUP BY ESTU_GENERO;
            '''
    return realizar_consulta(conexion, query)
