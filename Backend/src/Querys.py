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
            SELECT 
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
            FROM resultados_icfes
            LIMIT 100;
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_periodo(conexion):
    query = '''
            SELECT "periodo", AVG("punt_ingles") AS "puntaje_ingles",
                AVG("punt_c_naturales") AS "puntaje_ciencias_naturales",
                AVG("punt_lectura_critica") AS "puntaje_lectura_critica",
                AVG("punt_matematicas") AS "puntaje_matematicas",
                AVG("punt_sociales_ciudadanas") AS "puntaje_sociales_ciudadanas"
            FROM "resultados_icfes"
            GROUP BY "periodo"
            ORDER BY "periodo"
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_estrato(conexion):
    query = '''
            SELECT fami_estratovivienda, cole_area_ubicacion, 
                AVG(punt_global) AS puntaje_promedio
            FROM resultados_icfes
            WHERE fami_estratovivienda IS NOT NULL
            GROUP BY fami_estratovivienda, cole_area_ubicacion
            ORDER BY fami_estratovivienda
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_departamento(conexion):
    query = '''
            SELECT periodo, cole_depto_ubicacion, AVG(punt_global) AS puntaje_promedio
            FROM resultados_icfes
            GROUP BY periodo, cole_depto_ubicacion
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_genero(conexion):
    query = '''
            SELECT estu_genero,
            AVG(punt_ingles) AS promedio_puntaje_ingles,
            AVG(punt_c_naturales) AS promedio_puntaje_ciencias_naturales,
            AVG(punt_lectura_critica) AS promedio_puntaje_lectura_critica,
            AVG(punt_matematicas) AS promedio_puntaje_matematicas,
            AVG(punt_sociales_ciudadanas) AS promedio_puntaje_sociales_ciudadanas,
            AVG(punt_global)/500.0 *100 AS puntaje_promedio_total
        FROM resultados_icfes
        GROUP BY estu_genero
            '''
    return realizar_consulta(conexion, query)

def consulta_punt_prom_departamento(conexion):
    query = '''
            SELECT cole_depto_ubicacion, AVG(punt_global) as puntaje_prom
            FROM resultados_icfes
            GROUP BY cole_depto_ubicacion
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_global_barranquilla_por_periodo(conexion):
    query = '''
            SELECT r.periodo, r.cole_depto_ubicacion, r.cole_mcpio_ubicacion, r.estu_genero, r.cole_genero, r.punt_global
            FROM resultados_icfes r
            WHERE r.cole_mcpio_ubicacion LIKE '%BARRANQUILLA'
            GROUP BY r.periodo, r.cole_depto_ubicacion, r.cole_mcpio_ubicacion, r.estu_genero, r.cole_genero, r.punt_global
            ORDER BY r.punt_global DESC
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_global_por_periodo(conexion):
    query = '''
            SELECT r.periodo, r.cole_depto_ubicacion, r.cole_mcpio_ubicacion, r.estu_genero, r.cole_genero, r.punt_global
            FROM resultados_icfes r
            GROUP BY r.periodo, r.cole_depto_ubicacion, r.cole_mcpio_ubicacion, r.estu_genero, r.cole_genero, r.punt_global
            ORDER BY r.punt_global DESC
            '''
    return realizar_consulta(conexion, query)

def consulta_puntaje_global_por_municipio(conexion):
    query = '''
            SELECT cole_depto_ubicacion AS departamento, AVG(punt_global) AS puntaje_global
            FROM resultados_icfes
            GROUP BY cole_depto_ubicacion
            '''
    return realizar_consulta(conexion, query)