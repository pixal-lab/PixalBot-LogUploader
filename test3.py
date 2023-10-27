from datetime import datetime, timedelta
import os
def listar_archivos_recientes(ruta, tiempo_pasado, duraciones):
    try:
        cota_sup =[tiempos + duraciones]
        # Obtener la hora actual
        hora_actual = datetime.now()
        # Inicializar una lista para almacenar los archivos recientes
        archivos_recientes = []
        # Recorrer todos los archivos en la ruta y sus subcarpetas
        count=0
        for root, dirs, files in os.walk(ruta):
            for archivo in files:

                ruta_completa = os.path.join(root, archivo)
                tiempo_creacion = datetime.fromtimestamp(os.path.getctime(ruta_completa))
                for i in range(len(tiempo_pasado)):
                    # Calcular la hora límite para archivos recientes
                    if tiempo_creacion > tiempo_pasado[i] and tiempo_creacion < cota_sup[i]:
                        archivos_recientes.append(ruta_completa)
                        break
        # Imprimir la lista de archivos recientes
        if archivos_recientes:
            print(count)
            return archivos_recientes
        else:
            print(count)
            print("No se encontraron archivos recientes en la ruta especificada.")
    except Exception as e:
        print(f"Error: {e}")


times=[]
for i in range(7):
    times.append(timedelta(hours=168, minutes=0))
time0 = datetime.now()
arch = listar_archivos_recientes("C:/Users/pbobk/OneDrive/Documentos/Guild Wars 2/addons/arcdps/arcdps.cbtlogs",times)
timef = datetime.now()

print(timef-time0)
print(len(arch))