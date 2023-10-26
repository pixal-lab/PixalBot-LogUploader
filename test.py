import tkinter as tk
from tkcalendar import Calendar

def select_date():
    top = tk.Toplevel(root)
    cal = Calendar(top, font="Arial 14", selectmode="day", locale="es_ES")
    cal.pack(padx=20, pady=20)
    
    def set_date():
        selected_date.set(cal.get_date())
        top.destroy()
    
    ok_button = tk.Button(top, text="Aceptar", command=set_date)
    ok_button.pack()

root = tk.Tk()
root.title("Selección de Fecha")

selected_date = tk.StringVar()

date_label = tk.Label(root, text="Fecha seleccionada:")
date_label.pack()

date_entry = tk.Entry(root, textvariable=selected_date)
date_entry.pack()

select_date_button = tk.Button(root, text="Seleccionar Fecha", command=select_date)
select_date_button.pack()

root.mainloop()
