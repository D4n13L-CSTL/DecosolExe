from tkinter import * 
from tkinter import messagebox, filedialog # filedialog para guardar con ventana y poner nombre
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import sqlite3
import webbrowser
from tkcalendar import Calendar
from datetime import datetime, date
import os
import sys
import time
import babel

tiempo = time.sleep(1)

fecha_actual = datetime.now()
dia = fecha_actual.day
mes = fecha_actual.month
año = fecha_actual.year


#---------------------------FUNCION DE DIRECCION ABSOLUTA------------------#
def ruta(relativa):
        if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relativa)
        return os.path.join(os.path.abspath("."), relativa)

#-----------------------------------------------------------------------------#

#Dimencion y posion de ventana
ancho_root= 750
alto_root = 500


#--------------FUNCIONES GLOBALES---------------#

def resaltar(event):
        event.widget.config(bg="#83b7c3")

        event.widget.after( 200, lambda: event.widget.config(bg="#289E55"))
def cerrar_rootIndex():
       a =  messagebox.askokcancel("Salir","Desea salir?")
       if a:
                root_index.destroy()

#_______________________________________________#

#Configurado
def stock(event):

        def cerrar(event):
                root_inventario.destroy()
                root_index.deiconify()
        root_index.withdraw()
        fuente = ("Arial" ,32 , "bold")
        fondo = "#289E55"
        def query_inventario():
                conexion = sqlite3.connect(ruta("DataBase"))
                pointer = conexion.cursor()
                pointer.execute("SELECT * FROM INVENTARIO")
                datos = pointer.fetchall()
                for items in datos:
                        tree_inventario.insert("",END, values=(items[0], items[1]))
                conexion.close()
        def agregar(event):
                def insertar():
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        pointer.execute("INSERT INTO INVENTARIO (ITEM, CANTIDAD) VALUES (?,?)",(intro_item.get().upper(), intro_cantidad.get().upper()))
                        conexion.commit()
                        conexion.close()
                        a = messagebox.showinfo("Agregar","Agregado exitoso")
                        if a == "ok":
                                root_inventario.destroy()
                                tiempo
                                stock(event=None)
                         
                ancho_root = 250
                alto_root = 250

                root_agg = Toplevel(root_inventario)
                alto_pantalla = root_agg.winfo_screenheight()
                ancho_pantalla = root_agg.winfo_screenwidth()
                pos_x_agg = (ancho_pantalla // 2 ) - (ancho_root // 2)
                pos_y_agg = (alto_pantalla // 2) - (alto_root // 2)
                root_agg.geometry(f"{ancho_root}x{alto_root}+{pos_x_agg}+{pos_y_agg}")

                frame = Frame(root_agg)
                frame.place(x=65, y=20)

                Label(frame, text="Descripcion").grid(row=0, column=0, pady=10)
                intro_item = Entry(frame,justify="center")
                intro_item.grid(row=1, column=0)

                Label(frame, text="Cantidad").grid(row=2, column=0, pady=10)

                intro_cantidad = Entry(frame,justify="center")
                intro_cantidad.grid(row=3, column=0)

                Button(frame, text="Agregar", command=insertar ).grid(row=4, column=0, pady=10)


                root_agg.mainloop()
        
        def actualizar(event):
                def update():
                        conexion = sqlite3.connect("DataBase")
                        pointer = conexion.cursor()
                        pointer.execute("UPDATE INVENTARIO SET CANTIDAD = ? WHERE ITEM = ?" , (entrada.get(),valor[0]))
                        conexion.commit()
                        conexion.close()
                        a = messagebox.showinfo("UPDATE","Cantidad Actualizada con exito")
                        if a =="ok":
                                root_inventario.destroy()
                                tiempo
                                stock(event=None)
                try:                
                        eleccion = tree_inventario.selection()
                        if eleccion:
                                for item_id in eleccion:
                                        item = tree_inventario.item(item_id)
                                        valor = item['values']
                  
                        ancho_u = 380
                        alto_u = 280                                     
                        root_update = Toplevel(root_inventario)
                        
                        root_update.geometry(f"{ancho_u}x{alto_u}+{((root_update.winfo_screenwidth() // 2) - (ancho_u // 2))}+{((root_update.winfo_screenheight() // 2) - (alto_u // 2))}")
                        root_update.config(bg="#f2d1f8")

                        frame = Frame(root_update,bg="#f2d1f8")
                        frame.place(x=50, y=20)

                        Label(frame, text="Descripcion", bg="#ea7ffb",width=20).grid(row=0,column=0)
                        Label(frame, text="Cantida",bg="#ea7ffb",width=20).grid(row=0,column=1)
                        Label(frame, text=valor[0],bg="#f2d1f8").grid(row=1, column=0)
                        Label(frame,text=valor[1],bg="#f2d1f8").grid(row=1, column=1)
                        Label(frame, text="Actualizar cantidad", bg="#f2d1f8").grid(row=2, column=0, columnspan=2, pady=10)
                        entrada = Entry(frame)
                        entrada.grid(row=3, column=0, columnspan=2)
                        Button(frame, text="Actualizar", command=update).grid(row=4, column=0, columnspan=2, pady=10)
                        

                        root_update.mainloop()
                except UnboundLocalError:
                        ms = messagebox.showerror("ERROR","Seleccione una opcion para actualizar")
                        if ms == "ok":
                                root_update.destroy()

        def eleminar(event):
                eleccion = tree_inventario.selection()
                if eleccion:
                        for item_id in eleccion:
                                item = tree_inventario.item(item_id)
                                valor = item['values']
                                                                               
                        a = messagebox.askyesno("Borrar","Seguro que desea eleminar este dato")
                        if a:   
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                pointer.execute("DELETE FROM INVENTARIO WHERE ITEM=?",(valor[0],))                                 
                                conexion.commit()
                                conexion.close()
                                messagebox.showinfo("Borrar","Dato borrado con exito")
                                root_inventario.destroy()
                                tiempo
                                stock(event=None)
                                
                                
        root_inventario = Toplevel(root_index)  #TOPLEVEL
        alto_pantalla = root_inventario.winfo_screenheight()
        ancho_pantalla = root_inventario.winfo_screenwidth()
        pos_x = (ancho_pantalla // 2 ) - (ancho_root // 2)
        pos_y = (alto_pantalla // 2) - (alto_root // 2)
        root_inventario.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root_inventario.title("Decosol - Inventario")
        root_inventario.protocol("WM_DELETE_WINDOW",cerrar_rootIndex)
        root_inventario.config(bg="#289E55")

        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
        
        atras = Label(root_inventario, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)

        atras.bind("<Button-1>", cerrar)

        frame_labels = Frame(root_inventario)
        frame_labels.place(x=250, y=10)

        frame_tree = Frame(root_inventario)
        frame_tree.place(x=130, y=70)

        frame_btns = Frame(root_inventario, bg=fondo)
        frame_btns.place(x=150, y=400)


        Label(frame_labels, text="Inventario", bg=fondo, font=fuente).grid(row=0, column=0)

        tree_inventario = ttk.Treeview(frame_tree, columns=("Item", "Cantidad"), height=15, show="headings")
        tree_inventario.grid(row=0,column=0)

        tree_inventario.heading("Item", text="Descripcion")
        tree_inventario.heading("Cantidad", text="Cantidad")

        tree_inventario.column("Item",width=250,anchor="center")
        tree_inventario.column("Cantidad",width=250,anchor="center")

        image = Image.open(ruta("imagenes/add.png"))
        alto_i , ancho_i = 50,50
        image = image.resize((alto_i, ancho_i))
        add_img = ImageTk.PhotoImage(image)

        image2 = Image.open(ruta("imagenes/reload.png"))
        image2 = image2.resize((alto_i, ancho_i))
        reload_img = ImageTk.PhotoImage(image2)

        image3 = Image.open(ruta("imagenes/delete.png"))
        image3 = image3.resize((alto_i, ancho_i))
        delete_img = ImageTk.PhotoImage(image3)

        add = Label(frame_btns, text="Agregar Item", image=add_img, compound='top', bg=fondo, font=("Arial", 12, "bold"))
        add.grid(row=0, column=0)
        add.bind("<Button-1>", resaltar)
        add.bind("<Double-Button-1>",agregar)

        refresh = Label(frame_btns, text="Actualizar Item", font=("Arial", 12, "bold"),bg=fondo, image=reload_img, compound='top')
        refresh.grid(row=0, column=1, padx=50)
        refresh.bind("<Button-1>",resaltar)
        refresh.bind("<Double-Button-1>",actualizar)

        delete = Label(frame_btns,text="Eleminar Item", font=("Arial", 12, "bold"), bg=fondo, image=delete_img, compound='top')
        delete.grid(row=0, column=2)
        delete.bind("<Button-1>", eleminar)
        

        query_inventario()
        root_inventario.mainloop()
        
def clientes(event):
        def cerrar(event):
                root_clientes.destroy()
                root_index.deiconify()
        def insertar_clientes():
                conexion = sqlite3.connect(ruta("DataBase"))
                pointer = conexion.cursor()
                pointer.execute("SELECT * FROM CLIENTES")
                datos = pointer.fetchall()
                for i in datos:
                        if i[2] == "SIN REGISTRO":
                                a = i[2]
                                a = ""
                                tree_clientes.insert("", END, values=(i[0], f"{i[1]} {a}", i[3]))
                        else:
                                tree_clientes.insert("", END, values=(i[0], f"{i[1]} {i[2]}", i[3]))
                conexion.close()
        #HACER FUNCION DE EDITAR LOS NOMBRES DE CLIENTES
        def editar():
                eleccion = tree_clientes.selection()
                if eleccion:
                        for item_id in eleccion:
                                item = tree_clientes.item(item_id)
                                valor = item['values']
                def asignar():
                        id_var.set(i[0])
                        name_var.set(i[1])
                        lame_var.set(i[2])
                        tlf_var.set(i[3])
                def actualizacion(event):
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        pointer.execute("UPDATE CLIENTES SET NOMBRE = ?, APELLIDO = ?, NUMERO_TLF = ? WHERE ID = ?",(name.get(), lastme.get(),str(tlf.get()),id.get()))
                        conexion.commit()
                        conexion.close()
                        b = messagebox.showinfo("UPDATE","Se actualizo Correctamente")
                        if b:
                                root_clientes.destroy()
                                tiempo
                                clientes(event=None)
                conexion = sqlite3.connect(ruta("DataBase"))
                pointer = conexion.cursor()
                pointer.execute("SELECT * FROM CLIENTES WHERE ID = ?", (valor[0],))
                datos = pointer.fetchall()
                for i in datos:
                        pass
                conexion.close()
                root_editio_client = Toplevel(root_clientes)
                root_editio_client.geometry(f"550x80+{((root_editio_client.winfo_screenwidth() // 2) - (550 // 2 ))}+{((root_editio_client.winfo_screenheight() // 2) - (80 // 2))}")
                frame_s = Frame(root_editio_client)
                frame_s.pack()
                Label(frame_s, text="ID").grid(row=0, column=0)
                Label(frame_s, text="Nombre").grid(row=0, column=1)
                Label(frame_s, text="Apellido").grid(row=0, column=2)
                Label(frame_s, text="Tlf").grid(row=0, column=3)

                id_var = StringVar()    
                id = Entry(frame_s, textvariable=id_var, state='disabled') 
                id.grid(row=1, column=0)

                name_var = StringVar()
                name = Entry(frame_s, textvariable=name_var)
                name.grid(row=1, column=1, padx=10)

                lame_var = StringVar()
                lastme = Entry(frame_s, textvariable=lame_var)
                lastme.grid(row=1, column=2)

                tlf_var = StringVar()
                tlf = Entry(frame_s, textvariable=tlf_var)
                tlf.grid(row=1, column=3, padx=10)
                Button(frame_s, text="Aceptar",width=15, command=lambda:actualizacion("<Return>")).grid(row=2, column=0, columnspan=4, pady=10)
                asignar()
                root_editio_client.bind("<Return>" ,actualizacion)
                root_editio_client.mainloop()
        def delete():
                eleccion = tree_clientes.selection()
                if eleccion:
                        for item_id in eleccion:
                                item = tree_clientes.item(item_id)
                                valor = item['values']
                a = messagebox.askyesno("Borrar", "Seguro que desea eliminar cliente")
                if a:
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        pointer.execute("DELETE FROM CLIENTES WHERE ID = ?",(valor[0],))
                        conexion.commit()
                        conexion.close()
                        messagebox.showinfo("Borrar","Cliente Eliminado con exito")
                        root_clientes.destroy()
                        tiempo
                        clientes(event=None)

        root_index.withdraw()
        root_clientes = Toplevel(root_index)
        root_clientes.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root_clientes.protocol("WM_DELETE_WINDOW",cerrar_rootIndex)
        root_clientes.config(bg="#289E55")
        root_clientes.title("Clientes")

        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
        
        atras = Label(root_clientes, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)

        atras.bind("<Button-1>", cerrar)

        frame = Frame(root_clientes, bg="#289E55")
        frame.place(x=150, y=20)
        frame_btn = Frame(root_clientes, bg="#289E55")
        frame_btn.place(x=250, y=400)

        Label(frame, text="Clientes", font=("Arial", 20, "bold"), bg="#289E55").grid(row=0, column=0)

        tree_clientes  = ttk.Treeview(frame, columns=("ID", "NOMBRE_APELLIDO", "TLF"), show="headings", height=15)
        tree_clientes.grid(row=1, column=0, pady=15)

        tree_clientes.heading("ID", text="ID")
        tree_clientes.heading("NOMBRE_APELLIDO", text="Nombre y Apellido")
        tree_clientes.heading("TLF", text="Telefono")

        tree_clientes.column("ID",width=80,anchor="center")
        tree_clientes.column("NOMBRE_APELLIDO", width=150,anchor="center")
        tree_clientes.column("TLF", width=200,anchor="center")
        insertar_clientes()

        Button(frame_btn, text="Editar", command=editar, width=15).grid(row=0, column=0)
        Button(frame_btn, text="Eliminar", command=delete, width=15).grid(row=0, column=1, padx=10, pady=15)
        root_clientes.mainloop()

def consulta_ventas(event):    
        def cerrar(event):
               root_ventas.destroy()
               root_index.deiconify()   
        #SUB VENTANA VENTAS PENDIENTE
        def ventas_pendientes(event):
                root_ventas.withdraw()
                
                def salir_pendiente(event):
                        root_ventas.deiconify()
                        root_ventas_pendientes.destroy()
                
                def query_ventas_pendiente():
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        pendiente = "PENDIENTE"
                        pointer.execute("SELECT * FROM VENTAS WHERE STATUS = ?",(pendiente,))
                        datos = pointer.fetchall()
                        
                        for intems in datos:
                               tree.insert("",END, values=(intems[0],intems[1],intems[2],intems[3],intems[4],intems[8],intems[9]))
                        conexion.close()
                                
                def actualizar_venta(event):                        
                        eleccion = tree.selection()
                        if eleccion:
                                for item in eleccion:
                                        item_id = tree.item(item)
                                        valor = item_id['values']
                                        
                        #ACTUALIZAR AUTOMATICAMENTE LA FILA DE STATUS CUANDO DEUDA SEA 0  
 
                        
                        def procesar_update():
                                
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                pointer.execute("SELECT * FROM VENTAS WHERE ID = ?",(valor[0],))
                                datos = pointer.fetchall()
                                for up in datos:
                                        print(up[6])
                                conexion.close()

                                update_deuda = float(valor[5]) - float(update_entry.get())
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                pointer.execute("UPDATE VENTAS SET SEGUNDO_PAGO = ? , MDO_PAGO_SEGUNDO = ? , DEUDA = ? WHERE ID = ?",(update_entry.get(),lista.get(),update_deuda,valor[0]))
                                conexion.commit()
                                conexion.close()
                                
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                estado = "PROCESADA"
                                cantidad = 0
                                pointer.execute("UPDATE VENTAS SET STATUS = ? WHERE DEUDA = ? ",(estado, cantidad))
                                conexion.commit()
                                conexion.close()
                                
                                a = messagebox.showinfo("UPDATE","Listo")

                                #ACTUALIZA LA VENTANA CUANDO SE PRECIONE ACEPTAR DEL LISTO
                                if a == "ok":
                                        root_ventas_pendientes.destroy()
                                        tiempo
                                        ventas_pendientes(event=None)    
                        root_update = Toplevel(root_ventas_pendientes)
                        root_update.geometry("376x280+650+400")
                        root_update.config(bg="#f2d1f8")
                        
                        Label(root_update, text="PAGO", font=("Arial", 12,"bold"),bg="#ea7ffb", width=37).grid(row=0, column=0, columnspan=4)
                        Label(root_update, text="Cliente",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=0)
                        Label(root_update, text="Descripcion",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=1)
                        Label(root_update, text="Deuda",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=2)
                        Label(root_update, text="Paga",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=3)
                        Button(root_update, text="Procesar", bg="#fd8fff", font=("Arial",10,"bold"), command=procesar_update).grid(row=8, column=0, columnspan=4, pady=10)
                        opciones = ["METODOS","EFECTIVO", "PAGO MOVIL", "ZELLE"]
                        seleccion = StringVar()
                        lista = ttk.Combobox(root_update, values=opciones, textvariable=seleccion, state="readonly", font=("Arial",10,"bold"), justify="center")
                        lista.grid(row=3, column=0, columnspan=3)
                        lista.current(0)

                        Label(root_update, text=valor[1],bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=2, column=0)
                        Label(root_update, text=valor[2],bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=2, column=1)
                        Label(root_update, text=valor[5],bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=2, column=2)
                        update_entry = Entry(root_update, width=5)
                        update_entry.grid(row=2,column=3)
                        root_update.mainloop()
                
                def eliminar_venta():
                        eleccion = tree.selection()
                        if eleccion:
                                for item in eleccion:
                                        item_id = tree.item(item)
                                        valor = item_id['values']
                                        conexion = sqlite3.connect(ruta("DataBase"))
                                        pointer = conexion.cursor()
                                        pointer.execute("DELETE FROM VENTAS WHERE ID=?",(valor[0],))
                                        conexion.commit()
                                        conexion.close()
                                        a = messagebox.askyesno("Borrar","Seguro que desea eleminar este dato")
                                        if a:   
                                                messagebox.showinfo("Borrar","Venta eliminada")
                                                root_ventas_pendientes.destroy()
                                                tiempo
                                                ventas_pendientes(event=None)

                root_ventas_pendientes = Toplevel(root_ventas)
                root_ventas_pendientes.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
                root_ventas_pendientes.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
                root_ventas_pendientes.config(bg="#289E55")
                root_ventas_pendientes.title("Ventas - Pendientes")

                image_back = Image.open(ruta("imagenes/Back.png"))
                image_back=image_back.resize((50,50))
                back_img = ImageTk.PhotoImage(image_back)
                
                atras = Label(root_ventas_pendientes, image=back_img, bg="#289E55")
                atras.place(x=650, y=400)

                frame = Frame(root_ventas_pendientes, bg="#289E55")
                frame.place(x=280 , y=300)

                atras.bind("<Button-1>", salir_pendiente)
                
                Button(frame, text="Procesar Venta", command=lambda:actualizar_venta("<Button-1>")).grid(row=0, column=0)
                Button(frame, text="Eliminar venta", command=eliminar_venta).grid(row=0, column=1, padx=25)

                tree = ttk.Treeview(root_ventas_pendientes, columns=("ID","CLIIENTE", "DESCRIPCION", "PRECIO A PAGAR", "ABONO", "DEBE", "FECHA ENTREGA"), show="headings", height=10)
                tree.config()
                tree.place(x=50, y=50)

                tree.heading("ID", text="ID")
                tree.heading("CLIIENTE", text="Cliente")
                tree.heading("DESCRIPCION", text="Descripcion")
                tree.heading("PRECIO A PAGAR", text="Precio a Pagar")
                tree.heading("ABONO", text="Abono")
                tree.heading("DEBE", text="Debe")
                tree.heading("FECHA ENTREGA", text="Fecha Entrega")

                tree.column("ID", width=30, anchor="center")
                tree.column("CLIIENTE", width=100, anchor="center")
                tree.column("DESCRIPCION", width=150, anchor="center")
                tree.column("PRECIO A PAGAR", width=100, anchor="center")
                tree.column("ABONO", width=100, anchor="center")
                tree.column("DEBE", width=100, anchor="center")
                tree.column("FECHA ENTREGA", width=100, anchor="center")
                query_ventas_pendiente()

                tree.bind("<Double-Button-1>", actualizar_venta)
        
                root_ventas_pendientes.mainloop()   
        #SUB VENTANA SECCION DE VENTAS PROCESADAS

        #//Hacer ficha de detalles de ventas procesadas\\
        def ventas_procesadas(event):
                def regresar(event):
                        root_ventas.deiconify()
                        root_proces_ventas.destroy()
                def detalles():
                
                        eleccion = tree_proces.selection()                     
                        if eleccion:
                                for item in eleccion:
                                        item_id = tree_proces.item(item)
                                        valor = item_id['values']                                               
                        def query():
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                pointer.execute("SELECT * FROM VENTAS WHERE ID = ?",(valor[0],))
                                datos = pointer.fetchall()
                                        
                                for i in datos:

                                        return i
                                               
                        ancho_window = 350
                        alto_window = 250

                        root_detalles = Toplevel(root_proces_ventas)
                        root_detalles.title("Detalles")
                        root_detalles.config(bg="#289E55")
                        alto_pantalla = root_detalles.winfo_screenheight()
                        ancho_pantalla = root_detalles.winfo_screenwidth()
                        pos_x = (ancho_pantalla // 2) - (ancho_window // 2)
                        pos_y = (alto_pantalla // 2) - (alto_window // 2)
                        root_detalles.geometry(f"{ancho_window}x{alto_window}+{pos_x}+{pos_y}")
                        try:
                                frame_nro = Frame(root_detalles, height=12, width=25 , bg="black")
                                frame_nro.place(x=230, y=40)
                                
                                frame_datos = Frame(root_detalles, bg="#289E55")
                                frame_datos.place(x=40, y=50)

                                frame_name = Label(root_detalles, bg="#289E55")
                                frame_name.place(x=100, y=5)

                                name = Label(frame_name, text=f"{valor[1]}", font=("Arial", 15, "bold"), bg="#289E55")
                                name.grid(row=0, column=0)

                                nro = Label(frame_nro, text=f"Numero 0{valor[0]}", font=("Arial" , 12, "bold"), bg="#289E55")
                                nro.grid(row=0 , column=0)

                                pago = query()

                                Label(frame_datos, text="Primer Pago", font=("Arial", 12, "bold"), bg="#289E55").grid(row=0, column=0 , columnspan=2, pady=20)

                                mto_pri_pago = Label(frame_datos, text=f"{pago[5]}", bg="#289E55")
                                mto_pri_pago.grid(row=1, column=0)

                                monto_uno= Label(frame_datos, text=f"${pago[4]}", bg="#289E55")
                                monto_uno.grid(row=1, column=1, padx=20)

                                Label(frame_datos, text="Segundo Pago", font=("Arial", 12, "bold"), bg="#289E55").grid(row=2, column=0, columnspan=2, pady=20)

                                mto_pri_pago2 = Label(frame_datos, text=f"{pago[7]}", bg="#289E55")
                                mto_pri_pago2.grid(row=3, column=0)

                                monto_dos= Label(frame_datos, text=f"${pago[6]}", bg="#289E55")
                                monto_dos.grid(row=3, column=1, padx=20)
                        except:
                                messagebox.showerror("ERROR", "No has elegido ninguna venta, seleccione una para ver mas detalles")
                        root_detalles.mainloop()
                def consulta():
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        pendiente = "PROCESADA"
                        pointer.execute("SELECT * FROM VENTAS WHERE STATUS = ?",(pendiente,))
                        datos = pointer.fetchall()
                        for items in datos:

                               tree_proces.insert("",END,values=(items[0],items[1],items[2],items[3],items[9] ))
                        
                        conexion.close()
                        return datos
                def filtrar(event):
                        datos = consulta()
                        filtro = entrada.get().upper()

                        for row in tree_proces.get_children():
                                tree_proces.delete(row)
                          
                        for items in datos:
                                
                                if filtro in str(items[0]) or filtro in items[1] or filtro in items[2] or filtro in str(items[3]) or filtro in items[9]:
                                        tree_proces.insert("", END, values=(items[0],items[1], items[2],items[3], items[9]))
                def calendario(event):
                        top = Toplevel(root_proces_ventas)
                        x = 260
                        y = 230
                        top.geometry(f"{260}x{230}+{pos_x}+{pos_y}")
                        top.title("Fecha")
                        calendario = Calendar(top,selecmode="day", date_pattern= "dd/m/yy",locale='es_ES',year=año, month=mes , day = dia)
                        calendario.pack()
                        def fecha_get():
                                date = calendario.get_date()
                                var_intro.set(date)
                                top.destroy()
                        Button(top, text="Seleccionar", command=fecha_get).pack(pady=10)
                root_proces_ventas = Toplevel(root_ventas) 
                root_proces_ventas.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
                root_proces_ventas.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
                root_proces_ventas.title("Ventas Procesadas")
                root_proces_ventas.config(bg="#289E55")

                image_back = Image.open(ruta("imagenes/Back.png"))
                image_back=image_back.resize((50,50))
                back_img = ImageTk.PhotoImage(image_back)
                
                atras = Label(root_proces_ventas, image=back_img, bg="#289E55")
                atras.place(x=650, y=430)
                atras.bind("<Button-1>", regresar)


                Button(root_proces_ventas, text="Buscar", command=lambda:filtrar("<Return>"), width=10).place(x=350, y=35)
                
                Button(root_proces_ventas, text="Ver", command=detalles, width=10).place(x=450, y=35)


                Label(root_proces_ventas, text="Filtrar Venta", font=("Arial" , 12, "bold"), bg="#289E55").place(x=115,y=10)
                ima_calen = Image.open(ruta("imagenes/calendario.png"))
                ancho, alto = 30,30
                ima_calen = ima_calen.resize((ancho, alto))
                photo = ImageTk.PhotoImage(ima_calen)

                ima_lup = Image.open(ruta("imagenes/search.png"))
                ancho, alto = 30,30
                ima_lup = ima_lup.resize((ancho, alto))
                photo_lupa = ImageTk.PhotoImage(ima_lup)
                

                abrir_calen = Label(root_proces_ventas, text="Calendario", bg="#289E55", font=("Arial",10, "bold"), image=photo, compound='bottom')
                abrir_calen.place(x=240, y=20)
                abrir_calen.bind("<Button-1>", resaltar)
                abrir_calen.bind("<Double-Button-1>",calendario)

                Label(root_proces_ventas,image=photo_lupa, bg="#289E55").place(x=60, y=30)

                var_intro = StringVar()
                entrada = Entry(root_proces_ventas, textvariable=var_intro)
                entrada.place(x=100, y=40)

                tree_proces = ttk.Treeview(root_proces_ventas, columns=("ID","CLIIENTE", "DESCRIPCION", "PRECIO A PAGAR", "FECHA ENTREGA"), show="headings", height=15)
                tree_proces.place(x=80, y=80)

                tree_proces.heading("ID", text="ID")
                tree_proces.heading("CLIIENTE", text="Cliente")
                tree_proces.heading("DESCRIPCION", text="Descripcion")
                tree_proces.heading("PRECIO A PAGAR", text="Pago")
                tree_proces.heading("FECHA ENTREGA", text="Fecha Entregada")

                tree_proces.column("ID", width=30, anchor="center")
                tree_proces.column("CLIIENTE", width=150, anchor="center")
                tree_proces.column("DESCRIPCION", width=150, anchor="center")
                tree_proces.column("PRECIO A PAGAR", width=150, anchor="center")
                tree_proces.column("FECHA ENTREGA", width=150, anchor="center")
                
                consulta()
                root_proces_ventas.bind("<Return>", filtrar) 
                root_proces_ventas.mainloop()
                             
        #SUB VENTA AGREGAR VENTA
        def agg_ventas_f(event):         
                root_ventas.withdraw()
                def regresar(event):
                        root_ventas.deiconify()
                        root_add_ventas.destroy()
                        
                def registro_de_venta():
                                                     
                        separador = Cliente_entry.get().split(" ")
                        name_cl = Cliente_entry.get().upper()
                        n_descriptcion  = descripcion.cget("text")
                        n_fecha = fecha_resultado.cget("text")
                        n_monto = monto.cget("text")
                        n_abono = abono.get()
                        state = "PENDIENTE"
                        modo = lista.get().upper()
                        apellido = "SIN REGISTRO"
                        telefono = nrm.get()
                        deuda = float(n_monto) - float(n_abono)
                        sdo_pago = "PENDIENTE"
                        mdto_pago2 = "PENDIENTE"

                        datos = name_cl, n_descriptcion, n_monto, n_abono,modo,sdo_pago,mdto_pago2,deuda,n_fecha,state,
                        conexion = sqlite3.connect(ruta("DataBase"))

                        pointer = conexion.cursor()

                        pointer.execute("INSERT INTO VENTAS (NOMBRE_CLIENTE,DESCRIPCION,PRECIO_PAGAR,PRIMER_PAGO, MDO_PRIMER_PAGO,SEGUNDO_PAGO,MDO_PAGO_SEGUNDO,DEUDA,FECHA,STATUS) VALUES (?,?,?,?,?,?,?,?,?,?)", datos)
                        if variable_check.get() == 1:
                                if len(separador) == 1:
                                        pointer.execute("INSERT INTO CLIENTES (NOMBRE, APELLIDO,NUMERO_TLF) VALUES (?,?,?)",(Cliente_entry.get(),apellido, telefono))
                                if len(separador) == 2:
                                        pointer.execute("INSERT INTO CLIENTES (NOMBRE, APELLIDO,NUMERO_TLF) VALUES (?,?,?)",(separador[0],separador[1], telefono))
                        conexion.commit()
                        conexion.close()
                        

                        messagebox.showinfo("Venta","Venta registrada con exito")

                        cliente_text.set("")
                        descripcion.config(text="")
                        fecha_resultado.config(text="")
                        monto.config(text="")
                        abono_text.set("")
                        telfono_var.set("")
                                             
                def salir_agregar():
                        root_ventas.deiconify()
                        root_add_ventas.destroy()

                
                def juego():
                        if variable_check.get() == 1:
                                nrm.config(state='normal')
                                telfono_var.set("")
                                
                        else:
                                nrm.config(state='disabled')
                                telfono_var.set("BLOCK")

                def buscar_cliente():
                        def tree_clients():
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                pointer.execute("SELECT * FROM CLIENTES")
                                datos = pointer.fetchall()
                                print(datos)
                                for i in datos:
                                        if i[2] == "SIN REGISTRO":
                                                a = i[2]
                                                a = ""
                                                tree_clientes.insert("", END, values=(i[0], f"{i[1]} {a}", i[3]))
                                        else:
                                                tree_clientes.insert("", END, values=(i[0], f"{i[1]} {i[2]}", i[3]))
                                conexion.close()
                        def select():
                                eleccion = tree_clientes.selection()
                                if eleccion:
                                         for item_id in eleccion:
                                                item = tree_clientes.item(item_id)
                                                valor = item['values']
                                cliente_text.set(valor[1])
                                telfono_var.set(valor[2])
                                root_clientes.destroy()
                        rancho = 520
                        ralto = 300
                        root_clientes = Toplevel(root_add_ventas)
                        root_clientes.geometry(f"{rancho}x{ralto}+{((root_clientes.winfo_screenwidth() // 2) - (rancho // 2 ))}+{((root_clientes.winfo_screenheight() // 2) - (ralto // 2))}")
                        
                        frame_tree = Frame(root_clientes)
                        frame_tree.place(x=50, y=20)

                        tree_clientes  = ttk.Treeview(frame_tree, columns=("ID", "NOMBRE_APELLIDO", "TLF"), show="headings", height=10)
                        tree_clientes.grid(row=1, column=0, pady=15)

                        tree_clientes.heading("ID", text="ID")
                        tree_clientes.heading("NOMBRE_APELLIDO", text="Nombre y Apellido")
                        tree_clientes.heading("TLF", text="Telefono")

                        tree_clientes.column("ID",width=80,anchor="center")
                        tree_clientes.column("NOMBRE_APELLIDO", width=150,anchor="center")
                        tree_clientes.column("TLF", width=200,anchor="center")
                        tree_clients()
                        Button(root_clientes, text="Aceptar", command=select).place(x=250, y=270)
                        root_clientes.mainloop()

                root_add_ventas = Toplevel(root_ventas)
                root_add_ventas.title("Agregar")
                root_add_ventas.protocol("WM_DELETE_WINDOW", salir_agregar)
                root_add_ventas.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
                root_add_ventas.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
                root_add_ventas.config(bg="#289E55")
                Label(root_add_ventas, text="Agregar Venta", font=("Arial" ,35, "bold"), bg="#289E55").place(x=220, y=15)

                image_back = Image.open(ruta("imagenes/Back.png"))
                image_back=image_back.resize((50,50))
                back_img = ImageTk.PhotoImage(image_back)
                
                atras = Label(root_add_ventas, image=back_img, bg="#289E55")
                atras.place(x=650, y=430)
                atras.bind("<Button-1>", regresar)
                
                fondo = "#289E55"
                main = Frame(root_add_ventas, bg=fondo)
                main.place(x=150, y=100)
                fuente = ("Arial", 15, "bold")
                #CLIENTE
                Label(main, text="Cliente: ", font=fuente, bg=fondo).grid(row=0, column=0)
                cliente_text = StringVar()
                Cliente_entry = Entry(main, font=fuente, textvariable=cliente_text)
                Cliente_entry.grid(row=0, column=1, padx=5)
                                       
                 
                variable_check = IntVar()
                verificacion = Checkbutton(main, text="Registrar", font=fuente,variable=variable_check, bg=fondo, command=juego)
                verificacion.grid(row=0, column=2)
                
                Button(main, text= "Buscar", command=buscar_cliente).grid(row=0, column=3, padx=5)
               

                #DESCRIPCION
                #TERMINAR ESTA BUSQUEDA LUEGO IR A CONSULTA DE PRODUCTOS
                def busqueda_individuales():
                        def enviar_in (event):
                                listbox.delete(0, END)
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                intro = entrada.get().upper() 
                                intro2 = entrada.get().upper()
                                intro3 = entrada.get().upper()
                                intro4 = entrada.get().upper()
                                
                                pointer.execute("SELECT * FROM ITEM_INDIVIDUALES WHERE DESCRIPCION LIKE ? OR DESCRIPCION LIKE ? OR GRUPO LIKE ? OR ITEM LIKE ?",(f'%{intro}%',f'%{intro2}%,', f'%{intro3}%', f'%{intro4}%'))
                                datos = pointer.fetchall()
                                
                                for fila in datos:
                                       listbox.insert(END, f"{fila[5]}")

                                def seleccion():
                                       eleccion = listbox.curselection()
                                       
                                       if eleccion:
                                              valor = listbox.get(eleccion)
                                              pointer.execute("SELECT * FROM ITEM_INDIVIDUALES WHERE DESCRIPCION = ?",(valor,))
                                              query = pointer.fetchall()
                                              
                                              for price in query:
                                                     pass

                                              descripcion.config(text=valor, wraplength=150, bg="white")
                                              monto.config(text=price[6], bg="white")
                                              conexion.close()
                                              root_indi.destroy()
                                             
                                Button(frame_res, text="Seleccionar", command=seleccion).grid(row=2, column=0, columnspan=3, pady=5)



                        root_indi = Toplevel(root_add_ventas)
                        x = 450
                        y = 350
                        alto = root_indi.winfo_screenheight()
                        ancho = root_indi.winfo_screenwidth()
                        poy = (alto // 2) - (y // 2)
                        pox = (ancho // 2) - (x // 2)
                        
                        root_indi.geometry(f"{x}x{y}+{pox}+{poy}")
                        root_indi.title("Individuales")

                        frame_entry= Frame(root_indi)
                        frame_entry.place(x=90, y=10)

                        frame_res = Frame(root_indi)
                        frame_res.place(x=40, y=60)

                        entrada = Entry(frame_entry)
                        entrada.grid(row=0, column=0)

                        listbox = Listbox(frame_res, height=10, width=50, xscrollcommand=lambda f, l: [scrollbar_h.set(f, l), listbox.xview(f, l)],
                        yscrollcommand=lambda f, l: [scrollbar_v.set(f, l), listbox.yview(f, l)])
                        scrollbar_v = Scrollbar(frame_res, orient=VERTICAL, command=listbox.yview)
                        scrollbar_h = Scrollbar(frame_res, orient=HORIZONTAL, command=listbox.xview)
                        # Asociar los Scrollbars con el Listbox
                        listbox.config(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

                        # Posicionar el Listbox y los Scrollbars en el frame
                        listbox.grid(row=0, column=0, sticky='nsew')
                        scrollbar_v.grid(row=0, column=1, sticky='ns')
                        scrollbar_h.grid(row=1, column=0, sticky='ew')

                        # Hacer que el frame se expanda cuando se redimensione la ventana
                        frame_res.grid_rowconfigure(0, weight=1)
                        frame_res.grid_columnconfigure(0, weight=1)

                        root_indi.bind("<Return>", enviar_in)



                        Button(frame_entry, text="enviar", command=lambda:enviar_in("<Return>"), width=10).grid(row=0, column=1, padx=5)
                       
                def busqueda_ramos():
                        def enviar(event):
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                intro = entrada.get().upper()     
                                pointer.execute("SELECT * FROM RAMOS WHERE TIPO_RA=?",(intro,))
                                datos = pointer.fetchall()
                                for i in datos:
                                       pass
                                def selecion():
                                       descripcion.config(text=i[2], bg="white")
                                       monto.config(text=i[3], bg="white")
                                       root_ramos.destroy()
                                Label(frame_res, text="CODIGO").grid(row=0, column=0)
                                Label(frame_res, text="DESCRIPCION").grid(row=0, column=1)
                                Label(frame_res, text="PRECIO").grid(row=0, column=2)
                                
                                Label(frame_res, text=i[1]).grid(row=1, column=0)
                                Label(frame_res, text=i[2]).grid(row=1, column=1)
                                Label(frame_res, text=i[3]).grid(row=1, column=2)
                                Button(frame_res, text="Seleccionar", command=selecion).grid(row=1, column=3)  
                        root_ramos = Toplevel(root_add_ventas)
                        alto = root_ramos.winfo_screenheight()
                        ancho = root_ramos.winfo_screenwidth()
                        x = 300
                        y = 150
                        poy = (alto // 2) - (y // 2)
                        pox = (ancho // 2) - (x // 2)
                        

                        root_ramos.geometry(f"{x}x{y}+{pox}+{poy}")
                        root_ramos.title("Ramos")

                        frame_entry= Frame(root_ramos)
                        frame_entry.place(x=90, y=10)

                        frame_res = Frame(root_ramos)
                        frame_res.place(x=30, y=60)

                        entrada = Entry(frame_entry)
                        entrada.grid(row=0, column=0)
                        Button(frame_entry, text="enviar", command=lambda:enviar(event=None)).grid(row=1, column=0, pady=5)
                        root_ramos.bind("<Return>", enviar)
                       
                Label(main, text="Descripcion",font=fuente, bg=fondo).grid(row=1, column=0)

                
                descripcion = Label(main, font=fuente, bg="grey", width=18)
                descripcion.grid(row=1, column=1)
                
                btn_ramos = Button(main, text="Ramos", command=busqueda_ramos)
                btn_ramos.grid(row=1, column=2)

                btn_indi = Button(main, text="Individuales", command=busqueda_individuales)
                btn_indi.grid(row=1, column=3)

                #FECHA
                def abrir_calendario(event):
                        top = Toplevel(root_add_ventas)
                        top.geometry("260x230+700+350")
                        top.title("Fecha")
                        calendario = Calendar(top, selecmode='day', locale='es_ES' ,year=año, month=mes, day=dia)
                        calendario.pack()
                        def obtener_fecha():
                               date = calendario.get_date()
                               fecha_resultado.config(text=date, bg="white")
                               top.destroy()
                        Button(top, text="Seleccionar", command=obtener_fecha).pack(pady=10)

       
                Label(main, text="Fecha", font=fuente, bg=fondo).grid(row=3, column=0)
                
                fecha_resultado = Label(main, text="", bg="grey", font=fuente, width=18 )
                fecha_resultado.grid(row=3, column=1, pady=5)

                fecha = Label(main, text="Seleccionar", font=fuente, bg=fondo)
                fecha.bind("<Button-1>", resaltar)
                fecha.bind("<Double-Button-1>", abrir_calendario)
                fecha.grid(row=3, column=2)

                #MONTO
                Label(main, text="Monto a pagar :", font=fuente, bg=fondo).grid(row=4, column=0)
                monto  = Label(main, text="", bg="grey", font=fuente, width=18)
                monto.grid(row=4,column=1)

                Label(main, text="Monto Abonado", font=fuente, bg=fondo).grid(row=5, column=0)
                abono_text = StringVar()
                abono = Entry(main, text="", font=fuente, bg="white", textvariable=abono_text)
                abono.grid(row=5, column=1, pady=5)

                #METODO DE PAGO

                Label(main, text="Metodo de pago", font=fuente, bg=fondo).grid(row=6, column=0)
                opciones = ["METODOS","EFECTIVO", "PAGO MOVIL", "ZELLE"]
                seleccion = StringVar()
                lista = ttk.Combobox(main, values=opciones, textvariable=seleccion, state="readonly", font=("Arial",10,"bold"), justify="center")
                lista.grid(row=6, column=1)
                lista.current(0)

                #TELEFONO
                aviso = Label(main, text="Nro Tlf", bg=fondo, font=fuente)
                aviso.grid(row=7, column=0)
                
                telfono_var = StringVar()

                nrm = Entry(main, textvariable=telfono_var, font=fuente, justify='center')
                nrm.grid(row=7, column=1)
                nrm.config(state='disable')
                telfono_var.set("BLOCK")
                

                #BOTONES
                btn_envio = Button(main, text="Registro", command=registro_de_venta, font=fuente)
                btn_envio.grid(row=8, column=0, columnspan=6, pady=5)

                root_add_ventas.mainloop()
       #VENTANA DE SECCION DE VENTA 
        root_index.withdraw()
        root_ventas = Toplevel(root_index)
        root_ventas.title("Decosol- Ventas")
        root_ventas.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root_ventas.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
        root_ventas.config(bg="#289E55")

        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
        
        atras = Label(root_ventas, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)
        
        atras.bind("<Button-1>", cerrar)

        frame_optiones = Frame(root_ventas, bg="#289E55", width=250, height=250)
        frame_optiones.place(x=150, y=50)
        nuevo_alto, nuevo_ancho = 100,100
        imagen  = Image.open(ruta("imagenes/ventas_pendient.png"))
        nuevo_alto, nuevo_ancho
        imagen = imagen.resize((nuevo_alto, nuevo_ancho))
        pho  = ImageTk.PhotoImage(imagen)
        
        
        ventas_p = Label(frame_optiones, text="Ventas Pendientes", image=pho, font=("Arial", 12,"bold"), compound='top',bg="#289E55")
        ventas_p.grid(row=0, column=0)
        ventas_p.bind("<Button-1>", resaltar)
        ventas_p.bind("<Double-Button-1>", ventas_pendientes)

        imagen  = Image.open(ruta("imagenes/ventas.png"))
        nuevo_alto, nuevo_ancho
        imagen = imagen.resize((nuevo_alto, nuevo_ancho))
        pho_v  = ImageTk.PhotoImage(imagen)

        ventas = Label(frame_optiones, text="Ventas", image=pho_v, font=("Arial", 12,"bold"), compound='top',bg="#289E55")
        ventas.grid(row=0, column=1, padx=10)
        ventas.bind("<Button-1>", resaltar)
        ventas.bind("<Double-Button-1>", ventas_procesadas)

        imagen = Image.open(ruta("imagenes/add_venta.png"))
        imagen = imagen.resize((nuevo_alto, nuevo_ancho))
        photo_add = ImageTk.PhotoImage(imagen)

        agg_ventas = Label(frame_optiones, text="Agregar Ventas", image=photo_add, font=("Arial", 12,"bold"), compound='top',bg="#289E55")
        agg_ventas.grid(row=0, column=2, padx=10)
        agg_ventas.bind("<Button-1>", resaltar)
        agg_ventas.bind("<Double-Button-1>", agg_ventas_f)

        root_ventas.mainloop()

def consultor_de_precio(event):
        root_index.withdraw()
        opciones = ["Escoger Opcion","Ramos","Individuales"]
        seleccion = StringVar()
        def cerrar(event):
                        root2.destroy()
                        root_index.deiconify()
        def get_lista():
            a = lista.get()
            return a 
        def consulta_table(event):
                
                def mostrar_mas(event):
                        
                        eleccion = tree_indi.selection()
                        if eleccion:
                                for item_id in eleccion:
                                        item = tree_indi.item(item_id)
                                        valores = item['values']
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                pointer.execute("SELECT * FROM ITEM_INDIVIDUALES WHERE DESCRIPCION =?", (valores[1],))
                                datos = pointer.fetchall()
                                for k in datos:
                                        pass
                                try:        
                                        items = k[2].split(",")
                                        cantidad  = k[3].split(",")
                                        precio_u = k[4].split(",")
                                except:
                                        pass
                                conexion.close()
                                def creacion_de_imagen():
                                        fuente = ruta("C:\\Windows\\Fonts\\arial.ttf")
                                        #imagen blanca
                                        alto, ancho = 720, 1020
                                        fondo = Image.new('RGBA',(alto, ancho), color="#e9b2f2")

                                        dibujo = ImageDraw.Draw(fondo)

                                        imagen_montada = Image.open(ruta("imagenes/baner.png")).convert("RGBA")
                                        imagen_montada = imagen_montada.resize((200,50))
                                        fondo.paste(imagen_montada, (20,15),imagen_montada) #posicion

                                        producto = "Producto"
                                        cantidad_i = "Cantidad"
                                        precio_unidad = "Precio Unidad"
                                        precio_total = "Precio Total"
                                        monto_total = "Monto Total"

                                        font_es = ImageFont.truetype(fuente, 20)
                                        dibujo.text((100, 150), producto, fill="black", font=font_es)
                                        dibujo.text((230, 150), cantidad_i, fill="black", font=font_es)
                                        dibujo.text((347, 150), precio_unidad, fill="black", font=font_es)
                                        dibujo.text((520, 150), precio_total, fill="black", font=font_es)
                                
                                        if len(items) == 1:
                                                
                                                texto_a = k[2]
                                                dibujo.text((100,200), texto_a, fill="black", font=font_es)
                                                texto_b = str(k[3])
                                                dibujo.text((230,200), texto_b, fill="black", font=font_es)
                                                texto_c = str(k[4])
                                                dibujo.text((347,200), texto_c, fill="black", font=font_es)
                                                texto_d = str(k[6])
                                                dibujo.text((520,200), texto_d, fill="black", font=font_es)

                                                dibujo.text((520, 300), monto_total, fill="black", font=font_es)
                                                dibujo.text((520, 350), str(f"${k[6]}"), fill="black", font=font_es)
                                        elif len(items) == 2:
                                                resultado = f"{int(cantidad[0]) * float(precio_u[0])}"
                                                resultado2 = f"{int(cantidad[1])*float(precio_u[1])}"
                                                dibujo.text((100,200), items[0], fill="black", font=font_es) 
                                                dibujo.text((230,200),str(cantidad[0]), fill="black", font=font_es)     
                                                dibujo.text((347,200),str(precio_u[0]),fill="black", font=font_es)
                                                dibujo.text((520,200),str(resultado),fill="black", font=font_es)

                                                dibujo.text((100,250), items[1], fill="black", font=font_es) 
                                                dibujo.text((230,250),str(cantidad[1]), fill="black", font=font_es)     
                                                dibujo.text((347,250),str(precio_u[1]),fill="black", font=font_es)
                                                dibujo.text((520,250),str(resultado2),fill="black", font=font_es)

                                                dibujo.text((520, 300), monto_total, fill="black", font=font_es)
                                                dibujo.text((520, 350), str(f"${k[6]}"), fill="black", font=font_es)
                                        elif len(items) == 3:
                                                resultado = f"{int(cantidad[0]) * float(precio_u[0])}"
                                                resultado2 = f"{int(cantidad[1])*float(precio_u[1])}"
                                                resultado3 = f"{int(cantidad[2])*float(precio_u[2])}"


                                                dibujo.text((100,200), items[0], fill="black", font=font_es) 
                                                dibujo.text((230,200),str(cantidad[0]), fill="black", font=font_es)     
                                                dibujo.text((347,200),str(precio_u[0]),fill="black", font=font_es)
                                                dibujo.text((520,200),str(resultado),fill="black", font=font_es)

                                                dibujo.text((100,250), items[1], fill="black", font=font_es) 
                                                dibujo.text((230,250),str(cantidad[1]), fill="black", font=font_es)     
                                                dibujo.text((347,250),str(precio_u[1]),fill="black", font=font_es)
                                                dibujo.text((520,250),str(resultado2),fill="black", font=font_es)

                                                dibujo.text((100,300), items[2], fill="black", font=font_es) 
                                                dibujo.text((230,300),str(cantidad[2]), fill="black", font=font_es)     
                                                dibujo.text((347,300),str(precio_u[2]),fill="black", font=font_es)
                                                dibujo.text((520,300),str(resultado3),fill="black", font=font_es)

                                                dibujo.text((520, 400), monto_total, fill="black", font=font_es)
                                                dibujo.text((520, 450), str(f"${k[6]}"), fill="black", font=font_es)
                                        elif len(items) == 4:
                                                resultado = f"{int(cantidad[0]) * float(precio_u[0])}"
                                                resultado2 = f"{int(cantidad[1])*float(precio_u[1])}"
                                                resultado3 = f"{int(cantidad[2])*float(precio_u[2])}"
                                                resultado4 = f"{int(cantidad[3])*float(precio_u[3])}"
                                                

                                                dibujo.text((100,200), items[0], fill="black", font=font_es) 
                                                dibujo.text((230,200),str(cantidad[0]), fill="black", font=font_es)     
                                                dibujo.text((347,200),str(precio_u[0]),fill="black", font=font_es)
                                                dibujo.text((520,200),str(resultado),fill="black", font=font_es)

                                                dibujo.text((100,250), items[1], fill="black", font=font_es) 
                                                dibujo.text((230,250),str(cantidad[1]), fill="black", font=font_es)     
                                                dibujo.text((347,250),str(precio_u[1]),fill="black", font=font_es)
                                                dibujo.text((520,250),str(resultado2),fill="black", font=font_es)

                                                dibujo.text((100,300), items[2], fill="black", font=font_es) 
                                                dibujo.text((230,300),str(cantidad[2]), fill="black", font=font_es)     
                                                dibujo.text((347,300),str(precio_u[2]),fill="black", font=font_es)
                                                dibujo.text((520,300),str(resultado3),fill="black", font=font_es)

                                                dibujo.text((100,350), items[3], fill="black", font=font_es) 
                                                dibujo.text((230,350),str(cantidad[3]), fill="black", font=font_es)     
                                                dibujo.text((347,350),str(precio_u[3]),fill="black", font=font_es)
                                                dibujo.text((520,350),str(resultado4),fill="black", font=font_es)

                                                dibujo.text((520, 400), monto_total, fill="black", font=font_es)
                                                dibujo.text((520, 450), str(f"${k[6]}"), fill="black", font=font_es)
                                        fotoguardada = filedialog.asksaveasfilename( #abre una ventana para guardar la imagen
                                        defaultextension=".png",
                                        filetypes=[("PNG files","*.png"), ("All files","*,*")],
                                        title="Guardar Imagen"
                                        )          

                                        if fotoguardada:
                                                                                                                                                                
                                                fondo.save(fotoguardada)
                                                fondo.show() 
                                def abrir_whats():
                                        webbrowser.open("https://web.whatsapp.com/")
                                alto = 376
                                ancho = 280

                                root_mostrar_mas = Toplevel(root2)
                                pos_x = (ancho_pantalla // 2) - (ancho // 2)
                                pos_y = (alto_pantalla // 2) - (alto //2)
                                root_mostrar_mas.winfo_screenwidth()
                                root_mostrar_mas.grab_set()
                                root_mostrar_mas.config(bg="#f2d1f8")
                                root_mostrar_mas.geometry(f"{alto}x{ancho}+{pos_x}+{pos_y}")
                                
                                Label(root_mostrar_mas, text="CONSULTA", font=("Arial", 12,"bold"),bg="#ea7ffb", width=37).grid(row=0, column=0, columnspan=4)
                                Label(root_mostrar_mas, text="Producto",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=0)
                                Label(root_mostrar_mas, text="Cantidad",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=1)
                                Label(root_mostrar_mas, text="Precio Unidad",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=2)
                                Label(root_mostrar_mas, text="Precio Total",bg="#f2d1f8",font=("Arial",10,"bold")).grid(row=1, column=3)
                                Button(root_mostrar_mas, text="Exportar", command=creacion_de_imagen, bg="#fd8fff", font=("Arial",10,"bold")).grid(row=8, column=0, columnspan=4, pady=10)
                                Button(root_mostrar_mas, text="Abrir Whatsapp", command=abrir_whats, bg="#fd8fff", font=("Arial",10,"bold")).grid(row=9, column=0, columnspan=4)
                                if len(items) == 1:
                                        Label(root_mostrar_mas, text=k[2],bg="#f2d1f8").grid(row=2, column=0)
                                        Label(root_mostrar_mas, text=k[3],bg="#f2d1f8").grid(row=2, column=1) #cantidad
                                        Label(root_mostrar_mas, text=k[4],bg="#f2d1f8").grid(row=2, column=2) #precio U
                                        Label(root_mostrar_mas, text=k[6],bg="#f2d1f8").grid(row=2, column=3) #precio Total

                                elif len(items) == 2:
                                        Label(root_mostrar_mas, text=items[0],bg="#f2d1f8").grid(row=2, column=0) #item 1
                                        Label(root_mostrar_mas, text=cantidad[0],bg="#f2d1f8").grid(row=2, column=1) #cantidad 1
                                        Label(root_mostrar_mas, text=precio_u[0],bg="#f2d1f8").grid(row=2 , column=2) #precio U
                                        Label(root_mostrar_mas, text=f"{int(cantidad[0])*float(precio_u[0])}",bg="#f2d1f8").grid(row=2, column=3) #precio total
                                        
                                        Label(root_mostrar_mas, text=items[1],bg="#f2d1f8").grid(row=3, column=0) #item 2
                                        Label(root_mostrar_mas, text=cantidad[1],bg="#f2d1f8").grid(row=3, column=1) 
                                        Label(root_mostrar_mas, text=precio_u[1],bg="#f2d1f8").grid(row=3 ,column=2)
                                        Label(root_mostrar_mas, text=f"{int(cantidad[1])*float(precio_u[1])}",bg="#f2d1f8").grid(row=3, column=3)

                                        #---TOTAL---
                                        Label(root_mostrar_mas, text="Monto Total:",font=("Arial",10,"bold"),bg="#f2d1f8").grid(row=4, column=3)
                                        Label(root_mostrar_mas, text=f"${k[6]}",bg="#f2d1f8").grid(row=5, column=3)
                                elif len(items) == 3:
                                        Label(root_mostrar_mas, text=items[0],bg="#f2d1f8").grid(row=2, column=0) #item 1
                                        Label(root_mostrar_mas, text=cantidad[0],bg="#f2d1f8").grid(row=2, column=1) #cantidad 1
                                        Label(root_mostrar_mas, text=precio_u[0],bg="#f2d1f8").grid(row=2 , column=2) #precio U
                                        Label(root_mostrar_mas, text=f"{int(cantidad[0])*float(precio_u[0])}",bg="#f2d1f8").grid(row=2, column=3) #precio total
                                        
                                        Label(root_mostrar_mas, text=items[1],bg="#f2d1f8").grid(row=3, column=0) #item 2
                                        Label(root_mostrar_mas, text=cantidad[1],bg="#f2d1f8").grid(row=3, column=1) 
                                        Label(root_mostrar_mas, text=precio_u[1],bg="#f2d1f8").grid(row=3 ,column=2)
                                        Label(root_mostrar_mas, text=f"{int(cantidad[1])*float(precio_u[1])}",bg="#f2d1f8").grid(row=3, column=3)

                                        Label(root_mostrar_mas, text=items[2],bg="#f2d1f8").grid(row=4, column=0) #item 3
                                        Label(root_mostrar_mas, text=cantidad[2],bg="#f2d1f8").grid(row=4, column=1) 
                                        Label(root_mostrar_mas, text=precio_u[2],bg="#f2d1f8").grid(row=4 ,column=2)
                                        Label(root_mostrar_mas, text=f"{int(cantidad[2])*float(precio_u[2])}",bg="#f2d1f8").grid(row=4, column=3)

                                        #---TOTAL---
                                        Label(root_mostrar_mas, text="Monto Total:",bg="#f2d1f8").grid(row=5, column=3)
                                        Label(root_mostrar_mas, text=f"${k[6]}",bg="#f2d1f8").grid(row=6, column=3)
                                elif len(items) == 4:
                                        Label(root_mostrar_mas, text=items[0],bg="#f2d1f8").grid(row=2, column=0) #item 1
                                        Label(root_mostrar_mas, text=cantidad[0],bg="#f2d1f8").grid(row=2, column=1) #cantidad 1
                                        Label(root_mostrar_mas, text=precio_u[0],bg="#f2d1f8").grid(row=2 , column=2) #precio U
                                        Label(root_mostrar_mas, text=f"{int(cantidad[0])*float(precio_u[0])}",bg="#f2d1f8").grid(row=2, column=3) #precio total
                                        
                                        Label(root_mostrar_mas, text=items[1],bg="#f2d1f8").grid(row=3, column=0) #item 2
                                        Label(root_mostrar_mas, text=cantidad[1],bg="#f2d1f8").grid(row=3, column=1) 
                                        Label(root_mostrar_mas, text=precio_u[1],bg="#f2d1f8").grid(row=3 ,column=2)
                                        Label(root_mostrar_mas, text=f"{int(cantidad[1])*float(precio_u[1])}",bg="#f2d1f8").grid(row=3, column=3)

                                        Label(root_mostrar_mas, text=items[2],bg="#f2d1f8").grid(row=4, column=0) #item 3
                                        Label(root_mostrar_mas, text=cantidad[2],bg="#f2d1f8").grid(row=4, column=1) 
                                        Label(root_mostrar_mas, text=precio_u[2],bg="#f2d1f8").grid(row=4 ,column=2)
                                        Label(root_mostrar_mas, text=f"{int(cantidad[2])*float(precio_u[2])}",bg="#f2d1f8").grid(row=4, column=3)

                                        Label(root_mostrar_mas, text=items[3],bg="#f2d1f8").grid(row=5, column=0) #item 4
                                        Label(root_mostrar_mas, text=cantidad[3],bg="#f2d1f8").grid(row=5, column=1) 
                                        Label(root_mostrar_mas, text=precio_u[3],bg="#f2d1f8").grid(row=5 ,column=2)
                                        Label(root_mostrar_mas, text=f"{int(cantidad[3])*float(precio_u[3])}",bg="#f2d1f8").grid(row=5, column=3)



                                        #---TOTAL---
                                        Label(root_mostrar_mas, text="Monto Total:",bg="#f2d1f8").grid(row=6, column=3)
                                        Label(root_mostrar_mas, text=f"${k[6]}",bg="#f2d1f8").grid(row=7, column=3)
                      
                ramos  = get_lista()
                def query_ramos():
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        query = entrada_consulta.get().upper()
                        query2 = entrada_consulta.get().upper()
                        pointer.execute("SELECT * FROM RAMOS WHERE TIPO_RA LIKE ? OR CODIGO_RA LIKE ?", (f'%{query}%',f'%{query2}%'))
                        datos = pointer.fetchall()
                        for i in datos:                           
                                tree_ramos.insert("", END, values=(i[1], i[2], f"${i[3]}"))
                        conexion.close()
                def query_individuales():                        
                        conexion = sqlite3.connect(ruta("DataBase"))
                        pointer = conexion.cursor()
                        entrada = entrada_consulta.get().upper()
                        entrada2 = entrada_consulta.get().upper()
                        if entrada_consulta.get() == "":
                                messagebox.showerror("ALERT","Ingrese criterio de busqueda")
                        elif entrada_consulta.get() != "":
                                pointer.execute("SELECT * FROM ITEM_INDIVIDUALES WHERE DESCRIPCION LIKE ? OR GRUPO LIKE ?", (f'%{entrada}%',f'%{entrada2}%'))
                        datos_ind = pointer.fetchall()
                        if datos_ind == [] and entrada_consulta.get() != "":
                                messagebox.showerror("ALERT", "DATO NO ENCONTRADO, REGISTRELO PARA VER DETALLES")
                        for j in datos_ind:
                                tree_indi.insert("",END, values=(j[1], j[5], f"${j[6]}"))
                        conexion.close()
                        
                if ramos == opciones[1]:                            
                        tree_ramos = ttk.Treeview(frame_resultado, columns=("CODIGO", "DESCRIPCION", "PRECIO"), show="headings", height=15)
                        tree_ramos.grid(row=0, column=0)
                        tree_ramos.heading("CODIGO", text="Codigo")
                        tree_ramos.heading("DESCRIPCION", text="Descripcion")
                        tree_ramos.heading("PRECIO", text="Precio")
                        
                        tree_ramos.column("CODIGO", width=150, anchor="center")
                        tree_ramos.column("DESCRIPCION", width=150)
                        tree_ramos.column("PRECIO", width=150, anchor="center")
                        query_ramos()
                elif ramos == opciones[2]:                        
                        tree_indi = ttk.Treeview(frame_resultado, columns=("GRUPO", "DESCRIPCION", "PRECIO"), show="headings", height=15)
                        tree_indi.grid(row=0, column=0)
                        tree_indi.heading("GRUPO", text="Grupo")
                        tree_indi.heading("DESCRIPCION", text="Descripcion")
                        tree_indi.heading("PRECIO", text="Precio")
        
                        tree_indi.column("GRUPO", width=100, anchor="center")
                        tree_indi.column("DESCRIPCION", width=310, anchor="w")
                        tree_indi.column("PRECIO", width=100, anchor="center")
                        tree_indi.bind("<Double-Button-1>", mostrar_mas )
                        query_individuales()
                        Button(frame_table, text="Ver mas", command=lambda:mostrar_mas(event=None),font=("Arial" , 10, "bold")).grid(row=0, column=3, padx=20)
        root2 = Toplevel(root_index)
        root2.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
        root2.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root2.config(bg="#289E55")
        root2.title("Decosol - Consultor de precio")
        root2.resizable(False, False)
        root2.iconbitmap(ruta("recursos/icono.ico"))

        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
        
        atras = Label(root2, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)

        atras.bind("<Button-1>", cerrar)

        frame_table = Frame(root2, bg="#289E55")
        frame_table.place(x=130, y=80)

        frame_resultado = Frame(root2, bg="#289E55")
        frame_resultado.place(x=130 , y=150)

        aviso = Label(root2, text="Consultor", bg="#289E55")
        aviso.place(x=250, y=5)
        aviso.config(font=("Arial", 40, "bold"))

        lista = ttk.Combobox(frame_table,state="readonly", values=opciones, textvariable=seleccion, font=("Arial", 10, "bold"))
        lista.grid(row=0, column=0)
        lista.current(0)
        
        into = StringVar()
        entrada_consulta = Entry(frame_table, textvariable=into)
        entrada_consulta.grid(row=0, column=1, padx=10)
        entrada_consulta.config(font=("Arial" , 12, "bold"))

        boton_cta = Button(frame_table, text="Consulta", command=lambda:consulta_table("<Button-1>"))
        boton_cta.grid(row=0, column=2)
        boton_cta.config(font=("Arial" , 10, "bold"))

        

        root2.bind("<Return>", consulta_table)
        root2.mainloop()

def registrador_data(event):  
   ancho = 250
   alto = 90
   def windows_one_item():   
                def registro_datos():
                        a = in_item_aviso.get().upper()
                        b = in_cantidad.get()
                        c = in_item1.get()
                        ab = f"{b} {a}"
                        g = "GRUPO 1"
                        r = int(b) * float(c)                        
                        try:
                                conexion = sqlite3.connect(ruta("DataBase"))
                                pointer = conexion.cursor()
                                datos = g,in_item_aviso.get().upper(), in_cantidad.get(), in_item1.get(),ab, r
                                pointer.execute("INSERT INTO ITEM_INDIVIDUALES (GRUPO,ITEM, CANTIDAD, PRECIO_UNIDAD,DESCRIPCION, PRECIO_TOTAL) VALUES (?, ?, ?, ?, ?, ?)", datos)
                                conexion.commit()
                                conexion.close()
                                messagebox.showinfo("BBDD","Registro exitoso")                                
                        except sqlite3.IntegrityError:
                               messagebox.showerror("Registro", "Datos ya registrado")
                                                
                def cerrar(event):
                        root_index.deiconify() #mostrar ventana
                        root_Opcion1.destroy()
                      
                root_Opcion1 = Toplevel(root_index)
                pos_x = (ancho_pantalla // 2) - (ancho_root // 2)
                pos_y = (alto_pantalla // 2) - (alto_root // 2)
                root_Opcion1.protocol("WM_DELETE_WINDOW", cerrar_rootIndex) #Al presionar la X de la esquina, se cierra la ventana del item y regresa a la ventana principal
                root_Opcion1.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
                root_Opcion1.config(bg="#289E55")
                root_Opcion1.title("Decosol - Registra Datos")
                root_Opcion1.resizable(False, False)
                root_Opcion1.iconbitmap(ruta("recursos/icono.ico"))

                image_back = Image.open(ruta("imagenes/Back.png"))
                image_back=image_back.resize((50,50))
                back_img = ImageTk.PhotoImage(image_back)
                
                atras = Label(root_Opcion1, image=back_img, bg="#289E55")
                atras.place(x=650, y=25)

                atras.bind("<Button-1>", cerrar)

                
                aviso = Label(root_Opcion1, text="Registra Datos", bg="#289E55")
                aviso.place(x=190, y=10)
                aviso.config(font=("Arial", 35, "bold"))

                miframe = Frame(root_Opcion1, bg="#289E55")
                miframe.place(x=150, y=80)

                #-------------ITEM 1-------------------

                item_aviso = Label(miframe, text="Item", bg="#289E55")
                item_aviso.grid(row=1, column=0, sticky='w')
                item_aviso.config(font=("Arial" ,20, "bold"))

                texto_variable = StringVar()
                in_item_aviso=Entry(miframe, width=50,font=10, textvariable=texto_variable)
                in_item_aviso.grid(row=2, column=0)
                
                cantidad_monstrar = Label(miframe, text="Cantidad", bg="#289E55")
                cantidad_monstrar.grid(row=3, column=0,sticky='w')
                cantidad_monstrar.config(font=("Arial" ,20, "bold"))

                in_cantidad=Entry(miframe, width=50,font=10)
                in_cantidad.grid(row=4, column=0)

                precio_mostrar = Label(miframe, text="Precio ud", bg="#289E55")
                precio_mostrar.grid(row=5, column=0,sticky='w')
                precio_mostrar.config(font=("Arial", 20, "bold"))

                in_item1 = Entry(miframe, width=50, font=10)
                in_item1.grid(row=6, column=0)

                boton_query = Button(miframe, text="Registar", command=registro_datos)
                boton_query.config(font=("Arial" , 10, "bold"), width=15)
                boton_query.grid(row=7, column=0, pady=10)
                root_Opcion1.mainloop()
   def windows_two_item():   
                
        def registro_dato():

                a = f"{in_item_aviso.get().upper()},{in_item_aviso2.get().upper()}"
                b = f"{in_cantidad.get()},{in_cantidad2.get()}"
                c = f"{in_item1.get()},{in_item2.get()}"
                r = (float(in_item1.get()) * float(in_cantidad.get())) + (float(in_item2.get())*float(in_cantidad2.get()))
                g = "GRUPO 2"
                descrp = f"{in_cantidad.get()} {in_item_aviso.get().upper()} CON {in_cantidad2.get()} {in_item_aviso2.get().upper()}"
                conexion = sqlite3.connect(ruta("DataBase"))
                pointer = conexion.cursor()
                pointer.execute("INSERT INTO ITEM_INDIVIDUALES (GRUPO,ITEM, CANTIDAD, PRECIO_UNIDAD, DESCRIPCION ,PRECIO_TOTAL) VALUES (?,?,?,?,?,?)",(g,a,b,c,descrp,r))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("BBDD","Registro exitoso")
                
        def regresar(event):
               root_index.deiconify()
               root_opcion2.destroy()

        root_opcion2= Toplevel(root_index)
        pos_x = (ancho_pantalla // 2) - (ancho_root // 2)
        pos_y = (alto_pantalla // 2) - (alto_root // 2)
        root_opcion2.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
        root_opcion2.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root_opcion2.config(bg="#289E55")
        root_opcion2.title("Decosol -Registrar Datos")
        root_opcion2.resizable(False, False)
        root_opcion2.iconbitmap(ruta("recursos/icono.ico"))

        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
                
        atras = Label(root_opcion2, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)
        atras.bind("<Button-1>", regresar)

        
        aviso = Label(root_opcion2, text="Registrar Datos", bg="#289E55")
        aviso.place(x=185, y=5)
        aviso.config(font=("Arial", 35, "bold"))

        miframe = Frame(root_opcion2, bg="#289E55")
        miframe.place(x=180, y=100)

        #-------------ITEM 1-------------------
      
        item_aviso = Label(miframe, text="Item",font=("Arial" ,15, "bold"),bg="#289E55" )
        item_aviso.grid(row=1, column=0, sticky='w')

        in_item_aviso=Entry(miframe, width=20,font=12)
        in_item_aviso.grid(row=2, column=0, padx=15)

        cantidad_monstrar = Label(miframe, text="Cantidad",font=("Arial" ,15, "bold"),bg="#289E55" )
        cantidad_monstrar.grid(row=3, column=0, sticky='w')

        in_cantidad=Entry(miframe, width=20,font=12)
        in_cantidad.grid(row=4, column=0)

        precio_mostrar = Label(miframe, text="Precio ud",font=("Arial" ,15,"bold"),bg="#289E55")
        precio_mostrar.grid(row=5, column=0,sticky='w')

        in_item1 = Entry(miframe, width=20, font=12)
        in_item1.grid(row=6, column=0)

        #--------ITEM 2------
        
        item_aviso2 = Label(miframe, text="Item", font=("Arial" ,15, "bold"),bg="#289E55" )
        item_aviso2.grid(row=1, column=1, sticky='w')
        
        in_item_aviso2=Entry(miframe, width=20,font=12)
        in_item_aviso2.grid(row=2, column=1)
        
        cantidad_monstrar2 = Label(miframe, text="Cantidad", font=("Arial" ,15, "bold"),bg="#289E55")
        cantidad_monstrar2.grid(row=3, column=1, sticky='w')

        in_cantidad2=Entry(miframe, width=20,font=12)
        in_cantidad2.grid(row=4, column=1)

        precio_mostrar2 = Label(miframe, text="Precio Ud", font=("Arial" ,15, "bold"),bg="#289E55")
        precio_mostrar2.grid(row=5, column=1, sticky='w')

        in_item2 = Entry(miframe, width=20,font=12)
        in_item2.grid(row=6, column=1)

        Button(miframe, text="Registrar", command=registro_dato, font=("Arial" , 10, "bold")).grid(row=8, column=0, columnspan=2, pady=10)
        
        
        root_opcion2.mainloop()
   def windows_three_item():
      
        def registro_dato():
                a = f"{in_item_aviso.get().upper()},{in_item_aviso2.get().upper()},{in_item_aviso3.get().upper()}"
                b = f"{in_cantidad.get()},{in_cantidad2.get()}, {in_cantidad3.get()}"
                c = f"{in_item1.get()},{in_item2.get()}, {in_item3.get()}"
                r = (float(in_item1.get()) * float(in_cantidad.get())) + (float(in_item2.get())*float(in_cantidad2.get())) + (float(in_item3.get()) * float(in_cantidad3.get()))
                
                descrp = f"{in_cantidad.get()} {in_item_aviso.get().upper()} CON {in_cantidad2.get()} {in_item_aviso2.get().upper()} Y {in_cantidad3.get()} {in_item_aviso3.get().upper()}"
                g = "GRUPO 3"
                conexion = sqlite3.connect(ruta("DataBase"))
                pointer = conexion.cursor()
                pointer.execute("INSERT INTO ITEM_INDIVIDUALES (GRUPO,ITEM, CANTIDAD, PRECIO_UNIDAD, DESCRIPCION ,PRECIO_TOTAL) VALUES (?,?,?,?,?,?)",(g,a,b,c,descrp,r))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("BBDD","Registro exitoso")
                  
        def regresar(event):
                root_index.deiconify()
                root_opcion3.destroy()
        root_opcion3 = Toplevel(root_index)
        pos_x = (ancho_pantalla // 2) - (ancho_root // 2)
        pos_y = (alto_pantalla // 2) - (alto_root // 2)
        root_opcion3.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
        root_opcion3.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root_opcion3.config(bg="#289E55")
        root_opcion3.title("Decosol - Registro de Dato")
        root_opcion3.resizable(False, False)
        root_opcion3.iconbitmap(ruta("recursos/icono.ico"))

        
        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
                
        atras = Label(root_opcion3, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)
        atras.bind("<Button-1>", regresar)

        
        aviso = Label(root_opcion3, text="Registro de Dato",bg="#289E55")
        aviso.place(x=190, y=10)
        aviso.config(font=("Arial", 35))


        miframe = Frame(root_opcion3,bg="#289E55")
        miframe.place(x=150, y=100)

        #-------------ITEM 1-------------------
        item_aviso = Label(miframe, text="Item",font=("Arial" ,15, "bold"),bg="#289E55")
        item_aviso.grid(row=1, column=0, sticky='w', padx=10)

        in_item_aviso=Entry(miframe, width=15,font=12)
        in_item_aviso.grid(row=2, column=0)

        cantidad_monstrar = Label(miframe, text="Cantidad", font=("Arial" ,15, "bold"),bg="#289E55")
        cantidad_monstrar.grid(row=3, column=0, sticky='w')

        in_cantidad=Entry(miframe, width=15,font=12)
        in_cantidad.grid(row=4, column=0, padx=10)

        precio_mostrar = Label(miframe, text="Precio ud",font=("Arial" ,15, "bold"),bg="#289E55" )
        precio_mostrar.grid(row=5, column=0, sticky='w')

        in_item1 = Entry(miframe, width=15, font=12)
        in_item1.grid(row=6, column=0)

        #--------ITEM 2------
        item_aviso2 = Label(miframe, text="Item", font=("Arial" ,15, "bold"),bg="#289E55")
        item_aviso2.grid(row=1, column=1, sticky='w', padx=10)


        in_item_aviso2=Entry(miframe, width=15,font=12)
        in_item_aviso2.grid(row=2, column=1)
        
        cantidad_monstrar2 = Label(miframe, text="Cantidad",font=("Arial" ,15, "bold"),bg="#289E55")
        cantidad_monstrar2.grid(row=3, column=1, sticky='w')
        

        in_cantidad2=Entry(miframe, width=15,font=12)
        in_cantidad2.grid(row=4, column=1, padx=10)

        precio_mostrar2 = Label(miframe, text="Precio Ud",font=("Arial" ,15, "bold"),bg="#289E55")
        precio_mostrar2.grid(row=5, column=1, sticky='w')
        

        in_item2 = Entry(miframe, width=15,font=12)
        in_item2.grid(row=6, column=1)


        #----------------ITEM 3-------------------------------------

        item_aviso3 = Label(miframe, text="Item",font=("Arial" ,15,"bold"),bg="#289E55")
        item_aviso3.grid(row=1, column=2, sticky='w')
       

        in_item_aviso3=Entry(miframe, width=15,font=12)
        in_item_aviso3.grid(row=2, column=2)

        cantidad_monstrar3 = Label(miframe, text="Cantidad",font=("Arial" ,15,"bold"),bg="#289E55")
        cantidad_monstrar3.grid(row=3, column=2, sticky='w')
       
        in_cantidad3=Entry(miframe, width=15,font=12)
        in_cantidad3.grid(row=4, column=2, padx=10)
        
        precio_mostrar3 = Label(miframe, text="Precio",font=("Arial" ,15,"bold"),bg="#289E55")
        precio_mostrar3.grid(row=5, column=2, sticky='w')


        in_item3 = Entry(miframe, width=15,font=12)
        in_item3.grid(row=6, column=2)

        boton3 = Button(miframe, text="Registrar", command=registro_dato,font=("Arial" ,10, "bold"),width=25 )
        boton3.grid(row=7, column=0,columnspan=3, pady=10)
        root_opcion3.mainloop()
#ACOMODAR VENTANA DE CUATRO ITEMS ###################
   def windows_fourd_item():
       
        def registro_dato():
                a = f"{in_item_aviso.get().upper()},{in_item_aviso2.get().upper()},{in_item_aviso3.get().upper()}, {in_item_aviso4.get().upper()}"
                b = f"{in_cantidad.get()},{in_cantidad2.get()}, {in_cantidad3.get()}, {in_cantidad4.get()}"
                c = f"{in_item1.get()},{in_item2.get()}, {in_item3.get()}, {in_item4.get()}"
                r = (float(in_item1.get()) * float(in_cantidad.get())) + (float(in_item2.get())*float(in_cantidad2.get())) + (float(in_item3.get()) * float(in_cantidad3.get())) + (float(in_item4.get()) * float(in_cantidad4.get()))
                descrp = f"{in_cantidad.get()} {in_item_aviso.get().upper()} CON {in_cantidad2.get()} {in_item_aviso2.get().upper()} Y {in_cantidad3.get()} {in_item_aviso3.get().upper()} MAS {in_cantidad4.get()} {in_item_aviso4.get().upper()}"
                
                g = "GRUPO 4"
                conexion = sqlite3.connect(ruta("DataBase"))
                pointer = conexion.cursor()
                pointer.execute("INSERT INTO ITEM_INDIVIDUALES (GRUPO,ITEM, CANTIDAD, PRECIO_UNIDAD, DESCRIPCION ,PRECIO_TOTAL) VALUES (?,?,?,?,?,?)",(g,a,b,c,descrp,r))
                conexion.commit()
                conexion.close()
                messagebox.showinfo("BBDD","Registro exitoso")
        def atras_(evetn):
                root_index.deiconify()
                root_opcion4.destroy()
        root_opcion4 = Toplevel(root_index)
        pos_x = (ancho_pantalla // 2) - (ancho_root // 2)
        pos_y = (alto_pantalla // 2) - (alto_root // 2)
        root_opcion4.protocol("WM_DELETE_WINDOW",cerrar_rootIndex)
        root_opcion4.title("Decosol - Registro de Dato")
        root_opcion4.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
        root_opcion4.config(bg="#289E55")
        root_opcion4.resizable(False, False)
        root_opcion4.iconbitmap(ruta("recursos/icono.ico"))

        image_back = Image.open(ruta("imagenes/Back.png"))
        image_back=image_back.resize((50,50))
        back_img = ImageTk.PhotoImage(image_back)
                
        atras = Label(root_opcion4, image=back_img, bg="#289E55")
        atras.place(x=650, y=25)

        atras.bind("<Button-1>", atras_)

        aviso = Label(root_opcion4, text="Registro de Dato",bg="#289E55")
        aviso.place(x=150, y=5)
        aviso.config(font=("Arial", 35))

        
        miframe = Frame(root_opcion4,bg="#289E55")
        miframe.place(x=150, y=70)

        frame_row2 = Frame(root_opcion4,bg="#289E55")
        frame_row2.place(x=150, y=250)

        #-------------ITEM 1-------------------

        item_aviso = Label(miframe, text="Item", font=("Arial" ,15, "bold"),bg="#289E55")
        item_aviso.grid(row=1, column=0, sticky='w')

        in_item_aviso=Entry(miframe, width=20,font=12)
        in_item_aviso.grid(row=2, column=0,padx=10)  

        cantidad_monstrar = Label(miframe, text="Cantidad",font=("Arial" ,15, "bold"),bg="#289E55" )
        cantidad_monstrar.grid(row=3, column=0, sticky='w')

        in_cantidad=Entry(miframe, width=20,font=12)
        in_cantidad.grid(row=4, column=0,padx=10)

        precio_mostrar = Label(miframe, text="Precio ud",font=("Arial" ,15, "bold"),bg="#289E55")
        precio_mostrar.grid(row=5, column=0, sticky='w')

        in_item1 = Entry(miframe, width=20, font=12)
        in_item1.grid(row=6, column=0,padx=10)


        #--------ITEM 2------
        item_aviso2 = Label(miframe, text="Item", font=("Arial" ,15, "bold"),bg="#289E55" )
        item_aviso2.grid(row=1, column=1, sticky='w')
        
        in_item_aviso2=Entry(miframe, width=20,font=12)
        in_item_aviso2.grid(row=2, column=1)
        
        cantidad_monstrar2 = Label(miframe, text="Cantidad", font=("Arial" ,15, "bold"),bg="#289E55")
        cantidad_monstrar2.grid(row=3, column=1, sticky='w')

        in_cantidad2=Entry(miframe, width=20,font=12)
        in_cantidad2.grid(row=4, column=1)

        precio_mostrar2 = Label(miframe, text="Precio Ud", font=("Arial" ,15, "bold"),bg="#289E55")
        precio_mostrar2.grid(row=5, column=1, sticky='w')

        in_item2 = Entry(miframe, width=20,font=12)
        in_item2.grid(row=6, column=1)

                
        #----------------ITEM 3-------------------------------------
        item_aviso3 = Label(frame_row2, text="Item",font=("Arial" ,15,"bold"),bg="#289E55")
        item_aviso3.grid(row=0, column=0, sticky='w')
       

        in_item_aviso3=Entry(frame_row2, width=20,font=12)
        in_item_aviso3.grid(row=1, column=0,padx=10)

        cantidad_monstrar3 = Label(frame_row2, text="Cantidad",font=("Arial" ,15,"bold"),bg="#289E55")
        cantidad_monstrar3.grid(row=2, column=0, sticky='w')
       
        in_cantidad3=Entry(frame_row2, width=20,font=12)
        in_cantidad3.grid(row=3, column=0,padx=10)
        
        precio_mostrar3 = Label(frame_row2, text="Precio ud",font=("Arial" ,15,"bold"),bg="#289E55")
        precio_mostrar3.grid(row=4, column=0, sticky='w')


        in_item3 = Entry(frame_row2, width=20,font=12)
        in_item3.grid(row=5, column=0,padx=10)


        #-------------ITEM 4-------------
        item_aviso4 = Label(frame_row2, text="Item", font=("Arial" ,15, "bold"),bg="#289E55")
        item_aviso4.grid(row=0, column=1, sticky='w')
        
        in_item_aviso4=Entry(frame_row2, width=20,font=12)
        in_item_aviso4.grid(row=1, column=1)

        cantidad_monstrar4 = Label(frame_row2, text="Cantidad",font=("Arial" ,15,"bold"),bg="#289E55" )
        cantidad_monstrar4.grid(row=2, column=1,sticky='w')
       
        in_cantidad4=Entry(frame_row2, width=20,font=12)
        in_cantidad4.grid(row=3, column=1)

        precio_mostrar4 = Label(frame_row2, text="Precio ud",font=("Arial" ,15, "bold"),bg="#289E55")
        precio_mostrar4.grid(row=4, column=1, sticky='w')
        
        in_item4 = Entry(frame_row2, width=20,font=12)
        in_item4.grid(row=5, column=1)

        Button(frame_row2, text="Registrar", command=registro_dato,font=("Arial" ,10, "bold"), width=15).grid(row=7, column=0, columnspan=4 ,pady=10)
     


        root_opcion4.mainloop()
   def llamada_de_items():
        a = lista_des.get()
        if a == opciones[0]:                
                root_index.withdraw()
                opciones_root.destroy()
                windows_one_item()
        elif a == opciones[1]:
                root_index.withdraw()
                opciones_root.destroy()
                windows_two_item()
        elif a == opciones[2]:
                root_index.withdraw()
                opciones_root.destroy()
                windows_three_item()
        elif a == opciones[3]:
                root_index.withdraw()
                opciones_root.destroy()
                windows_fourd_item()

   opciones_root = Toplevel()
   pos_x = (ancho_pantalla // 2) - (ancho // 2)
   pos_y = (alto_pantalla // 2) - (alto // 2)
   opciones_root.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
   opciones_root.grab_set()
   opciones_root.config(bg="#289E55")
   opciones_root.title("OPCIONES")
   
 
   Label(opciones_root, text="Eliga cantidad de items: ", bg="#289E55", font=("Arial", 15, "bold")).pack()
   opciones = ["UN SOLO ITEM", "2 ITEMS", "3 ITEMS", "4 ITEMS"]

   seleccion = StringVar()
   lista_des = ttk.Combobox(opciones_root, values=opciones, textvariable=seleccion, state='readonly')
   lista_des.pack()
   lista_des.current(0)
   Button(opciones_root, text="Aceptar", command=llamada_de_items, font=("Arial", 12,"bold")).pack(pady=10)

def salir():
    cerrar = messagebox.askokcancel("SALIR" , "Desea salir") 
    if cerrar:
        root_index.destroy()

#VENTANA PRINCIPAL
root_index = Tk()

alto_pantalla = root_index.winfo_screenheight()
ancho_pantalla = root_index.winfo_screenwidth()
pos_x = (ancho_pantalla // 2 ) - (ancho_root // 2)
pos_y = (alto_pantalla // 2) - (alto_root // 2)

root_index.geometry(f"{ancho_root}x{alto_root}+{pos_x}+{pos_y}")
root_index.protocol("WM_DELETE_WINDOW", cerrar_rootIndex)
barra_de_menu = Menu(root_index)
root_index.config(bg="#289E55", menu=barra_de_menu)
root_index.title("Decosol")
root_index.resizable(False, False)

root_index.iconbitmap(ruta("recursos/icono.ico"))

nuevo_ancho, nuevo_alto = 250, 100
banner = Image.open(ruta("imagenes/baner.png"))
banner_resize = banner.resize((nuevo_ancho, nuevo_alto))
banner_see = ImageTk.PhotoImage(banner_resize)

frame_fecha = Frame(root_index, width=625, height=25,bg="black")
frame_fecha.place(x=45, y=450)

frame_hora = Frame(root_index,bg="#289E55")
frame_hora.place(x=600, y=450)

welcome= Label(root_index, image=banner_see,font=("Arial", 45), bg="#289E55")
welcome.place(x=250 , y=2)

frame_options = Frame(root_index, bg="#289E55")
frame_options.place(x=150, y=100)


#-------------OPTIONES---------------#

imagens  = Image.open(ruta("imagenes/img-consultor.png"))
nuevo_anchoa, nuevo_altoa = 100, 100
imagen_ridemen = imagens.resize((nuevo_anchoa, nuevo_altoa))
photoa = ImageTk.PhotoImage(imagen_ridemen)

label_consulta = Label(frame_options, text="Consultar Precio",font=("Arial", 12, "bold"), image=photoa, compound='top', bg="#289E55")
label_consulta.grid(row=0, column=0)
label_consulta.bind("<Button-1>",resaltar)
label_consulta.bind("<Double-Button-1>", consultor_de_precio)

imagen_calculador  = Image.open(ruta("imagenes/calculador_de precio.png"))
alto, ancho = 100,100
redimencion = imagen_calculador.resize((alto, ancho), Image.Resampling.LANCZOS)
photo_b = ImageTk.PhotoImage(redimencion)

label_calculador = Label(frame_options, text="  Registro de datos", font=("Aria", 12, "bold"), image=photo_b, compound='top', bg="#289E55")
label_calculador.grid(row=0, column=1)
label_calculador.bind("<Button-1>",resaltar)
label_calculador.bind("<Double-Button-1>", registrador_data)

imagen_ventas = Image.open(ruta("imagenes/Img-Venta2.png"))
redimencion_b = imagen_ventas.resize((alto, ancho), Image.Resampling.LANCZOS)
photo_c = ImageTk.PhotoImage(redimencion_b)

label_ventas = Label(frame_options, text="Ventas",font=("Arial", 12,"bold"), image=photo_c, compound='top', bg="#289E55")
label_ventas.grid(row=0, column=2)
label_ventas.bind("<Button-1>",resaltar)
label_ventas.bind("<Double-Button-1>",consulta_ventas)

imagen_clientes = Image.open(ruta("imagenes/img_Clientes.png"))
redimencion_cd = imagen_clientes.resize((alto, ancho), Image.Resampling.LANCZOS)
photo_cliente = ImageTk.PhotoImage(redimencion_cd)

label_clientes = Label(frame_options, text="Clientes", font=("Arial", 12, "bold"), image=photo_cliente, compound='top', bg="#289E55")
label_clientes.grid(row=1, column=0)

label_clientes.bind("<Button-1>",resaltar)
label_clientes.bind("<Double-Button-1>",clientes)

imagen_inventario = Image.open(ruta("imagenes/img-inventario.png"))
inventario_redimencion = imagen_inventario.resize((alto, ancho), Image.Resampling.LANCZOS)
photo_inventario = ImageTk.PhotoImage(inventario_redimencion)

label_inventario = Label(frame_options, text="Inventario", font=("Arial", 12, "bold"), image=photo_inventario, compound='top', bg="#289E55")
label_inventario.grid(row=1, column=1)
label_inventario.bind("<Button-1>",resaltar)
label_inventario.bind("<Double-Button-1>",stock)


#FECHA: 
dates = date.today()
meses =  [ 
        "Enero",    # 1
        "Febrero",  # 2
        "Marzo",    # 3
        "Abril",    # 4
        "Mayo",     # 5
        "Junio",    # 6
        "Julio",    # 7
        "Agosto",   # 8
        "Septiembre", # 9
        "Octubre",  # 10
        "Noviembre", # 11
        "Diciembre"  # 12
]
dias = [ 
        "Lunes",    # 0
        "Martes",   # 1
        "Miércoles", # 2
        "Jueves",   # 3
        "Viernes",  # 4
        "Sábado",   # 5
        "Domingo"   # 6
]

index_semana = dates.weekday()
index_mes = dates.month - 1
dia_index = dias[index_semana]
mes_español = meses[index_mes]

def mostrar_hora():
        hora = time.strftime("%H:%M:%S")
        root_index.after(1000, mostrar_hora)
        reloj.config(text=hora)
       

fecha = dates.strftime(f"{dia_index} {dates.day:2d} de {mes_español} del {dates.year}")

Label(frame_fecha, text=fecha, bg="#289E55", font="bold").grid(row=0, column=0)

Label(frame_hora, text="Hora: ",bg="#289E55", font="bold").grid(row=0, column=0)

reloj = Label(frame_hora, bg="#289E55", font="bold")
reloj.grid(row=0, column=1)
mostrar_hora()



root_index.mainloop()
