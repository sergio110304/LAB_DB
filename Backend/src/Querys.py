import pandas as pd
from conexion_db import conectar_servidor

def realizar_consulta(conexion):
    if conexion:
        try:
            cursor = conexion.cursor()
            query = '''
                    SELECT FAMI_TIENECOMPUTADOR, FAMI_TIENEINTERNET,AVG(PUNT_GLOBAL) AS Puntaje_Promedio FROM Resultados_Saber_11_R_Caribe_2015_2022 GROUP BY FAMI_TIENEAUTOMOVIL, FAMI_TIENECOMPUTADOR, FAMI_TIENEINTERNET
                    '''
            df_resuldatos = pd.read_sql(query, conexion)
            cursor.close()
            return df_resuldatos
        except Exception as e:
            print('Error al realizar la consulta:', e)
            return None
    else:
        return None

# Ejemplo de uso
if __name__ == "__main__":

    conexion = conectar_servidor()
    if conexion:
        df_resuldatos = realizar_consulta(conexion)
        if df_resuldatos is not None:
            print(df_resuldatos)
        else:
            print('No se pudo realizar la consulta')
        conexion.close()
    else:
        print('No se pudo establecer la conexión')

## Modificacion___
### Medificacion2
