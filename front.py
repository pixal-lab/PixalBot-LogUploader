import tkinter as tk
import re
import time as t
from tkinter import filedialog, ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar


def select_date():
    top = tk.Toplevel(frame)
    cal = Calendar(top, font="Arial 14", selectmode="day", locale="es_ES")
    cal.pack(padx=20, pady=20)
    
    def set_date():
        selected_date.set(cal.get_date())
        top.destroy()
    
    ok_button = tk.Button(top, text="Aceptar", command=set_date)
    ok_button.pack()

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def validate_time_input(P):
    # La función se llama cada vez que se ingresa un carácter en el Entry
    if re.match(r'^\d{1,2}:\d{2}$', P):
        return True
    else:
        return False

def on_submit():
    folder_path = folder_entry.get().strip()
    date = date_entry.get().strip()
    hours = hours_entry.get().strip()
    minutes = minutes_entry.get().strip()
    link = link_entry.get().strip()
    print("-----")
    print(folder_entry)
    print(date)
    print(hours)
    print(minutes)
    print(link)
    print("-----")
    return 0
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
    
def refresh_position():
    add_row.grid(row=3 + rows, columnspan=3)
    link_label.grid(row=4+ rows, column=0, sticky='e')
    link_entry.grid(row=4+ rows, column=1)
    submit_button.grid(row=5+ rows, columnspan=3)

def add_time():
    global rows
    rows += 2
    
    #------- Fecha -------
    time_label = tk.Label(frame, text='Fecha inicio [DD:MM:AA]:')
    time_label.grid(row=1 + rows, column=0, sticky='e')

    date_entry = tk.Entry(frame, textvariable=selected_date,justify="center", width=wEntry)
    date_entry.grid(row=1 + rows, column=1)
    date_entry.insert(0, datetime.now().strftime("%d/%m/%y"))

    select_date_button = tk.Button(frame, text="Calend", command=select_date, width=5)
    select_date_button.grid(row=1 + rows, column=2)


    #------- Duracion -------
    m_label = tk.Label(frame, text='Duracion [HH:MM]')
    m_label.grid(row=2 + rows, column=0, sticky='e')
    frame_time = tk.Frame(frame)
    frame_time.grid(row=2 + rows, column=1)

    hours_entry = ttk.Spinbox(frame_time, from_=0, to=24, justify="center", format="%02.0f", width=int(wEntry/2-4))
    hours_entry.grid(row=0, column=0)
    hours_entry.insert(0, "00")

    m_label = tk.Label(frame_time, text=':')
    m_label.grid(row=0, column=1)

    minutes_entry = ttk.Spinbox(frame_time, from_=0, to=59, justify="center", format="%02.0f", width=int(wEntry/2-4))
    minutes_entry.grid(row=0, column=2)
    minutes_entry.insert(0, "00")

    refresh_position()



wEntry = 20
entries_date = []

app = tk.Tk()
app.title('PixalBot LogUploader')

frame = tk.Frame(app, padx=20, pady=20)
frame.grid(row=0, column=0)

selected_date = tk.StringVar()


#------- ruta -------
folder_label = tk.Label(frame, text='Ruta de la carpeta:')
folder_label.grid(row=0, column=0, sticky='e')

folder_entry = tk.Entry(frame, width=wEntry)
folder_entry.grid(row=0, column=1)

browse_button = tk.Button(frame, text='Buscar', command=browse_folder, width=5)
browse_button.grid(row=0, column=2)



rows = 0


add_row = tk.Button(frame, text='Agregar periodo', command=add_time)
add_row.grid(row=3 + rows, columnspan=3)


#------- Link -------
link_label = tk.Label(frame, text='Enlace:')
link_label.grid(row=4+ rows, column=0, sticky='e')
link_entry = tk.Entry(frame, width=wEntry)
link_entry.grid(row=4+ rows, column=1)



#------- Enviar -------
submit_button = tk.Button(frame, text='Enviar', command=on_submit)
submit_button.grid(row=5+ rows, columnspan=3)
add_time()

app.mainloop()




