import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
from conexion_db import conectar_servidor
import plotly.express as px
import plotly.graph_objects as go

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
    query = 'SELECT * FROM Resultados_Saber_11_R_Caribe_2015_2022'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_periodo(conexion):
    query = 'SELECT PERIODO, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY PERIODO ORDER BY PERIODO'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_estrato(conexion):
    query = 'SELECT FAMI_ESTRATOVIVIENDA, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY FAMI_ESTRATOVIVIENDA'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_departamento(conexion):
    query = 'SELECT PERIODO, COLE_DEPTO_UBICACION, AVG(PUNT_GLOBAL) AS Puntaje_Promedio\
            FROM Resultados_Saber_11_R_Caribe_2015_2022 \
            GROUP BY PERIODO, COLE_DEPTO_UBICACION'
    return realizar_consulta(conexion, query)

def consulta_puntaje_promedio_por_acceso_a_recursos(conexion):
    query = 'SELECT FAMI_TIENECOMPUTADOR, FAMI_TIENEINTERNET, AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY FAMI_TIENECOMPUTADOR, FAMI_TIENEINTERNET'
    return realizar_consulta(conexion, query)


# Main
if __name__ == "__main__":
    conexion = conectar_servidor() # Conexión a la base de datos
    # Título del dashboard
    st.title('Resultados Prueba Saber 2015-2022 REGIÓN CARIBE')

    with st.sidebar:
        st.write("Información sobre el proyecto")
        st.write("Es un dashboard que presenta cinco gráficas interactivas sobre los resultados de las\
                pruebas saber desde el 2015 hasta el 2022, especifícamente de \
                la  Región Caribe de Colombia. ")
        
    st.markdown("---")

    # Gráfica para todos los datos
    df_all = consulta_todos_los_datos(conexion)
    if df_all is not None:
        st.subheader('Resultados de la consulta para todos los datos')
        st.write(df_all.head())
    else:
        st.error('No se pudieron obtener los resultados para todos los datos')

    st.markdown("---")

    # Gráfica para el puntaje promedio por periodo
    df_punt = consulta_puntaje_promedio_por_periodo(conexion)
    if df_punt is not None:
        st.subheader('Resultados de la consulta para el puntaje promedio por periodo')
        st.write(df_punt.head())
    else:
        st.error('No se pudieron obtener los resultados para el puntaje promedio por periodo')

    st.markdown("---") 

    # Gráfica para el puntaje promedio por estrato
    df_estrato = consulta_puntaje_promedio_por_estrato(conexion)
    if df_estrato is not None:
        st.subheader('Resultados de la consulta para el puntaje promedio por estrato')
        st.write(df_estrato.head())
    else:
        st.error('No se pudieron obtener los resultados para el puntaje promedio por estrato')

    # Gráfico para el puntaje promedio por departamento
    df_depto = consulta_puntaje_promedio_por_departamento(conexion)
    if df_depto is not None:
        # operaciones por departamento
        departamentos = df_depto['COLE_DEPTO_UBICACION'].unique() 
        st.subheader('Gráfico para el puntaje promedio por departamentos')
        select_depto = st.multiselect('Seleccione los departamentos', departamentos)

        if select_depto:
            traces = []
            for depto in select_depto:
                trace = go.Scatter(x=df_depto[df_depto['COLE_DEPTO_UBICACION'] == depto]['Puntaje_Promedio'].value_counts().sort_index(ascending=True).index,
                                    y=df_depto[df_depto['COLE_DEPTO_UBICACION'] == depto]['Puntaje_Promedio'].value_counts().sort_index(ascending=True).values,
                                    mode='lines',
                                    name=depto,
                                    visible=True)  
                traces.append(trace)
            fig = go.Figure(traces)

            fig.update_layout(title='Promedio de los estudiantes sobre los departamentos ',
                                xaxis_title='Promedio',
                                yaxis_title= 'PERIODO')

            st.plotly_chart(fig)
        else:
            st.write('Porfavor seleccione departamentos para observar la gráfica.')  
    
    else:
        st.error('No se pudieron obtener los resultados para el puntaje promedio por departamento')

    # Gráfica para el puntaje promedio por acceso a recursos
    df_acceso_recursos = consulta_puntaje_promedio_por_acceso_a_recursos(conexion)
    if not df_acceso_recursos.empty:
        st.subheader("Gráfico para el puntaje promedio por acceso a recursos  ")  
        st.write("Resultados de la consulta:")
        st.write(df_acceso_recursos.head())

    else:
        st.error('No se pudieron obtener resultados de la consulta')

    # Cerrar conexión a la base de datos
    conexion.close()

else:
    st.error('No se pudo establecer la conexión a la base de datos')
