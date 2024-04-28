from Graficas_query import *
from conexion_db import conectar_servidor

def main():
    conexion = conectar_servidor()

    # Título del dashboard
    st.title('Resultados Prueba Saber 2015-2022 REGIÓN CARIBE')

    with st.sidebar:
        st.write("Información sobre el proyecto")
        st.write("Es un dashboard que presenta cinco gráficas interactivas sobre los resultados de las\
                pruebas saber desde el 2015 hasta el 2022, especifícamente de \
                la  Región Caribe de Colombia. ")
        
    st.markdown("---")

    mostrar_datos(conexion)

    st.markdown("---")

    g_puntajeProm_Asig_periodo(conexion)

    st.markdown("---")

    g_puntajeProm_Estrato(conexion)

    st.markdown("---")

    g_puntajeProm_Dept(conexion)

    st.markdown("---")

    g_puntajeProm_genero(conexion)

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
    
    g_ba_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)

    g_linea_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)

    g_areaapiladas_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)

    g_dipersion_genero_municipio(conexion, departamento_seleccionado, municipio_seleccionado)       

    st.markdown("---")

    g_puntajeProm_barranquilla(conexion)

    # Cerrar conexión a la base de datos
    conexion.close()
