import pyodbc

def conectar_servidor():
    server = 'LAPTOP-1NKRV5PD'
    bd = 'LAB_ICFES'
    user = 'uselab1'
    password = 'uselab1'
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+bd+';UID='+user+';PWD='+password
        )
        print('Conexión exitosa')
        return conexion
    except Exception as e:
        print('Error al intentar conectarse:', e)
        return None

## No modificar
