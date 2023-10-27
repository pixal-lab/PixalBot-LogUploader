import tkinter as tk

# Función que se ejecuta cuando el valor del Spinbox cambia
def on_spinbox_change():
    print("test")
    new_value = spinbox.get()  # Obtén el nuevo valor del Spinbox
    # Realiza la validación o edición del valor según sea necesario
    # Por ejemplo, puedes convertirlo a un número y multiplicarlo por 2:
    try:
        new_value = int(new_value) * 2
    except ValueError:
        # Manejo de errores si la entrada no es un número válido
        new_value = 0
    spinbox.delete(0, 'end')  # Borrar el contenido actual
    spinbox.insert(0, new_value)  # Establecer el nuevo valor

# Crear la ventana principal
root = tk.Tk()

# Crear un Spinbox y vincularlo a la función on_spinbox_change
spinbox = tk.Spinbox(root, from_=0, to=100, command=on_spinbox_change)
spinbox.pack()


# Inicializar la ventana
root.mainloop()
