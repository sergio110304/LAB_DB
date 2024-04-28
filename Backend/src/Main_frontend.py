import streamlit as st
from Querys import *
from conexion_db import *
import plotly.graph_objects as go
import plotly.express as px
import folium
import pandas as pd
import altair as alt

# Main
if __name__ == "__main__":
    conexion = conectar_servidor() # Conexión a la base de datos
    # Título del dashboard
    st.markdown(
        """
        <div style='background-color: #F63366; padding: 10px;'>
            <h1 style='color: white; text-align: center;'>Resultados Prueba Saber 2015-2022 REGIÓN CARIBE</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.write("Información sobre el proyecto:")
        st.write("Es un dashboard que presenta gráficas interactivas sobre los resultados de las\
                pruebas saber desde el 2015 hasta el 2022, especifícamente de \
                la  Región Caribe de Colombia. ")
        
    st.markdown("---")
    # Gráfica para todos los datos
    df_all = consulta_todos_los_datos(conexion)
    if df_all is not None:
        st.subheader('Visualización de la base de datos')
        st.write(df_all.head())
    else:
        st.error('No se pudieron obtener los resultados para todos los datos')

    st.markdown("---")
    
    # Gráfica para el puntaje promedio por periodo
    df_punt = consulta_puntaje_promedio_por_periodo(conexion)
    if df_punt is not None:
        st.subheader('Gráfico para el puntaje promedio por asignaturas en cada periodo')
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
        st.subheader('Gráfico para el puntaje promedio por estrato')
        st.write('Por favor seleccione el número de estrato para observar la gráfica.')

        # Obtener la lista de estratos únicos
        estratos = df_estrato['FAMI_ESTRATOVIVIENDA'].unique()
        # Crear el Sunburst
        fig = px.sunburst(df_estrato, path=['FAMI_ESTRATOVIVIENDA', 'COLE_AREA_UBICACION'], values='Puntaje_Promedio')
        # Mostrar el Sunburst 
        st.plotly_chart(fig)
        
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
            # Obtener los datos de los departamentos seleccionados y ordenarlos por el eje x (PERIODO)
            data_seleccionado = df_depto[df_depto['COLE_DEPTO_UBICACION'].isin(select_depto)].sort_values(by='PERIODO')
            data_seleccionado['PERIODO'] = data_seleccionado['PERIODO'].astype(str)

            traces = []
            for depto in select_depto:
                trace = go.Scatter(
                    y=data_seleccionado[data_seleccionado['COLE_DEPTO_UBICACION'] == depto]['Puntaje_Promedio'].values,
                    x=data_seleccionado[data_seleccionado['COLE_DEPTO_UBICACION'] == depto]['PERIODO'],
                    mode='lines+markers',
                    name=depto,
                    visible=True
                )
                traces.append(trace)

            fig = go.Figure(traces)

            fig.update_layout(
                title='Promedio de los estudiantes por departamento',
                yaxis_title='Puntaje Promedio',
                xaxis_title='Periodo',
                xaxis=dict(type='category')  # Tipo de eje x como 'category' para que se traten los valores como cadenas de texto
            )

            st.plotly_chart(fig)

        else:
            st.write('Por favor seleccione uno o más departamentos para observar la gráfica.')

    else:
        st.error('No se pudieron obtener los resultados para el puntaje promedio por departamento')


    '''
    # Cargar datos geoespaciales desde el archivo JSON
    st.subheader('Mapa de Resultados Globales en la región Caribe de Colombia')

    with open("Backend\src\Colombia.geo.json", "r") as file:
        geojson_data = file.read()

    # Crear el mapa con Folium
    m = folium.Map(location=[10.195679, -74.516440], zoom_start=6.45)

    df_depa_prom = consulta_punt_prom_departamento(conexion)

    # Añadir datos geoespaciales al mapa
    folium.GeoJson(geojson_data).add_to(m)

    # Crear una capa de coropleta para mostrar los puntajes globales por departamento
    folium.Choropleth(
        geo_data=geojson_data,
        name='Puntaje Global por Departamento',
        data=df_depa_prom,
        columns=['COLE_DEPTO_UBICACION', 'Puntaje_Prom'],
        key_on='feature.properties.NOMBRE_DPT',
        fill_color='YlGn',
        fill_opacity=0.9,
        line_opacity=0.5,
        legend_name='Puntaje Global por Departamento',
    ).add_to(m)

    # Mostrar el mapa en Streamlit
    #st.components.v1.html(m._repr_html_(), width=700, height=500)
    '''


    st.markdown("---") 
    # Gráfica para el puntaje promedio por género
    df_acceso_genero = consulta_puntaje_promedio_por_genero(conexion)
    if not df_acceso_genero.empty:
        st.subheader("Gráfico para el puntaje promedio por género para cada asignatura")  

        # Widget para seleccionar el tipo de promedio
        promedio_selector = st.radio("Seleccione la asignatura:", 
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
            st.write('Por favor seleccione una asignatura para observar la gráfica.')  

    else:
        st.error('No se pudieron obtener resultados de la consulta')

    #*****************************************************************************************************
    st.markdown("---")
    st.header("Gráficos para los puntajes globales por género y período para cada departamento/municipio")

    df_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_global_deptmun.empty:
        st.subheader("Para las siguientes gráficas seleccione el departamento/municipio que desea consultar:")
        # Se agregan widgets de selección para el departamento y municipio
        departamento_seleccionado = st.selectbox("Selecciona un departamento", df_global_deptmun['COLE_DEPTO_UBICACION'].unique())
        municipio_seleccionado = st.selectbox("Selecciona un municipio", df_global_deptmun[df_global_deptmun['COLE_DEPTO_UBICACION'] == departamento_seleccionado]['COLE_MCPIO_UBICACION'].unique())
    else:
        st.error('No se pudieron obtener resultados de la consulta')
    
    st.text("")

    # Gráfico de barras apiladas de puntajes globales por género y período para cada departamento/municipio
    df_bar_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_bar_global_deptmun.empty:
        st.subheader("Gráfico de barras apiladas de puntajes globales por género y período para cada departamento/municipio")

        # Se filtran los datos según la selección
        df_filtrado = df_bar_global_deptmun[(df_bar_global_deptmun['COLE_DEPTO_UBICACION'] == departamento_seleccionado) & (df_bar_global_deptmun['COLE_MCPIO_UBICACION'] == municipio_seleccionado)]

        # Creación del gráfico de barras apiladas
        barras_apiladas = alt.Chart(df_filtrado).mark_bar().encode(x='PERIODO:N', y='PUNT_GLOBAL:Q', color='ESTU_GENERO:N', tooltip=['PUNT_GLOBAL:Q', 'PERIODO:N', 'ESTU_GENERO:N']).properties(width=600, height=400, title=f'Puntajes Globales por Género y Período en {municipio_seleccionado}, {departamento_seleccionado}')

        # Mostrar el gráfico en Streamlit
        st.altair_chart(barras_apiladas)
    else:
        st.error('No se pudieron obtener resultados de la consulta')

    st.text("")

    #Gráfico de líneas acerca de los puntajes globales por genero y período para cada departamento/municipio
    df_lin_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_lin_global_deptmun.empty:
        st.subheader("Gráfico de líneas acerca de los puntajes globales por genero y período para cada departamento/municipio")
        
        # Se filtran los datos según la selección
        df_filtrado = df_lin_global_deptmun[(df_lin_global_deptmun['COLE_DEPTO_UBICACION'] == departamento_seleccionado) & (df_lin_global_deptmun['COLE_MCPIO_UBICACION'] == municipio_seleccionado)]

        # Creación del gráfico de lineas
        grafico_lineas = alt.Chart(df_filtrado).mark_line().encode(x='PERIODO:N', y='PUNT_GLOBAL:Q', color='ESTU_GENERO:N', tooltip=['PUNT_GLOBAL:Q', 'PERIODO:N', 'ESTU_GENERO:N']).properties(width=600, height=400,title=f'Puntajes Globales por Género y Período en {municipio_seleccionado}, {departamento_seleccionado}')

        # Mostrar el gráfico en Streamlit
        st.altair_chart(grafico_lineas)
    else:
        st.error('No se pudieron obtener resultados de la consulta')

    st.text("")

    # Gráfico de areas apiladas de puntajes globales por género y período para cada departamento/municipio
    df_are_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_are_global_deptmun.empty:
        st.subheader("Gráfico de areas apiladas de puntajes globales por género y período para cada departamento/municipio")
        
        # Se filtran los datos según la selección
        df_filtrado = df_are_global_deptmun[(df_are_global_deptmun['COLE_DEPTO_UBICACION'] == departamento_seleccionado) & (df_are_global_deptmun['COLE_MCPIO_UBICACION'] == municipio_seleccionado)]

        # Creación del gráfico de areas apiladas
        areas_apiladas = alt.Chart(df_filtrado).mark_area().encode(x='PERIODO:N', y=alt.Y('PUNT_GLOBAL:Q', stack=None), color='ESTU_GENERO:N', tooltip=['PUNT_GLOBAL:Q', 'PERIODO:N', 'ESTU_GENERO:N']).properties(width=600, height=400, title=f'Puntajes Globales por Género y Período en {municipio_seleccionado}, {departamento_seleccionado}')

        # Mostrar el gráfico en Streamlit
        st.altair_chart(areas_apiladas)
    else:
        st.error('No se pudieron obtener resultados de la consulta')

    st.text("")

    # Gráfico de dispersión para los puntajes globales por género y período para cada departamento/municipio
    df_disp_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_disp_global_deptmun.empty:
        st.subheader("Gráfico de dispersión para los puntajes globales por género y período para cada departamento/municipio")
        
        # Se filtran los datos según la selección
        df_filtrado = df_disp_global_deptmun[(df_disp_global_deptmun['COLE_DEPTO_UBICACION'] == departamento_seleccionado) & (df_disp_global_deptmun['COLE_MCPIO_UBICACION'] == municipio_seleccionado)]

        # Creación del gráfico de dispersión
        dispersion_deptmun = alt.Chart(df_filtrado).mark_point().encode(x='PERIODO:N', y='PUNT_GLOBAL:Q', color='ESTU_GENERO:N', tooltip=['PUNT_GLOBAL:Q', 'PERIODO:N', 'ESTU_GENERO:N']).properties(width=600, height=400, title=f'Puntajes Globales por Género y Período en {municipio_seleccionado}, {departamento_seleccionado}').interactive()

        # Mostrar el gráfico en Streamlit
        st.altair_chart(dispersion_deptmun)
    else:
        st.error('No se pudieron obtener resultados de la consulta')
    
    #*****************************************************************************************************    
    st.markdown("---")
    st.header("Gráficos para los puntajes globales en Barranquilla")    

    # Menú de opciones para elegir cual gráfico mostrar
    opcion_graficas_baq = st.selectbox("Selecciona el tipo de gráfico", ["Gráfico de Areas", "Histograma", "Dispersión"])

    # Mostrar el gráfico correspondiente según la opción seleccionada
    if opcion_graficas_baq == "Gráfico de Areas":
        
        # Gráfica de area para analizar el puntaje global en Barranquilla por periodo
        df_area_global_baq = consulta_puntaje_global_barranquilla_por_periodo(conexion)
        if not df_area_global_baq.empty:
            st.subheader("Gráfico de area para los puntajes globales en Barranquilla por periodo")
            # Crear la gráfica de area
            grafica = alt.Chart(df_area_global_baq).mark_area().encode(x='PERIODO', y='PUNT_GLOBAL')
            st.altair_chart(grafica, use_container_width=True)
        else:
            st.error('No se pudieron obtener resultados de la consulta')       

    elif opcion_graficas_baq == "Histograma":

        # Histograma de puntajes globales por período en Barranquilla
        df_hist_global_baq = consulta_puntaje_global_barranquilla_por_periodo(conexion)
        if not df_hist_global_baq.empty:
            st.subheader("Histograma de puntajes globales por período en Barranquilla")
            # Crear el histograma
            histograma = alt.Chart(df_hist_global_baq).mark_bar().encode(alt.X("PUNT_GLOBAL:Q", bin=alt.Bin(step=50)), y='count()', color='PERIODO:N').properties(width=600, height=400)
            # Mostrar el gráfico en Streamlit
            st.altair_chart(histograma)
        else:
            st.error('No se pudieron obtener resultados de la consulta')
        
    elif opcion_graficas_baq == "Dispersión":

        # Gráfico de dispersión de puntajes globales por género en Barranquilla
        df_disp_global_baq = consulta_puntaje_global_barranquilla_por_periodo(conexion)
        if not df_disp_global_baq.empty:
            st.subheader("Gráfico de dispersión de puntajes globales por género en Barranquilla")
            # Crear el gráfico
            dispersion = alt.Chart(df_disp_global_baq).mark_circle().encode(x='PUNT_GLOBAL:Q', y='ESTU_GENERO:N', color='ESTU_GENERO:N',tooltip=['PUNT_GLOBAL:Q', 'ESTU_GENERO:N']).properties(width=600, height=400)
            # Mostrar el gráfico en Streamlit
            st.altair_chart(dispersion)
        else:
            st.error('No se pudieron obtener resultados de la consulta')
    else:
         st.error('No se pudieron obtener resultados de la seleccíon')

    # Cerrar conexión a la base de datos
    conexion.close()
else:
    st.error('No se pudo establecer la conexión a la base de datos')
