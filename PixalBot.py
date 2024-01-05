import tkinter as tk
from tkinter import filedialog, ttk, Scrollbar, simpledialog
from datetime import datetime, timedelta
from tkcalendar import Calendar
import filesToLinks as fl
from collections import defaultdict
import discHook as dh
import sys, os
from configparser import ConfigParser

failure = defaultdict(list)
success = defaultdict(list)
rows = 0
config = ConfigParser()
hooks = []
configfile = 'PixalBot_config.ini'

def load_config():
    try:
        config.read(configfile)
        for section in config.sections():
            nombre = config[section]['nombre']
            valor = config[section]['valor']
            hooks.append({"nombre": nombre, "valor": valor})
    except:
        pass

def save_hook():
    valor = link_entry.get()

    # Pedir al usuario que ingrese un nombre para el guardado
    nombre = simpledialog.askstring("Save", "WebHook name")

    if nombre:
        # Agregar el valor y nombre a la lista
        hooks.append({"nombre": nombre, "valor": valor})

        # Guardar la lista en un archivo de configuración
        actualizar_configuracion()
def load_hook():
    # Abrir una nueva ventana para seleccionar un valor de la lista
    ventana_seleccion = tk.Toplevel(app)
    ventana_seleccion.title('Discord WebHooks')
    ventana_seleccion.resizable(width=False, height=False)
    ventana_seleccion.iconbitmap(resource_path("icon.ico"))

    # Crear una listabox para mostrar los valores almacenados
    lista_box = tk.Listbox(ventana_seleccion, width=70)
    lista_box.grid(row=0, column=0, pady=5, padx=10, sticky=tk.N+tk.S)

    # Barra de desplazamiento vertical
    scrollbar = tk.Scrollbar(ventana_seleccion, orient=tk.VERTICAL, command=lista_box.yview)
    scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)

    # Configurar la listbox para usar la barra de desplazamiento
    lista_box.config(yscrollcommand=scrollbar.set)

    # Llenar la listabox con los valores y nombres almacenados
    for item in hooks:
        lista_box.insert(tk.END, f"{item['nombre']} - {item['valor']}")

    # Función para cargar el valor y nombre seleccionado
    def cargar_seleccion():
        seleccion = lista_box.curselection()
        if seleccion:
            item_seleccionado = hooks[seleccion[0]]
            link_entry.delete(0, tk.END)
            link_entry.insert(0, item_seleccionado["valor"])

        ventana_seleccion.destroy()


    # Función para eliminar el valor y nombre seleccionado
    def eliminar_seleccion():
        seleccion = lista_box.curselection()
        if seleccion:
            hooks.pop(seleccion[0])
            lista_box.delete(seleccion)
            # Actualizar la configuración después de eliminar
            actualizar_configuracion()

    bottom_frame = tk.Frame(ventana_seleccion)
    bottom_frame.grid(row=1, column=0, pady=5, padx=10)
    
    # Botón para cargar el valor y nombre seleccionado
    cargar_boton = tk.Button(bottom_frame, text="Load", command=cargar_seleccion)
    cargar_boton.grid(row=0, column=0)

    # Botón para eliminar el valor y nombre seleccionado
    eliminar_boton = tk.Button(bottom_frame, text="Delete", command=eliminar_seleccion)
    eliminar_boton.grid(row=0, column=1)

def actualizar_configuracion():
    # Guardar la lista en un archivo de configuración
    config = ConfigParser()
    for i, item in enumerate(hooks):
        config[f'hook_{i}'] = {'nombre': item['nombre'], 'valor': item['valor']}

    with open(configfile, 'w') as c:
        config.write(c)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def console_log(console, text):
    console.insert("end", text + "\n")
    print(text)
    console.see("end")
    app.update()

def select_date(entry_var):
    top = tk.Toplevel(frame)
    
    cal = Calendar(top, font="Arial 14", selectmode="day", locale="es_ES")
    cal.pack()
    
    def set_date(i):
        entry_dates[i].set(cal.get_date())
        top.destroy()
    
    ok_button = tk.Button(top, text="Aceptar", command=lambda entry = entry_var:set_date(entry))
    ok_button.pack()

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)


def validationH(e, spinbox):
    new_value = spinbox.get().strip()
    if not new_value.isdigit():
        spinbox.delete(0, 'end')
        spinbox.insert(0, "00")
    else:
        if int(new_value) > 23:
            spinbox.delete(0, 'end')
            spinbox.insert(0, 23)
        else:
            spinbox.delete(0, 'end')
            spinbox.insert(0, f'{int(new_value):02d}')

def validationH2(e, spinbox):
    new_value = spinbox.get().strip()
    if not new_value.isdigit():
        spinbox.delete(0, 'end')
        spinbox.insert(0, "00")
    else:
        if int(new_value) < 100:
            spinbox.delete(0, 'end')
            spinbox.insert(0, f'{int(new_value):02d}')
        if int(new_value) > 168:
            spinbox.delete(0, 'end')
            spinbox.insert(0, 168)


def validationM(e, spinbox):
    new_value = spinbox.get().strip()
    if not new_value.isdigit():
        spinbox.delete(0, 'end')
        spinbox.insert(0, "00")
    else:
        if int(new_value) > 59:
            spinbox.delete(0, 'end')
            spinbox.insert(0, 59)
        else:
            spinbox.delete(0, 'end')
            spinbox.insert(0, f'{int(new_value):02d}')

def on_submit():

    success.clear()
    failure.clear()
    folder_path = folder_entry.get().strip()
    times0 = []
    times1 = []
    for i in range(len(entry_dates)):
        date_str = entry_dates[i].get()
        hm_str = entry_h0[i].get()+entry_m0[i].get()

        fecha_obj = datetime.strptime(date_str, '%d/%m/%y')
        hora_obj = datetime.strptime(hm_str, '%H%M')
        fecha_obj = fecha_obj.replace(hour=hora_obj.hour, minute=hora_obj.minute)
        times0.append(fecha_obj)

        delta = timedelta(hours=int(entry_h[i].get()), minutes=int(entry_m[i].get()))
        times1.append(fecha_obj + delta)
    for i in range(len(times0)):
        console_log(console, f"Tiempo de run {i} \n Inicio: {times0 [i].strftime('%d/%m/%Y %H:%M')} \n Termino: {times1[i].strftime('%d/%m/%Y %H:%M')}")

    link = link_entry.get().strip()
    # console_log("-----")
    # console_log(console, folder_path)
    # console_log(console, times0)
    # console_log(console, times1)
    # console_log(console, link)
    # console_log(console, "-----")

    console_log(console, f"Buscando en la ruta: {folder_path}")

    file_logs, data_runs = fl.listar_archivos_recientes(console, folder_path, times0, times1)

    wipes = 0

    data = defaultdict(list)    # {ruta : data}

    contador = 0
    if file_logs:
        for run in range(len(file_logs)):
            for log in range(len(file_logs[run])):
                if file_logs[run][log][0] in data:
                    console_log(console, "Log ya subido")
                    pass
                else:
                    console_log(console, f"Subiendo log {log + 1}/{len(file_logs[run])} de la run {run + 1}/{len(file_logs)}")
                    res = fl.subir_archivo_a_api(console, url_api, file_logs[run][log][0])
                    contador += 1
                    if res != -1:
                        data[file_logs[run][log][0]] = res
        console_log(console, "Logs subidos, haciendo cosas")
        for i, j in data.items(): # [link, boss, duration, success, isCm]
            if (j[2] >= int(d_entry.get())):
                if j[3]:
                    success[j[1]].append(j)
                else:
                    wipes += 1
                    failure[j[1]].append(j)
        t_runs = []
        console_log(console, "Haciendo más cosas")
        if any(item is not None for item in data_runs):
            for run in data_runs:
                total = timedelta(seconds=0)
                if run != None:
                    t0 = run[0]
                    tf = run[2]
                    df = data[run[1]][2]
                    total = tf - t0
                    total = total + timedelta(seconds=df)
                t_runs.append(total)
        if len(t_runs) > 0:
            console_log(console, "Enviando a Discord")
            dh.send(link, success, failure, t_runs, times0)
            console_log(console, ":)")

    else:
        console_log(console, 'No se encontraron archivos')

    
def refresh_position():
    add_row.grid(row=4 + rows, columnspan=3)
    
    d_label.grid(row=5 + rows, column=0, sticky='e')
    d_entry.grid(row=5 + rows, column=1)
    link_label.grid(row=6+ rows, column=0, sticky='e')
    link_entry.grid(row=6+ rows, column=1)
    frame_hook.grid(row=6+ rows, column=2)
    submit_button.grid(row=7+ rows, columnspan=3)
    consfr.grid(row=8+ rows, columnspan=3)


entry_dates = []
entry_h0 = []
entry_m0 = []
entry_h = []
entry_m = []
def add_time():
    global rows
    global vldt_ifnum_cmd
    if int(rows/2)-1 < 9:
        rows += 3

        #------- Fecha -------
        time_label = tk.Label(frame, text='Start Date:')
        time_label.grid(row=1 + rows, column=0, sticky='e')

        entry_var = tk.StringVar()
        date_entry = tk.Entry(frame, textvariable=entry_var, state='disabled', justify="center", width=wEntry)
        date_entry.grid(row=1 + rows, column=1)
        entry_var.set(datetime.now().strftime("%d/%m/%y"))
        entry_dates.append(entry_var)

        select_date_button = tk.Button(frame, text="Calend", command=lambda i=int(rows/3)-1:select_date(i), width=5)
        select_date_button.grid(row=1 + rows, column=2)

        #------- hora inicio -------
        m0_label = tk.Label(frame, text='Start Time [HH:MM]')
        m0_label.grid(row=2 + rows, column=0, sticky='e')
        frame_time0 = tk.Frame(frame)
        frame_time0.grid(row=2 + rows, column=1)

        hours0_entry = ttk.Spinbox(frame_time0,from_=0, to=23,wrap=True,justify="center",format="%02.0f",width=int(wEntry/2-4))
        hours0_entry.bind("<FocusOut>", lambda event, spinbox=hours0_entry: validationH(event, spinbox))
        hours0_entry.grid(row=0, column=0)
        hours0_entry.insert(0, "00")
        entry_h0.append(hours0_entry)

        m0_label = tk.Label(frame_time0, text=':')
        m0_label.grid(row=0, column=1)

        minutes0_entry = ttk.Spinbox(frame_time0, from_=0, to=59,wrap=True, justify="center", format="%02.0f", width=int(wEntry/2-4))
        minutes0_entry.bind("<FocusOut>", lambda event, spinbox=minutes0_entry: validationM(event, spinbox))
        minutes0_entry.grid(row=0, column=2)
        minutes0_entry.insert(0, "00")
        entry_m0.append(minutes0_entry)


        #------- Duracion -------
        m_label = tk.Label(frame, text='Run duration [HH:MM]')
        m_label.grid(row=3 + rows, column=0, sticky='e')
        frame_time = tk.Frame(frame)
        frame_time.grid(row=3 + rows, column=1)

        hours_entry = ttk.Spinbox(frame_time, from_=0, to=24*7,wrap=True, justify="center", format="%02.0f", width=int(wEntry/2-4))
        hours_entry.bind("<FocusOut>", lambda event, spinbox=hours_entry: validationH2(event, spinbox))
        hours_entry.grid(row=0, column=0)
        hours_entry.insert(0, "00")
        entry_h.append(hours_entry)

        m_label = tk.Label(frame_time, text=':')
        m_label.grid(row=0, column=1)

        minutes_entry = ttk.Spinbox(frame_time, from_=0, to=59,wrap=True, justify="center", format="%02.0f", width=int(wEntry/2-4))
        minutes_entry.bind("<FocusOut>", lambda event, spinbox=minutes_entry: validationM(event, spinbox))
        minutes_entry.grid(row=0, column=2)
        minutes_entry.insert(0, "00")
        entry_m.append(minutes_entry)

        refresh_position()
        if not int(rows/2)-1 < 9:
            add_row.configure(state='disabled')


wEntry = 20
entries_date = []
url_api = "https://dps.report/uploadContent"
url_apib = "https://b.dps.report//uploadContent"

load_config()

app = tk.Tk()
app.title('PixalBot LogUploader')
app.resizable(width=False, height=False)
app.iconbitmap(resource_path("icon.ico"))

frame = tk.Frame(app, padx=20, pady=20)
frame.grid(row=0, column=0)

#------- ruta -------
folder_label = tk.Label(frame, text='Log Directory Path:')
folder_label.grid(row=0, column=0, sticky='e')

folder_entry = tk.Entry(frame, width=wEntry)
folder_entry.grid(row=0, column=1)

browse_button = tk.Button(frame, text='Search', command=browse_folder, width=5)
browse_button.grid(row=0, column=2)



add_row = tk.Button(frame, text='Add run', command=add_time)
add_row.grid(row=4 + rows, columnspan=3)



d_label = tk.Label(frame, text='Min encounter duration [sec]')
d_label.grid(row=5 + rows, column=0, sticky='e')

d_entry = ttk.Spinbox(frame, from_=0, to=120,wrap=True, justify="center", format="%02.0f", width=int(wEntry-3))
d_entry.bind("<FocusOut>", lambda event, spinbox=d_entry: validationH2(event, spinbox))
d_entry.grid(row=5 + rows, column=1)
d_entry.insert(0, "00")


#------- Link -------
link_label = tk.Label(frame, text='Webhook Link:')
link_label.grid(row=6+ rows, column=0, sticky='e')
link_entry = tk.Entry(frame, width=wEntry)
link_entry.grid(row=6+ rows, column=1)

frame_hook = tk.Frame(frame)
frame_hook.grid(row=6+ rows, column=2)

save_webhook = tk.Button(frame_hook, text='Save', command=save_hook, width=5)
save_webhook.grid(row=0, column=0)

load_webhook = tk.Button(frame_hook, text='Load', command=load_hook, width=5)
load_webhook.grid(row=0, column=1)


#------- Enviar -------
submit_button = tk.Button(frame, text='Send', command=on_submit)
submit_button.grid(row=7+ rows, columnspan=3)


consfr = tk.Frame(frame)
consfr.grid(row=8+ rows, columnspan=3)

console = tk.Text(consfr, height=10, width=50)
console.grid(row=0, column=0)
scrollbar = Scrollbar(consfr, command=console.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

console.config(yscrollcommand=scrollbar.set)

add_time()
app.mainloop()