import tkinter as tk
from tkinter import simpledialog
from configparser import ConfigParser

class MiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi App")

        # Entry
        self.mi_entry = tk.Entry(root)
        self.mi_entry.pack(pady=10)

        # Botones
        guardar_boton = tk.Button(root, text="Guardar", command=self.guardar_valor)
        guardar_boton.pack()

        cargar_boton = tk.Button(root, text="Cargar", command=self.cargar_valor)
        cargar_boton.pack()

        # Lista para almacenar valores y nombres
        self.lista_valores = []

        # Cargar los valores almacenados al iniciar
        self.cargar_configuracion()

    def guardar_valor(self):
        # Obtener el valor del Entry
        valor = self.mi_entry.get()

        # Pedir al usuario que ingrese un nombre para el guardado
        nombre = simpledialog.askstring("Guardar", "Ingrese un nombre para el guardado:")

        if nombre:
            # Agregar el valor y nombre a la lista
            self.lista_valores.append({"nombre": nombre, "valor": valor})

            # Guardar la lista en un archivo de configuración
            self.actualizar_configuracion()

    def cargar_valor(self):
        # Abrir una nueva ventana para seleccionar un valor de la lista
        ventana_seleccion = tk.Toplevel(self.root)

        # Crear una listabox para mostrar los valores almacenados
        lista_box = tk.Listbox(ventana_seleccion)
        lista_box.pack(pady=10)

        # Llenar la listabox con los valores y nombres almacenados
        for item in self.lista_valores:
            lista_box.insert(tk.END, f"{item['nombre']} - {item['valor']}")

        # Función para cargar el valor y nombre seleccionado
        def cargar_seleccion():
            seleccion = lista_box.curselection()
            if seleccion:
                item_seleccionado = self.lista_valores[seleccion[0]]
                self.mi_entry.delete(0, tk.END)
                self.mi_entry.insert(0, item_seleccionado["valor"])

            ventana_seleccion.destroy()

        # Botón para cargar el valor y nombre seleccionado
        cargar_boton = tk.Button(ventana_seleccion, text="Cargar", command=cargar_seleccion)
        cargar_boton.pack()

        # Función para eliminar el valor y nombre seleccionado
        def eliminar_seleccion():
            seleccion = lista_box.curselection()
            if seleccion:
                self.lista_valores.pop(seleccion[0])
                lista_box.delete(seleccion)
                # Actualizar la configuración después de eliminar
                self.actualizar_configuracion()

        # Botón para eliminar el valor y nombre seleccionado
        eliminar_boton = tk.Button(ventana_seleccion, text="Eliminar", command=eliminar_seleccion)
        eliminar_boton.pack()

    def actualizar_configuracion(self):
        # Guardar la lista en un archivo de configuración
        config = ConfigParser()
        for i, item in enumerate(self.lista_valores):
            config[f'MiSeccion_{i}'] = {'nombre': item['nombre'], 'valor': item['valor']}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def cargar_configuracion(self):
        try:
            # Cargar los valores desde el archivo de configuración
            config = ConfigParser()
            config.read('config.ini')

            for section in config.sections():
                nombre = config[section]['nombre']
                valor = config[section]['valor']
                self.lista_valores.append({"nombre": nombre, "valor": valor})

        except FileNotFoundError:
            # El archivo no existe, no hay valores almacenados aún
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MiApp(root)
    root.mainloop()
