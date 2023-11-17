from datetime import datetime, timedelta
import requests
import os
import time as t

def console_log(console, text):
    console.insert("end", text + "\n")
    print(text)
    console.see("end")

def listar_archivos_recientes(console, ruta, t0, t1):
    try:
        data_runs = [None] * len(t0) # t0, tf, dur_f
        archivos = [[] for _ in range(len(t0))]
        # Recorrer todos los archivos en la ruta y sus subcarpetas
        for root, dirs, files in os.walk(ruta):
            for archivo in files:
                ruta_completa = os.path.join(root, archivo)
                for i in range(len(t0)):
                    if (ruta_completa.split(".")[-1] == "evtc" or ruta_completa.split(".")[-1] == "zevtc"):
                        tiempo_creacion = datetime.strptime(archivo.split(".")[0], "%Y%m%d-%H%M%S")
                        if tiempo_creacion > t0[i] and tiempo_creacion < t1[i]:
                            console_log(console,f"Archivo encontrado: {archivo}.")
                            archivos[i].append([ruta_completa, tiempo_creacion])

        for i in range(len(archivos)):
            console_log(console,f"Se encontraron: {len(archivos[i])} logs para la run {i}")
        if archivos:
            for i in range(len(archivos)):
                if len(archivos[i]) > 0:
                    archivos[i] = sorted(archivos[i], key=lambda x: x[1])
                    data_runs[i] = [archivos[i][0][1], archivos[i][0][0], archivos[i][-1][1]]
    
            return [archivos, data_runs]
        else:
            console_log(console,"No se encontraron archivos recientes en la ruta especificada.")
    except Exception as e:
        console_log(console,f"Error: {e}")

def subir_archivo_a_api(console, url_api, archivo):
    try:
        params = {'json': '1'}
        files = {'file': (archivo, open(archivo, 'rb'))}
        response = requests.post(url_api, params=params, files=files)
        if response.status_code == 429:
            console_log(console, "Durmiendo uwu")
            t.sleep(61)
            response = requests.post(url_api, params=params, files=files)
        if response.status_code == 200:
            print(response.json())
            link = response.json()['permalink']
            boss = response.json()['encounter']['boss']
            duration = response.json()['encounter']['duration']
            success = response.json()['encounter']['success']
            isCm = response.json()['encounter']['isCm']
            # print([link, boss, duration, success, isCm])
            return [link, boss, duration, success, isCm]
        else:
            console_log(console,f"Error al subir el archivo. Código de estado: {response}")
            console_log(console,archivo)
            return -1     
    except Exception as e:
        console_log(console,f"Error: {e}")



