import pyodbc
import pandas as pd
import time

# Crear cuatro variebles donde guardare los datos de conxion de mi servidor SQL Server
server = 'LAPTOP-1NKRV5PD'
bd = 'LAB_ICFES'
user = 'uselab1'
password = 'uselab1'

#Para controlar cualquier error que pueda susceder voy a meter todo dentro de try
#Voy a llevar a cabo la conexion con el servidor:
try:
    conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL server};SERVER='+server+';DATABASE='+bd+';UID='+user+';PWD='+password
    )
    print('Conexión exitosa')
except:
    print('Error al intentar conectarse')


start_time = time.time()
cursor = conexion.cursor()
# Consulta SQL para seleccionar todos los datos de la tabla Resuldatos_11_2010_2022
query = 'select s.PERIODO, s.PUNT_GLOBAL from Resultados_Saber_11_Region_Caribe s' 

# Guardar los resultados de la consulta en un DataFrame
df_resuldatos = pd.read_sql(query, conexion)

cursor.close()

# Imprimir una muestra de los datos de la tabla
print(df_resuldatos.head())
print(df_resuldatos.shape[0])

end_time = time.time()
execution_time = end_time - start_time
print("Tiempo de ejecución:", execution_time, "segundos")


'''
#Voy a crear un cursos para almacenar la informacion en memoria
cursor = conexion.cursor()

#La informacion que vaya generando o trayendo de SQL lo guardamos en memoria
query_tablas = 'SELECT * FROM information_schema.tables'
query_columnas = 'SELECT * FROM information_schema.columns'

#Guardo las consultas anteriores como dataframes
df_tablas = pd.read_sql(query_tablas, conexion)
df_columnas = pd.read_sql(query_columnas, conexion)

#Nos aseguramos de cerrar el cursos
cursor.close()


#df_tablas.info()
print(df_tablas.sample(2))
'''
