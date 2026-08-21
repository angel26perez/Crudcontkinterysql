from tkinter import *

raiz = Tk()
raiz.title("LAS PAMPARAS") 
raiz.resizable(True, True)

icono = PhotoImage(file="Escudo_Junior.png") 
raiz.iconphoto(False, icono)
raiz.geometry("650x450")

# 1. Creamos una LISTA de imágenes
imagenes = [
    PhotoImage(file="migueanimado.png"),
    PhotoImage(file="images.png"),
    PhotoImage(file="dieguito.png"),  # <-- Agrega aquí las fotos que quieras
    PhotoImage(file="papaletas.png")]

# 2. Creamos una LISTA de textos que coincidan con las fotos
textos = [
    "Angeeeel",
    "¡Marquitoooo!",
    "Diegoooouououo",
    "PAPALETAAAA"
]

# Variable contador para saber en qué posición vamos (empieza en 0)
indice = 0

# Texto e Imagen Iniciales (usan la posición 0 de las listas)
etiqueta = Label(raiz, text=textos[indice], font=("Arial", 12), bg="#f0f0f0")
etiqueta.pack(pady=10) 

lbl_imagen = Label(raiz, image=imagenes[indice])
lbl_imagen.pack(pady=10)


def siguiente_persona():
    global indice
    
    # TRUCO: Le sumamos 1 al índice.
    # El % len(imagenes) hace que al llegar al final vuelva automáticamente al inicio (0)
    indice = (indice + 1) % len(imagenes)
    
    # Actualizamos el texto y la imagen con la nueva posición
    etiqueta.config(text=textos[indice])
    lbl_imagen.config(image=imagenes[indice])
    lbl_imagen.image = imagenes[indice]


# BOTÓN
boton = Button(
    raiz, 
    text="Siguiente Persona ➡️", 
    command=siguiente_persona,
    font=("Arial", 11), 
    bg="#227751",
    fg="white"
)
boton.pack(pady=15)

raiz.mainloop()