from datetime import datetime, timedelta
import requests
import os

def listar_archivos_recientes(ruta, t0, t1):
    print("listando-----------------------")
    try:
        data_runs = [None] * len(t0) # t0, tf, dur_f
        archivos = [[] for _ in range(len(t0))]
        # Recorrer todos los archivos en la ruta y sus subcarpetas
        for root, dirs, files in os.walk(ruta):
            for archivo in files:
                ruta_completa = os.path.join(root, archivo)
                tiempo_creacion = datetime.fromtimestamp(os.path.getctime(ruta_completa))
                for i in range(len(t0)):
                    if tiempo_creacion > t0[i] and tiempo_creacion < t1[i]:
                        print(f"t:{t0[i]}----{tiempo_creacion}----{t1[i]}")
                        print(f"archivo: {archivo}, para la run {i}, de un total de {len(t0)} runs.")
                        archivos[i].append([ruta_completa, tiempo_creacion])
        # Imprimir la lista de archivos recientes
        print(archivos)
        if archivos:
            for i in range(len(archivos)):
                if len(archivos[i]) > 0:
                    archivos[i] = sorted(archivos[i], key=lambda x: x[1])
                    data_runs[i] = [archivos[i][0][1], archivos[i][0][0], archivos[i][-1][1]]

            return [archivos, data_runs]
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



