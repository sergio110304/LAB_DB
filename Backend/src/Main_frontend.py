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
        st.subheader('Resultados de la consulta para el puntaje promedio por asignaruras en cada periodo')
        # Obtener los períodos disponibles
        periodos_disponibles = [20151, 20152, 20161, 20162, 20171, 20172, 20181, 20191,\
                                20194, 20201, 20211, 20221, 20224]

        # Widget para seleccionar el período
        periodo_seleccionado = st.select_slider("Seleccione el período:", options=periodos_disponibles)

        # Filtrar el DataFrame para el período seleccionado
        df_periodo_seleccionado = df_punt[df_punt['PERIODO'] == periodo_seleccionado]

        if not df_periodo_seleccionado.empty:
            # Eliminar la columna de PERIODO para evitar duplicados
            df_periodo_seleccionado = df_periodo_seleccionado.drop(columns=['PERIODO'])

            # Convertir el DataFrame a un formato adecuado para la gráfica de barras
            df_melted = df_periodo_seleccionado.melt(var_name='Asignatura', value_name='Promedio')

            # Crear gráfico interactivo de barras con Plotly
            fig = px.bar(df_melted, x='Asignatura', y='Promedio', color='Asignatura',
                        title=f"Promedio de Puntaje por periodo {periodo_seleccionado}",
                        labels={"Promedio": "Promedio de Puntaje"},
                        template="plotly_white")

            fig.update_layout(transition_duration=500)
            # Agregar ejes y títulos
            fig.update_xaxes(title="Asignatura")
            fig.update_yaxes(title="Puntajes (Percentil)", range=[0, 90]) 

            # Mostrar el gráfico 
            st.plotly_chart(fig)
        else:
            st.write("No hay datos disponibles para el período seleccionado.")
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

            # Configurar animación
            fig.update_layout(transition_duration=500)

            fig.update_yaxes(range=[0, 50])

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
