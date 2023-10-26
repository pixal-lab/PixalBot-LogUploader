import tkinter as tk
import re
import os
import requests
import time as t
from tkinter import filedialog
from datetime import datetime, timedelta
from collections import defaultdict
from dhooks import Webhook, Embed

url_api = "https://dps.report/uploadContent"
data = []
base = defaultdict(list)
base_success = defaultdict(list)

nombres = {
    "vg": "Vale Guardian",
    "gors": "Gorseval",
    "sab": "Sabetha",
    "sloth": "Slothason",
    "matt": "Matthias Gabrel",
    "kc": "Keep Construct",
    "xera": "Xera",
    "cairn": "Cairn the Indomitable",
    "mo": "Mursaat Overseer",
    "sam": "Samarog",
    "dei": "Deimos",
    "sh": "Soulless Horror",
    "dhuum": "Dhuum",
    "ca": "Conjured Amalgamate",
    "twins": "Twin Largos",
    "qadim": "Qadim",
    "adina": "Cardinal Adina",
    "sabir": "Cardinal Sabir",
    "qpeer": "Qadim the Peerless",
}

def listar_archivos_recientes(ruta, tiempo_pasado):
    try:
        # Obtener la hora actual
        hora_actual = datetime.now()
        # Calcular la hora límite para archivos recientes
        hora_limite = hora_actual - tiempo_pasado
        # Inicializar una lista para almacenar los archivos recientes
        archivos_recientes = []
        # Recorrer todos los archivos en la ruta y sus subcarpetas
        for root, dirs, files in os.walk(ruta):
            for archivo in files:
                ruta_completa = os.path.join(root, archivo)
                tiempo_creacion = datetime.fromtimestamp(os.path.getctime(ruta_completa))
                if tiempo_creacion > hora_limite:
                    archivos_recientes.append(ruta_completa)
        # Imprimir la lista de archivos recientes
        if archivos_recientes:
            return archivos_recientes
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


def boss(codigo):
    if nombres[codigo] in base or nombres[codigo] in base_success:
        wipe = ""
        if nombres[codigo] in base:
            for f in base[nombres[codigo]]:
                wipe += " [:x:](" + f[0] + ")"
        y = ""
        if nombres[codigo] in base_success:
            y =" CM" if base_success[nombres[codigo]][0][4] else ""
            return "[" + nombres[codigo] + y +"](" + base_success[nombres[codigo]][0][0] + ")" + wipe
        else:
            return nombres[codigo] + y + wipe
    else:
        return nombres[codigo]

def disc_hook(wHook, wipes):
    hook = Webhook(wHook)
    embed = Embed(
    title = 'Blue Panda Logs falta agregar funcion de semana',
    color = 1694948,
    thumbnail_url = "https://img.freepik.com/premium-vector/cute-red-panda-reading-book-cartoon-icon-illustration-animal-education-icon-concept-isolated-flat-cartoon-style_138676-1295.jpg")

    embed.add_field(
        name = "W1:",
        value = boss("vg") + "\n" + boss("gors") + "\n" + boss("sab"),
        inline = False
    )
    embed.add_field(
        name = "W2:",
        value = boss("sloth") + "\n" + boss("matt"),
        inline = False
    )
    embed.add_field(
        name = "W3:",
        value = boss("kc") + "\n" + boss("xera"),
        inline = False
    )
    embed.add_field(
        name = "W4:",
        value = boss("cairn") + "\n" + boss("mo") + "\n" + boss("sam") + "\n" + boss("dei"),
        inline = False
    )
    embed.add_field(
        name = "W5:",
        value = boss("sh") + "\n" + boss("dhuum"),
        inline = False
    )
    embed.add_field(
        name = "W6:",
        value = boss("ca") + "\n" + boss("twins") + "\n" + boss("qadim"),
        inline = False
    )
    embed.add_field(
        name = "W7:",
        value = boss("adina") + "\n" + boss("sabir") + "\n" + boss("qpeer"),
        inline = False
    )
    embed.add_field(
        name = "Lunes:   ",
        value = "",
        inline = False
    )
    embed.add_field(
        name = "Martes:   ",
        value = "",
        inline = False
    )
    embed.add_field(
        name = "Total:",
        value = "",
        inline = False
    )
    embed.add_field(
        name = "Wipeos:   " + str(wipes) ,
        value = "",
        inline = False
    )
    hook.send(
        embed = embed,
        username = "PixalBot",
        avatar_url = "https://img.freepik.com/vector-premium/cute-red-panda-icon-illustration-estilo-plano-dibujos-animados_138676-1212.jpg?w=826"
    )






def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def validate_time_input(P):
    # La función se llama cada vez que se ingresa un carácter en el Entry
    if re.match(r'^\d{0,2}$', P):
        return True
    else:
        return False

def on_submit():
    folder_path = folder_entry.get().strip()
    hours = hours_entry.get().strip()
    minutes = minutes_entry.get().strip()

    hrs = 0
    min = 0

    try:
        hrs = int(hours)
    except:
        pass
    try:
        min = int(minutes)
    except:
        pass

    time = timedelta(hours=hrs, minutes=min)

    link = link_entry.get().strip()
    file_logs = listar_archivos_recientes(folder_path, time)
    wipes = 0
    if file_logs:
        contador = 0
        for log in file_logs:
            print(contador)
            contador += 1
            if contador == 23:
                t.sleep(60)
                contador = 0
            res = subir_archivo_a_api(url_api, log)
            if res != -1:
                print(res)
                data.append(res)
        print("---xx---")
        for i in data:
            print(i)
            if i[3]:
                base_success[i[1]].append(i)
            else:
                wipes += 1
                base[i[1]].append(i)
        print("---xxxxxx---")
        for i in base_success:
            print(i)
        print("---xxxxxx---")
        for i in base:
            for j in base[i]:
                print(j)
        print("---xxxxxx---")
        
        disc_hook(link, wipes)
    else:
        print('no archivos')
    file_logs = []
    

app = tk.Tk()
app.title('PixalBot LogUploader')

frame = tk.Frame(app, padx=20, pady=20)
frame.grid(row=0, column=0, sticky='w')

# Etiqueta y entrada para la ruta de la carpeta
folder_label = tk.Label(frame, text='Ruta de la carpeta:')
folder_label.grid(row=0, column=0, sticky='e')
folder_entry = tk.Entry(frame)
folder_entry.grid(row=0, column=1)
browse_button = tk.Button(frame, text='Buscar', command=browse_folder)
browse_button.grid(row=0, column=3)



# Etiqueta y entradas para las horas y minutos
time_label = tk.Label(frame, text='Tiempo:')
time_label.grid(row=1, column=0, sticky='e')

frame_time = tk.Frame(frame)
frame_time.grid(row=1, column=1)

time_validation = frame.register(validate_time_input)
hours_entry = tk.Entry(frame_time, validate="key", validatecommand=(time_validation, "%P"),width=2)
hours_entry.grid(row=0, column=0)

h_label = tk.Label(frame_time, text='h')
h_label.grid(row=0, column=1, sticky='e')

time_validation = frame.register(validate_time_input)
minutes_entry = tk.Entry(frame_time, validate="key", validatecommand=(time_validation, "%P"),width=2)
minutes_entry.grid(row=0, column=2)

m_label = tk.Label(frame_time, text='m')
m_label.grid(row=0, column=3, sticky='e')



# Etiqueta y entrada para el enlace
link_label = tk.Label(frame, text='Enlace:')
link_label.grid(row=2, column=0, sticky='e')
link_entry = tk.Entry(frame)
link_entry.grid(row=2, column=1, columnspan=2)

# Botón de envío
submit_button = tk.Button(frame, text='Enviar', command=on_submit)
submit_button.grid(row=3, columnspan=3)

app.mainloop()
