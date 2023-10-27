import tkinter as tk

def add_row():
    global row_count
    row_count += 1
    
    label = tk.Label(root, text=f"Label {row_count}:")
    label.grid(row=row_count, column=0)
    
    entry_var = tk.StringVar()  # Crea una variable StringVar para el Entry
    entry_var.trace("w", lambda name, index, mode, var=entry_var: format_entry(var))
    entry = tk.Entry(root, textvariable=entry_var)
    entry.grid(row=row_count, column=1)
    
    entries.append(entry_var)  # Agrega la variable StringVar a la lista

    add_row_button.grid(row=row_count + 1, column=0, columnspan=2)  # Actualiza la posición del botón

def format_entry(var):
    value = var.get()
    # Asegurarse de que el valor tenga 2 dígitos
    if len(value) > 2:
        var.set(value[:2])
    # Opcional: Llenar con ceros si es necesario
    elif len(value) < 2:
        var.set(value.rjust(2, '0'))

def get_entry_values():
    entry_values = [entry.get() for entry in entries]
    print("Valores de los Entries:", entry_values)

# Crear la ventana principal
root = tk.Tk()
root.title("Agregar Filas al Grid")

# Contador de filas
row_count = 0

# Botón para agregar una nueva fila
add_row_button = tk.Button(root, text="Agregar Fila", command=add_row)
add_row_button.grid(row=row_count + 1, column=0, columnspan=2)

# Lista para almacenar las variables StringVar
entries = []

# Botón para obtener los valores de los Entries
get_values_button = tk.Button(root, text="Obtener Valores", command=get_entry_values)
get_values_button.grid(row=row_count + 2, column=0, columnspan=2)

root.mainloop()
