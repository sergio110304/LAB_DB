import streamlit as st
from Querys import consulta_todos_los_datos, consulta_puntaje_promedio_por_periodo, consulta_puntaje_promedio_por_estrato, consulta_puntaje_promedio_por_departamento, consulta_puntaje_promedio_por_genero
from conexion_db import conectar_servidor
import plotly.graph_objects as go
import plotly.express as px

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
    
    st.markdown("---") 
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
                    y=df_depto[df_depto['COLE_DEPTO_UBICACION'] == depto]['Puntaje_Promedio'].values,
                    x=df_depto[df_depto['COLE_DEPTO_UBICACION'] == depto]['PERIODO'].values,
                    mode='lines',
                    name=depto,
                    visible=True
                )
                traces.append(trace)
            fig = go.Figure(traces)

            fig.update_layout(
                title='Promedio de los estudiantes por departamento',
                yaxis_title='Puntaje Promedio',
                xaxis_title='Periodo'
            )

            st.plotly_chart(fig)
        else:
            st.write('Por favor seleccione departamentos para observar la gráfica.')  
    
    else:
        st.error('No se pudieron obtener los resultados para el puntaje promedio por departamento')
    
    st.markdown("---") 
    # Gráfica para el puntaje promedio por género
    df_acceso_genero = consulta_puntaje_promedio_por_genero(conexion)
    if not df_acceso_genero.empty:
        st.subheader("Gráfico para el puntaje promedio por género")  

        # Widget para seleccionar el tipo de promedio
        promedio_selector = st.radio("Selecciona el tipo de promedio:", 
                                ["Promedio_Puntaje_Ingles", "Promedio_Puntaje_Ciencias_Naturales", 
                                "Promedio_Puntaje_Lectura_Critica", "Promedio_Puntaje_Matematicas", 
                                "Promedio_Puntaje_Sociales_Ciudadanas", "Puntaje_Promedio_Total"])
        if promedio_selector: 
            # Crear gráfico de barras con Plotly
            fig = px.bar(df_acceso_genero, x="ESTU_GENERO", y=promedio_selector, color="ESTU_GENERO",
                        labels={"value": "Promedio de puntaje", "ESTU_GENERO": "Género"},
                        title=f"Promedio de puntaje por género ({promedio_selector})",
                        template="plotly_white")

            # Mostrar el gráfico de barras
            st.plotly_chart(fig)
        else: 
            st.write('Por favor seleccione un tipo de promedio para observar la gráfica.')  

    else:
        st.error('No se pudieron obtener resultados de la consulta')

    # Cerrar conexión a la base de datos
    conexion.close()

else:
    st.error('No se pudo establecer la conexión a la base de datos')
