import tkinter as tk

def on_checkbox_change():
    # Esta función se llama cuando el estado del checkbox cambia
    checkbox_state = checkbox_var.get()
    print("Estado del checkbox:", checkbox_state)

# Crear la ventana principal
root = tk.Tk()
root.title("Ejemplo Checkbox")

# Variable para almacenar el estado del checkbox
checkbox_var = tk.IntVar()

# Crear el checkbox y asociarlo a la variable
checkbox = tk.Checkbutton(root, text="Mi Checkbox", variable=checkbox_var, command=on_checkbox_change)
checkbox.pack(pady=10)

# Iniciar el bucle principal de la aplicación
root.mainloop()
