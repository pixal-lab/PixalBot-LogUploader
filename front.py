import tkinter as tk
import re
import time as t
from tkinter import filedialog, ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar


def select_date(entry_var):
    print("-----")
    top = tk.Toplevel(frame)
    print(entry_var)
    
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
            print(new_value)
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
    dates = [i.get() for i in entry_dates]
    times_h0 = [i.get() for i in entry_h0]
    times_m0 = [i.get() for i in entry_m0]
    times_h = [i.get() for i in entry_h]
    times_m = [i.get() for i in entry_m]
    link = link_entry.get().strip()
    print("-----")
    print(folder_entry)
    print(dates)
    print(times_h0)
    print(times_m0)
    print(times_h)
    print(times_m)
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
