import tkinter as tk
from tkinter import ttk

def on_double_click(event):
    # Identifica la fila y columna en la que se hizo doble clic
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    
    # Si se hizo clic en una fila y columna válidas
    if item and column:
        x, y, width, height = tree.bbox(item, column)
        column_index = int(column[1:]) - 1  # Convierte el identificador de columna a un índice
        
        # Obtiene el valor actual de la celda
        value = tree.item(item, 'values')[column_index]
        
        # Crea un Entry temporal para editar el valor
        entry = tk.Entry(root)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def on_focus_out(event):
            # Actualiza el valor en el Treeview
            new_value = entry.get()
            current_values = list(tree.item(item, 'values'))
            current_values[column_index] = new_value
            tree.item(item, values=current_values)
            entry.destroy()

        # Destruye el Entry cuando pierde el foco
        entry.bind('<FocusOut>', on_focus_out)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Treeview Editable")

# Crea un Treeview con algunas columnas
tree = ttk.Treeview(root, columns=('Columna 1', 'Columna 2', 'Columna 3'), show='headings')
tree.heading('Columna 1', text='Columna 1')
tree.heading('Columna 2', text='Columna 2')
tree.heading('Columna 3', text='Columna 3')

# Agrega algunas filas de ejemplo
tree.insert('', 'end', values=('Valor 1', 'Valor 2', 'Valor 3'))
tree.insert('', 'end', values=('Valor 4', 'Valor 5', 'Valor 6'))

# Configura el evento de doble clic
tree.bind('<Double-1>', on_double_click)

tree.pack(expand=True, fill=tk.BOTH)

root.mainloop()
