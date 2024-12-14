import pandas as pd
import glob
import os
from datetime import datetime


# Ruta de la carpeta de archivos
ruta_raw = "./raw"

# Ruta de la carpeta resultado
ruta_transform = './transform_data'

# Obtener la fecha de ejecución
now = datetime.now()
fecha_de_ejecucion = now.strftime('%Y-%m-%d')
#print(fecha_de_ejecucion)

# Función de unificar archivos y consolidar tipos de datos
def consolidar_datos(ruta_raw, ruta_transform):

    # Obtener todos los archivos en la carpeta raw
    archivos = glob.glob(ruta_raw + "/*.csv") + glob.glob(ruta_raw + "/*.json") + glob.glob(ruta_raw + "/*.xml")

    if not archivos:
        print("No se encontraron archivos para procesar")
        return

    df_consolidado = pd.DataFrame()

    # Iterar sobre cada archivo y leer datos
    for archivo in archivos:
        extension = archivo.split('.')[-1].lower()
        try:
            if extension == 'csv':
                df = pd.read_csv(archivo)
            elif extension == 'json':
                df = pd.read_json(archivo)
            elif extension == 'xml':
                df = pd.read_xml(archivo)
            else:
                print(f'Formato no soprtado: {archivo}')
                continue
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
            continue
        df_consolidado = pd.concat([df_consolidado, df])

    if df_consolidado.empty:
        print("No se consolidaron datos")
        return
    
    # Asegurar que la fecha sea correcto el formato a datetime
    df_consolidado['fecha'] = pd.to_datetime(df_consolidado['fecha']) 
    df_consolidado = df_consolidado.dropna() # Eliminar valores nulos
    #df_consolidado['mes'] = df_consolidado['fecha'].dt.month

    # Crear y guardar el archivo consolidado
    ruta_archivo_consolidado = os.path.join(ruta_transform, f"CONSOLIDACIÓN_{fecha_de_ejecucion}.csv")
    df_consolidado.to_csv(ruta_archivo_consolidado, index=False)
    print(f"Archivo consolidado: {ruta_archivo_consolidado}")

    # Crear el archivo Ventas por mes de cada producto
    ventas_por_mes = df_consolidado.groupby([pd.Grouper(key='fecha', freq='ME'), 'producto_id'])['total_venta'].sum().reset_index()
    ruta_archivo_ventas_mes = os.path.join(ruta_transform, f"VENTAS_MES_{fecha_de_ejecucion}.csv")
    ventas_por_mes.to_csv(ruta_archivo_ventas_mes, index=False)
    print(f"Archivo de ventas por mes: {ruta_archivo_ventas_mes}")

    # Crear el archivo o top 10 de loss productos más vendidos durante el año
    top_10_productos = df_consolidado.groupby('producto_id')['total_venta'].sum().sort_values(ascending=False).head(10).reset_index()
    ruta_archivo_top_productos = os.path.join(ruta_transform, f"PRODUCTOS_TOP_{fecha_de_ejecucion}.csv")
    top_10_productos.to_csv(ruta_archivo_top_productos, index=False)
    print(f"Archivo top 10 productos: {ruta_archivo_top_productos}")

# Ejecutar funcion
consolidar_datos(ruta_raw, ruta_transform)