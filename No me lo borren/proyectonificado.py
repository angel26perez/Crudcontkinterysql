# Proyecto unificado 1 
#CRUD con tkinter + sqlite

#Declaramos Variables y librerias

from tkinter import * 
from tkinter import messagebox 
from tkinter import ttk 
import sqlite3 
from pathlib import Path 

#ruta del proyecto 

BASE_DIR =  Path (__file__).resolve().parent 

#Base de datos en la misma carpeta

RUTA_BBDD = BASE_DIR / "BaseMAPG.db"

# icono en la misma carpet ade programa 

RUTA_ICONO = BASE_DIR  / "Escudo_Junior.ico"

# Ventana principal 

raiz = Tk()
raiz.title("Proyecto Unificado 1 - CRUD")

#tamaño de la ventana
ancho = 1100
alto = 650

#icono de la ventana 
if RUTA_ICONO.exists():

    try:
        raiz.iconbitmap(str(RUTA_ICONO))

    except Exception as e :
        print(F"no se pudo cargar el icono {e}")
else : 
    print("NO SE ENCONTRO EL ICONO ")
    print(RUTA_ICONO)


#variables tkinter

miId = StringVar()
miNombre = StringVar()
miPass = StringVar()
miApellido = StringVar()
miDireccion = StringVar()

# ===================================================
# FUNCIONES BDD Y CONEXION
# ===================================================

def conexionBBDD():

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TBL_USUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDO VARCHAR(50),
            DIRECCION VARCHAR(100),
            COMENTARIOS VARCHAR(255)
        )
    """)

    conexion.commit()
    conexion.close()

# ===================================================
# VALIDAR CAMPOS
# ===================================================

def validarCampos():

    if miNombre.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese el nombre"
        )
        return False

    if miPass.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese la contraseña"
        )
        return False

    if miApellido.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese el apellido"
        )
        return False

    if miDireccion.get().strip()== "":
        messagebox.showwarning(
            "validacion",
            "Ingrese la direccion"
        )


# ===================================================
# VALIDAR ID
# ===================================================

def validarID():

    if miId.get().strip() == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese un ID"
        )
        return False

    if not miId.get().isdigit():
        messagebox.showwarning(
            "Validación",
            "El ID debe ser numérico"
        )
        return False

    return True

# ===================================================
# LIMPIAR CAMPOS
# ===================================================

def limpiarCampos():

    miId.set("")
    miNombre.set("")
    miPass.set("")
    miApellido.set("")
    miDireccion.set("")

    textComentario.delete(
        "1.0",
        END
    )


# ===================================================
# CARGAR DATOS EN LA TABLA
# ===================================================

def cargarDatos():

    # Limpiar la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            ID,
            NOMBRE_USUARIO,
            PASSWORD,
            APELLIDO,
            DIRECCION,
            COMENTARIOS
        FROM TBL_USUARIOS
        ORDER BY ID
        """
    )

    registros = cursor.fetchall()

    for registro in registros:

        tabla.insert(
            "",
            END,
            values = registro 
        )
    conexion.close()

# ===================================================
# CREAR REGISTRO
# ===================================================

def crear():

    if not validarCampos():
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO TBL_USUARIOS
        (
            NOMBRE_USUARIO,
            PASSWORD,
            APELLIDO,
            DIRECCION,
            COMENTARIOS
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        miNombre.get().strip(),
        miPass.get().strip(),
        miApellido.get().strip(),
        miDireccion.get().strip(),
        textComentario.get("1.0", END).strip()
    ))

    conexion.commit()
    conexion.close()

    messagebox.showinfo(
        "BBDD",
        "Registro guardado correctamente"
    )

    limpiarCampos()
    cargarDatos()

#====================================================
#LEER O CONSULTAR REGISTRO
#====================================================

def leer():

    if not validarID():
        return
    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT * 
        FROM TBL_USUSARIOS 
        WHERE ID = ? 
        """,
        (miId.get(),)       
    )

    usuario = cursor.fetchone()

    conexion.close()

    if usuario:
        miNombre.set(usuario[1])
        miPass.set(usuario[2])
        miApellido.set(usuario[3])
        miDireccion.set(usuario[4])

        textComentario.delete (
            "1.0",
            END
        )

    else:
        messagebox.showwarning(
            "consulta",
            "no existe un registro con ese ID"
        )


# ===================================================
# ACTUALIZAR REGISTRO
# ===================================================

def actualizar():

    if not validarID():
        return

    if not validarCampos():
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE TBL_USUARIOS
        SET
            NOMBRE_USUARIO = ?,
            PASSWORD = ?,
            APELLIDO = ?,
            DIRECCION = ?,
            COMENTARIOS = ?
        WHERE ID = ?
    """, (
        miNombre.get().strip(),
        miPass.get().strip(),
        miApellido.get().strip(),
        miDireccion.get().strip(),
        textComentario.get("1.0", END).strip(),
        miId.get()
    ))

    conexion.commit()

    registros_actualizados = cursor.rowcount

    conexion.close()

    if registros_actualizados > 0:
        messagebox.showinfo(
            "Actualizar",
            "Registro actualizado correctamente"
        )
    else:
        messagebox.showwarning(
            "Actualizar",
            "No existe el ID"
        )

    cargarDatos()
    limpiarCampos()

# ===================================================
# ELIMINAR REGISTRO
# ===================================================

def eliminar():

    if not validarID():
        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Desea eliminar este registro?"
    )

    if not respuesta:
        return

    conexion = sqlite3.connect(str(RUTA_BBDD))
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM TBL_USUARIOS
        WHERE ID = ?
        """,
        (miId.get(),)
    )

    conexion.commit()

    registros_eliminados = cursor.rowcount

    conexion.close()

    if registros_eliminados > 0:
        messagebox.showinfo(
            "Eliminar",
            "Registro eliminado correctamente"
        )
    else:
        messagebox.showwarning(
            "Eliminar",
            "No existe el ID"
        )

    cargarDatos()
    limpiarCampos()

# ===================================================
# SELECCIONAR REGISTRO DE LA TABLA
# ===================================================

def seleccionarRegistro(event):

    item = tabla.focus()

    if item == "":
        return

    datos = tabla.item(item)["values"]

    if not datos:
        return

    miId.set(datos[0])
    miNombre.set(datos[1])
    miPass.set(datos[2])
    miApellido.set(datos[3])
    miDireccion.set(datos[4])

    textComentario.delete(
        "1.0",
        END
    )

    textComentario.insert(
        "1.0",
        datos[5]
    )


# ===================================================
# SALIR DE LA APLICACION
# ===================================================

def salirAplicacion():

    valor = messagebox.askyesno(
        "Salir",
        "¿Desea salir de la aplicación?"
    )

    if valor:
        raiz.destroy()


# ===================================================
# MENU
# ===================================================
barraMenu = Menu(raiz)

raiz.config(menu=barraMenu)

menuBBDD = Menu(
    barraMenu,
    tearoff=0
)

menuBBDD.add_command(
    label="Conectar",
    command=conexionBBDD
)

menuBBDD.add_separator()

menuBBDD.add_command(
    label="salir",
    command=salirAplicacion
)

barraMenu.add_cascade(
    label="BBDD",
    menu = menuBBDD
)

#====================================================
#Menu ayuda
#====================================================

menuAyuda =Menu(
    barraMenu,
    tearoff=0
)

menuAyuda.add_command(
    label= "acerca de",
    command=lambda : messagebox.showinfo(
        "acerca de",
        "proyecto unificado 1\n"
        "CRUD co Tkinter y SQLite \n"
        "Desarrollo en Python \n"
        "CREADO POR: Miguel Angel Perez"
    )
)

barraMenu.add_cascade(
    label="ayuda",
    menu=menuAyuda
)

#====================================================
#Crear Base de Datos
#====================================================

conexionBBDD()

#====================================================
#CENTRAR VENTANA EN LA PANTALLA
#====================================================
ancho_pantalla = raiz.winfo_screenwidth()
alto_pantalla = raiz.winfo_screenheight()

posicion_x = int(
    (ancho_pantalla - ancho) / 2
)

posicion_y = int(
    (alto_pantalla - alto) / 2
)

#raiz.geometry(
   # f"{ancho} x {alto} + {posicion_x} + {posicion_y}"
#)
#====================================================
#FRAME DE DATOS
#====================================================

miFrame = Frame (
    raiz
)

miFrame.pack(
    padx=10
)

#====================================================
#ID
#====================================================

Label(
    miFrame,
    text="ID"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

Entry(
    miFrame,
    textvariable=miId,
    width=30
).grid(
    row=0,
    column=1
)

#====================================================
#NOMBRE
#====================================================

Label(
    miFrame,
    text="Nombre"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miNombre,
    width=30
).grid(
    row=0,
    column=1
)

#====================================================
#Password
#====================================================

Label(
    miFrame,
    text="Password"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miPass,
    show="#",
    width=30
).grid(
    row=2,
    column=1
)
#====================================================
#Password
#====================================================

Label(
    miFrame,
    text="Password"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)
Entry(
    miFrame,
    textvariable=miPass,
    show="#",
    width=30
).grid(
    row=2,
    column=1
)

# ===================================================
# APELLIDO
# ===================================================

Label(
    miFrame,
    text="Apellido"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5
)

Entry(
    miFrame,
    textvariable=miApellido,
    width=30
).grid(
    row=3,
    column=1
)


# ===================================================
# COMENTARIOS
# ===================================================

Label(
    miFrame,
    text="Comentarios"
).grid(
    row=5,
    column=0,
    padx=5,
    pady=5
)

textComentario = Text(
    miFrame,
    width=30,
    height=5
)

textComentario.grid(
    row=5,
    column=1
)

# ===================================================
# SCROLL DE COMENTARIOS
# ===================================================

scroll = Scrollbar(
    miFrame,
    command=textComentario.yview
)

scroll.grid(
    row=5,
    column=2,
    sticky="nsew"
)

textComentario.config(
    yscrollcommand=scroll.set
)


# ===================================================
# FRAME BOTONES
# ===================================================

frameBotones = Frame(
    raiz
)

frameBotones.pack(
    pady=10
)


# ===================================================
# BOTON CREAR
# ===================================================

Button(
    frameBotones,
    text="Crear",
    width=15,
    command=crear
).grid(
    row=0,
    column=0,
    padx=5
)

# ===================================================
# FRAME TABLA
# ===================================================

frameTabla = Frame(
    raiz
)

frameTabla.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ===================================================
# TABLA TREEVIEW
# ===================================================

tabla = ttk.Treeview(
    frameTabla,
    columns=(
        "ID",
        "NOMBRE",
        "PASSWORD",
        "APELLIDO",
        "DIRECCION",
        "COMENTARIOS"
    ),
    show="headings"
)

# ===================================================
# ENCABEZADOS
# ===================================================

tabla.heading(
    "ID",
    text="ID"
)

tabla.heading(
    "NOMBRE",
    text="Nombre"
)

tabla.heading(
    "PASSWORD",
    text="Password"
)

tabla.heading(
    "APELLIDO",
    text="Apellido"
)

tabla.heading(
    "DIRECCION",
    text="Dirección"
)

tabla.heading(
    "COMENTARIOS",
    text="Comentarios"
)

# ===================================================
# ANCHO DE COLUMNAS
# ===================================================

tabla.column(
    "ID",
    width=50,
    anchor="center"
)

tabla.column(
    "NOMBRE",
    width=150
)

tabla.column(
    "PASSWORD",
    width=120
)

tabla.column(
    "APELLIDO",
    width=150
)

tabla.column(
    "DIRECCION",
    width=200
)

tabla.column(
    "COMENTARIOS",
    width=300
)

# ===================================================
# SCROLL VERTICAL DE LA TABLA
# ===================================================

scrollTabla = Scrollbar(
    frameTabla,
    orient=VERTICAL,
    command=tabla.yview
)

tabla.configure(
    yscrollcommand=scrollTabla.set
)


# ===================================================
# MOSTRAR TABLA
# ===================================================

tabla.pack(
    side=LEFT,
    fill="both",
    expand=True
)

scrollTabla.pack(
    side=RIGHT,
    fill="y"
)


# ===================================================
# EVENTO SELECCIONAR REGISTRO
# ===================================================

tabla.bind(
    "<<TreeviewSelect>>",
    seleccionarRegistro
)


# ===================================================
# CARGAR REGISTROS EXISTENTES
# ===================================================

cargarDatos()

# ===================================================
# CERRAR CON LA X DE LA VENTANA
# ===================================================

raiz.protocol(
    "WM_DELETE_WINDOW",
    salirAplicacion
)

#====================================================
#EJECTAR APP
#====================================================

raiz.mainloop()