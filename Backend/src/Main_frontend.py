import streamlit as st
from Querys import consulta_todos_los_datos, consulta_puntaje_promedio_por_periodo, consulta_puntaje_promedio_por_estrato, consulta_puntaje_promedio_por_departamento, consulta_puntaje_promedio_por_acceso_a_recursos
from conexion_db import conectar_servidor
import plotly.graph_objects as go


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
        departamentos = df_depto['COLE_DEPTO_UBICACION'].unique() 
        st.subheader('Gráfico para el puntaje promedio por departamentos')
        select_depto = st.multiselect('Seleccione los departamentos', departamentos)

        if select_depto:
            traces = []
            for depto in select_depto:
                trace = go.Scatter(
                    y=df_depto[df_depto['COLE_DEPTO_UBICACION'] == depto]['PERIODO'].values,
                    x=df_depto[df_depto['COLE_DEPTO_UBICACION'] == depto]['Puntaje_Promedio'].values,
                    mode='lines',
                    name=depto,
                    visible=True
                )
                traces.append(trace)
            fig = go.Figure(traces)

            fig.update_layout(
                title='Promedio de los estudiantes por departamento',
                yaxis_title='PERIODO',
                xaxis_title='Puntaje Promedio'
            )

            st.plotly_chart(fig)
        else:
            st.write('Por favor seleccione departamentos para observar la gráfica.')  
    
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
