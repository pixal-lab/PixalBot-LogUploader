import tkinter as tk
import time as t
from tkinter import filedialog, ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar
import filesToLinks as fl
from collections import defaultdict
import discHook as dh

failure = defaultdict(list)
success = defaultdict(list)


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

    link = link_entry.get().strip()
    # print("-----")
    # print(folder_path)
    # print(times0)
    # print(times1)
    # print(link)
    # print("-----")


    file_logs, data_runs = fl.listar_archivos_recientes(folder_path, times0, times1)

    wipes = 0

    data = defaultdict(list)    # {ruta : data}

    contador = 0
    if file_logs:
        for run in range(len(file_logs)):
            for log in range(len(file_logs[run])):
                if file_logs[run][log][0] in data:
                    print("Log ya subido")
                    pass
                else:
                    print(f"subiendo log {log + 1}")
                    if contador > 24:
                        t.sleep(60)
                    res = fl.subir_archivo_a_api(url_api, file_logs[run][log][0])
                    contador += 1
                    if res != -1:
                        data[file_logs[run][log][0]] = res

        for i, j in data.items(): # [link, boss, duration, success, isCm]
            if j[3]:
                success[j[1]].append(j)
            else:
                wipes += 1
                failure[j[1]].append(j)
        t_runs = []
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
        print(t_runs)
        if len(t_runs) > 0:
            dh.send(link, success, failure, t_runs, times0)

    else:
        print('No archivos')

    
def refresh_position():
    add_row.grid(row=4 + rows, columnspan=3)
    link_label.grid(row=5+ rows, column=0, sticky='e')
    link_entry.grid(row=5+ rows, column=1)
    submit_button.grid(row=6+ rows, columnspan=3)

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
        time_label = tk.Label(frame, text='Fecha inicio:')
        time_label.grid(row=1 + rows, column=0, sticky='e')

        entry_var = tk.StringVar()
        date_entry = tk.Entry(frame, textvariable=entry_var, state='disabled', justify="center", width=wEntry)
        date_entry.grid(row=1 + rows, column=1)
        entry_var.set(datetime.now().strftime("%d/%m/%y"))
        entry_dates.append(entry_var)

        select_date_button = tk.Button(frame, text="Calend", command=lambda i=int(rows/3)-1:select_date(i), width=5)
        select_date_button.grid(row=1 + rows, column=2)

        #------- hora inicio -------
        m0_label = tk.Label(frame, text='Hora inicio [HH:MM]')
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
        m_label = tk.Label(frame, text='Duracion [HH:MM]')
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

app = tk.Tk()
app.title('PixalBot LogUploader')
app.resizable(width=False, height=False)

frame = tk.Frame(app, padx=20, pady=20)
frame.grid(row=0, column=0)

#------- ruta -------
folder_label = tk.Label(frame, text='Ruta de la carpeta:')
folder_label.grid(row=0, column=0, sticky='e')

folder_entry = tk.Entry(frame, width=wEntry)
folder_entry.grid(row=0, column=1)

browse_button = tk.Button(frame, text='Buscar', command=browse_folder, width=5)
browse_button.grid(row=0, column=2)

rows = 0

add_row = tk.Button(frame, text='Agregar periodo', command=add_time)
add_row.grid(row=4 + rows, columnspan=3)

#------- Link -------
link_label = tk.Label(frame, text='Enlace:')
link_label.grid(row=5+ rows, column=0, sticky='e')
link_entry = tk.Entry(frame, width=wEntry)
link_entry.grid(row=5+ rows, column=1)

#------- Enviar -------
submit_button = tk.Button(frame, text='Enviar', command=on_submit)
submit_button.grid(row=6+ rows, columnspan=3)

add_time()
app.mainloop()
