import streamlit as st
from Querys import *
from conexion import *
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import json

def mostrar_datos(conexion):
    # Gráfica para todos los datos
    df_all = consulta_todos_los_datos(conexion)
    if df_all is not None:
        st.subheader('Base de datos')
        st.write(df_all.head())
    else:
        st.error('No se pudieron obtener los resultados para todos los datos')

def g_puntajeProm_Asig_periodo(conexion):
    
    # Gráfica para el puntaje promedio por periodo
    df_punt = consulta_puntaje_promedio_por_periodo(conexion)
    if df_punt is not None:
        st.subheader('Puntaje promedio de las Asignaturas')
        # Obtener los períodos disponibles
        periodos_disponibles = [20151, 20152, 20161, 20162, 20171, 20172, 20181, 20191,\
                                20194, 20201, 20211, 20221, 20224]

        # Widget para seleccionar el período
        periodo_seleccionado = st.select_slider("Seleccione el período:", options=periodos_disponibles)

        # Filtrar el DataFrame para el período seleccionado
        df_periodo_seleccionado = df_punt[df_punt['periodo'] == periodo_seleccionado]

        if not df_periodo_seleccionado.empty:
            # Eliminar la columna de PERIODO para evitar duplicados
            df_periodo_seleccionado = df_periodo_seleccionado.drop(columns=['periodo'])

            # Convertir el DataFrame a un formato adecuado para la gráfica de barras
            df_melted = df_periodo_seleccionado.melt(var_name='asignatura', value_name='promedio')

            # Crear gráfico interactivo de barras con Plotly
            fig = px.bar(df_melted, x='asignatura', y='promedio', color='asignatura',
                        title=f"Promedio de Puntaje por periodo {periodo_seleccionado}",
                        labels={"promedio": "Promedio de Puntaje"},
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

def g_puntajeProm_Estrato(conexion):

    # Gráfica para el puntaje promedio por estrato
    df_estrato = consulta_puntaje_promedio_por_estrato(conexion)
    if df_estrato is not None:
        st.subheader('Puntaje promedio por Estrato')
        st.write('Por favor seleccione el número de estrato para observar la gráfica.')

        # Obtener la lista de estratos únicos
        estratos = df_estrato['fami_estratovivienda'].unique()
        # Crear el Sunburst
        fig = px.sunburst(df_estrato, path=['fami_estratovivienda', 'cole_area_ubicacion'], values='puntaje_promedio')
        # Mostrar el Sunburst 
        st.plotly_chart(fig)
        
    else:
        st.error('No se pudieron obtener los resultados para el puntaje promedio por estrato')
    
def g_puntajeProm_Dept(conexion):

    # Gráfico para el puntaje promedio por departamento
    df_depto = consulta_puntaje_promedio_por_departamento(conexion)

    if df_depto is not None:
        departamentos = df_depto['cole_depto_ubicacion'].unique() 
        st.subheader('Puntaje promedio por Departamento')

        select_depto = st.multiselect('Seleccione departamentos para observar la gráfica', departamentos)

        # Obtener los datos de los departamentos seleccionados y ordenarlos por el eje x (periodo)
        data_seleccionado = df_depto[df_depto['cole_depto_ubicacion'].isin(select_depto)].sort_values(by='periodo')
        data_seleccionado['periodo'] = data_seleccionado['periodo'].astype(str)

        traces = []
        for depto in select_depto:
            trace = go.Scatter(
                y=data_seleccionado[data_seleccionado['cole_depto_ubicacion'] == depto]['puntaje_promedio'].values,
                x=data_seleccionado[data_seleccionado['cole_depto_ubicacion'] == depto]['periodo'],
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
        st.error('No se pudieron obtener los resultados para el puntaje promedio por departamento')

def g_puntajeProm_genero(conexion):

    # Gráfica para el puntaje promedio por género
    df_acceso_genero = consulta_puntaje_promedio_por_genero(conexion)
    if not df_acceso_genero.empty:
        st.subheader("Puntaje promedio por Genero")  

        # Widget para seleccionar el tipo de promedio
        promedio_selector = st.radio("Selecciona el tipo de promedio:", 
                                ["promedio_puntaje_ingles", "promedio_puntaje_ciencias_naturales", 
                                "promedio_puntaje_lectura_critica", "promedio_puntaje_matematicas", 
                                "promedio_puntaje_sociales_ciudadanas", "puntaje_promedio_total"])
        if promedio_selector: 
            # Crear gráfico de barras con Plotly
            fig = px.bar(df_acceso_genero, x="estu_genero", y=promedio_selector, color="estu_genero",
                        labels={"value": "Promedio de puntaje", "estu_genero": "Género"},
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

def consulta_global_municipios(conexion):

    st.header("Gráficos para los puntajes globales por género y período para cada departamento/municipio")

    df_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_global_deptmun.empty:
        st.subheader("Para las siguientes gráficas seleccione el departamento/municipio que desea consultar:")
        # Se agregan widgets de selección para el departamento y municipio
        departamento_seleccionado = st.selectbox("Selecciona un departamento", df_global_deptmun['cole_depto_ubicacion'].unique())
        municipio_seleccionado = st.selectbox("Selecciona un municipio", df_global_deptmun[df_global_deptmun['cole_depto_ubicacion'] == departamento_seleccionado]['cole_mcpio_ubicacion'].unique())
    else:
        st.error('No se pudieron obtener resultados de la consulta')


        #######################################################################################################################################################
        #######################################################################################################################################################	
        #######################################################################################################################################################
        #######################################################################################################################################################
    

def g_ba_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado):
    st.text("")
        # Gráfico de barras apiladas de puntajes globales por género y período para cada departamento/municipio
    df_bar_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_bar_global_deptmun.empty:
        st.subheader("Gráfico de Barras Apiladas")

        # Se filtran los datos según la selección
        df_filtrado = df_bar_global_deptmun[(df_bar_global_deptmun['cole_depto_ubicacion'] == departamento_seleccionado) & (df_bar_global_deptmun['cole_mcpio_ubicacion'] == municipio_seleccionado)]

        # Creación del gráfico de barras apiladas
        barras_apiladas = alt.Chart(df_filtrado).mark_bar().encode(x='periodo:N', y='punt_global:Q', color='estu_genero:N', tooltip=['punt_global:Q', 'periodo:N', 'estu_genero:N']).properties(width=400, height=300)

        # Mostrar el gráfico en Streamlit
        st.altair_chart(barras_apiladas)
    else:
        st.error('No se pudieron obtener resultados de la consulta')

def g_linea_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado):
    st.text("")

    #Gráfico de líneas acerca de los puntajes globales por genero y período para cada departamento/municipio
    df_lin_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_lin_global_deptmun.empty:
        st.subheader("Gráfico de Líneas")
        
        # Se filtran los datos según la selección
        df_filtrado = df_lin_global_deptmun[(df_lin_global_deptmun['cole_depto_ubicacion'] == departamento_seleccionado) & (df_lin_global_deptmun['cole_mcpio_ubicacion'] == municipio_seleccionado)]

        # Creación del gráfico de lineas
        grafico_lineas = alt.Chart(df_filtrado).mark_line().encode(x='periodo:N', y='punt_global:Q', color='estu_genero:N', tooltip=['punt_global:Q', 'periodo:N', 'estu_genero:N']).properties(width=400, height=300)

        # Mostrar el gráfico en Streamlit
        st.altair_chart(grafico_lineas)
    else:
        st.error('No se pudieron obtener resultados de la consulta')

def g_areaapiladas_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado):
    st.text("")

    # Gráfico de areas apiladas de puntajes globales por género y período para cada departamento/municipio
    df_are_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_are_global_deptmun.empty:
        st.subheader("Gráfico de Areas Apiladas")
        
        # Se filtran los datos según la selección
        df_filtrado = df_are_global_deptmun[(df_are_global_deptmun['cole_depto_ubicacion'] == departamento_seleccionado) & (df_are_global_deptmun['cole_mcpio_ubicacion'] == municipio_seleccionado)]

        # Creación del gráfico de areas apiladas
        areas_apiladas = alt.Chart(df_filtrado).mark_area().encode(x='periodo:N', y=alt.Y('punt_global:Q', stack=None), color='estu_genero:N', tooltip=['punt_global:Q', 'periodo:N', 'estu_genero:N']).properties(width=400, height=300)

        # Mostrar el gráfico en Streamlit
        st.altair_chart(areas_apiladas)
    else:
        st.error('No se pudieron obtener resultados de la consulta')

def g_dipersion_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado):
    st.text("")
    df_disp_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_disp_global_deptmun.empty:
        st.subheader("Gráfico de Dispersión")
        
        # Se filtran los datos según la selección
        df_filtrado = df_disp_global_deptmun[(df_disp_global_deptmun['cole_depto_ubicacion'] == departamento_seleccionado) & (df_disp_global_deptmun['cole_mcpio_ubicacion'] == municipio_seleccionado)]

        # Creación del gráfico de dispersión
        dispersion_deptmun = alt.Chart(df_filtrado).mark_point().encode(x='periodo:N', y='punt_global:Q', color='estu_genero:N', tooltip=['punt_global:Q', 'periodo:N', 'estu_genero:N']).properties(width=400, height=300).interactive()

        # Mostrar el gráfico en Streamlit
        st.altair_chart(dispersion_deptmun)
    else:
        st.error('No se pudieron obtener resultados de la consulta')


        #######################################################################################################################################################
        #######################################################################################################################################################
        #######################################################################################################################################################
        #######################################################################################################################################################
        

def g_puntajeProm_barranquilla(conexion):

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
            grafica = alt.Chart(df_area_global_baq).mark_area().encode(x='periodo', y='punt_global')
            st.altair_chart(grafica, use_container_width=True)
        else:
            st.error('No se pudieron obtener resultados de la consulta')       

    elif opcion_graficas_baq == "Histograma":

        # Histograma de puntajes globales por período en Barranquilla
        df_hist_global_baq = consulta_puntaje_global_barranquilla_por_periodo(conexion)
        if not df_hist_global_baq.empty:
            st.subheader("Histograma de puntajes globales por período en Barranquilla")
            # Crear el histograma
            histograma = alt.Chart(df_hist_global_baq).mark_bar().encode(alt.X("punt_global:Q", bin=alt.Bin(step=50)), y='count()', color='periodo:N').properties(width=600, height=400)
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
            dispersion = alt.Chart(df_disp_global_baq).mark_circle().encode(x='punt_global:Q', y='estu_genero:N', color='estu_genero:N',tooltip=['punt_global:Q', 'estu_genero:N']).properties(width=600, height=400)
            # Mostrar el gráfico en Streamlit
            st.altair_chart(dispersion)
        else:
            st.error('No se pudieron obtener resultados de la consulta')
    else:
         st.error('No se pudieron obtener resultados de la seleccíon')



def dibujar_mapa(conexion):
    st.header("Mapa de los puntajes globales por municipio")
    df = consulta_puntaje_global_por_municipio(conexion)
    st.write(df)
    # Cargar el archivo GeoJSON más detallado
    geojson = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
    
    #Cargar el archivo GeoJSON local
    #with open('Backend/src/Colombia.geo.json') as f:
    #    geojson = json.load(f)
    # Crear la gráfica de dispersión geográfica con el archivo GeoJSON más detallado
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='departamento', color='puntaje_global',
                                featureidkey='properties.NOMBRE_DPT', mapbox_style="carto-positron",
                                center={"lat": 10.074048, "lon": -74.601469}, zoom=5,
                                opacity=0.5, labels={'puntaje_global':'Puntaje Global'},
                                color_continuous_scale="Viridis")
    

    # Mostrar la gráfica
    st.plotly_chart(fig)
