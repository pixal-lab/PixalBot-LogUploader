from datetime import datetime, timedelta
import requests
import os

def listar_archivos_recientes(ruta, tiempo_pasado):
    try:
        archivos = []
        time_end = datetime.now()
        hora_limite = time_end - tiempo_pasado
        
        # Recorrer todos los archivos en la ruta y sus subcarpetas
        for root, dirs, files in os.walk(ruta):
            for archivo in files:
                ruta_completa = os.path.join(root, archivo)
                tiempo_creacion = datetime.fromtimestamp(os.path.getctime(ruta_completa))
                if tiempo_creacion > hora_limite:
                    archivos.append(ruta_completa)
        # Imprimir la lista de archivos recientes
        if archivos:
            return archivos
        else:
            print("No se encontraron archivos recientes en la ruta especificada.")
    except Exception as e:
        print(f"Error: {e}")

def subir_archivo_a_api(url_api, archivo):
    try:
        params = {'json': '1'}
        files = {'file': (archivo, open(archivo, 'rb'))}
        response = requests.post(url_api, params=params, files=files)
        if response.status_code == 200:
            link = response.json()['permalink']
            boss = response.json()['encounter']['boss']
            duration = response.json()['encounter']['duration']
            success = response.json()['encounter']['success']
            isCm = response.json()['encounter']['isCm']
            return [link, boss, duration, success, isCm]
        else:
            print(f"Error al subir el archivo. Código de estado: {response}")
            print(archivo)
            return -1     
    except Exception as e:
        print(f"Error: {e}")


path = "C:/Users/pbobk/OneDrive/Documentos/Guild Wars 2/addons/arcdps/arcdps.cbtlogs"
listar_archivos_recientes(path)