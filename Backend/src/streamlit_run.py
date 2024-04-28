from Graficas_query import *
from conexion_db import conectar_servidor

def main():
    conexion = conectar_servidor() # se establece conexión

    # Título del dashboard
    st.title('Resultados Prueba Saber 2015-2022 REGIÓN CARIBE')

    with st.sidebar:
        st.write("Información sobre el proyecto")
        st.write("Es un dashboard que presenta gráficas interactivas sobre los resultados de las\
                pruebas saber desde el 2015 hasta el 2022, especifícamente de \
                la  Región Caribe de Colombia. ")
        st.sidebar.markdown("# Índice")
        st.sidebar.write("- <a href='#basededatos' style='text-decoration: none; color: inherit;'>Base de datos</a>", unsafe_allow_html=True)
        st.sidebar.write("- <a href='#puntajepromedioasig' style='text-decoration: none; color: inherit;'>Puntaje promedio de las Asignaturas</a>", unsafe_allow_html=True)
        st.sidebar.write("- <a href='#puntapromestrato' style='text-decoration: none; color: inherit;'>Puntaje promedio por Estrato</a>", unsafe_allow_html=True)
        st.sidebar.write("- <a href='#pntapromdepa' style='text-decoration: none; color: inherit;'>Puntaje promedio por Departamento</a>", unsafe_allow_html=True)
        st.sidebar.write("- <a href='#puntapromgenero' style='text-decoration: none; color: inherit;'>Puntaje promedio por Género</a>", unsafe_allow_html=True)
        st.sidebar.write("- <a href='#puntamunicipios' style='text-decoration: none; color: inherit;'>Puntajes globales por género y período para cada municipio</a>", unsafe_allow_html=True)
        st.sidebar.write("- <a href='#puntajesquilla' style='text-decoration: none; color: inherit;'>Gráficos para los puntajes globales en Barranquilla</a>", unsafe_allow_html=True)


    st.markdown("<a name='basededatos'></a>", unsafe_allow_html=True)
    st.markdown("---")
    mostrar_datos(conexion)

    st.markdown("<a name='puntajepromedioasig'></a>", unsafe_allow_html=True)
    st.markdown("---")
    g_puntajeProm_Asig_periodo(conexion)

    st.markdown("<a name='puntapromestrato'></a>", unsafe_allow_html=True)
    st.markdown("---")
    g_puntajeProm_Estrato(conexion)

    st.markdown("<a name='pntapromdepa'></a>", unsafe_allow_html=True)
    st.markdown("---")
    g_puntajeProm_Dept(conexion)

    st.markdown("<a name='puntapromgenero'></a>", unsafe_allow_html=True)
    st.markdown("---")
    g_puntajeProm_genero(conexion)

    st.markdown("<a name='puntamunicipios'></a>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("Puntajes globales por género y período para cada municipio")

    df_global_deptmun = consulta_puntaje_global_por_periodo(conexion)
    if not df_global_deptmun.empty:
        st.subheader("Para las siguientes gráficas seleccione el departamento/municipio que desea consultar:")
        # Se agregan widgets de selección para el departamento y municipio
        departamento_seleccionado = st.selectbox("Selecciona un departamento", df_global_deptmun['COLE_DEPTO_UBICACION'].unique())
        municipio_seleccionado = st.selectbox("Selecciona un municipio", df_global_deptmun[df_global_deptmun['COLE_DEPTO_UBICACION'] == departamento_seleccionado]['COLE_MCPIO_UBICACION'].unique())
    else:
        st.error('No se pudieron obtener resultados de la consulta')

    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            g_ba_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)

        with right_column:
            g_linea_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            g_areaapiladas_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)

        with row2_col2:
            g_dipersion_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)       


    st.markdown("<a name='puntajesquilla'></a>", unsafe_allow_html=True)
    st.markdown("---")
    g_puntajeProm_barranquilla(conexion)

    # Cerrar conexión a la base de datos
    conexion.close()
