import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent

IMATGES = {
    "Via en Corba a l'Esquerra": "resvio.png",
    "Via de Creuement en X": "viax.png",
    "Via amb Desviament a l'Esquerra": "convaes.png",
    "Via amb Desviament a la Dreta": "conva.png",
    "Via en Línia Recta ": "lina.png",
}


def carregar_imatge(nom_fitxer, mida=(110, 70)):
    ruta = BASE_DIR / "images" / nom_fitxer

    with Image.open(ruta) as original:
        imatge = original.convert("RGBA")
        imatge.thumbnail(mida, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imatge)


def obrir_imatges(parent, titol="Seleccionar imatge"):
    finestra = tk.Toplevel(parent)
    finestra.title(titol)
    finestra.geometry("650x350")

    finestra.fotos = []

    for index, (nom, fitxer) in enumerate(IMATGES.items()):
        marc = tk.Frame(finestra, padx=8, pady=8)
        marc.grid(row=index // 3, column=index % 3)

        try:
            foto = carregar_imatge(fitxer, (150, 100))
            finestra.fotos.append(foto)

            tk.Label(marc, image=foto).pack()
            tk.Label(marc, text=nom).pack()

        except (OSError, ValueError) as error:
            tk.Label(marc, text=str(error), fg="red").pack()

    return finestra

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from pathlib import Path

# Carpeta on es troba aquest fitxer
CARPETA = Path(__file__).resolve().parent
FITXER_JSON = CARPETA / "seleccion.json"

# Opcions de selecció
IMATGES = {
    "resvio": "resvio.png",
    "viax": "viax.png",
    "conva": "conva.png",
    "conra": "conra.png",
    "lina": "lina.png",
}


def guardar_seleccio(opcio):
    """Guarda l'opció seleccionada en format JSON."""
    dades = {
        "seleccio": opcio,
        "imatge": IMATGES[opcio]
    }

    try:
        with open(FITXER_JSON, "w", encoding="utf-8") as fitxer:
            json.dump(dades, fitxer, indent=4, ensure_ascii=False)

        messagebox.showinfo(
            "Selecció guardada",
            f"Has seleccionat: {opcio}\n\n"
            f"Guardat a: {FITXER_JSON.name}"
        )
    except OSError as error:
        messagebox.showerror("Error", str(error))


def crear_finestra(parent=None):
    """Crea la finestra de selecció d'imatges."""
    finestra = tk.Toplevel(parent) if parent else tk.Tk()
    finestra.title("Selecciona una opció")
    finestra.geometry("500x400")

    tk.Label(
        finestra,
        text="Selecciona una opció",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    marc = tk.Frame(finestra)
    marc.pack(expand=True)

    # Conservem les referències de les imatges
    finestra.imatges = []

    for index, (nom, fitxer) in enumerate(IMATGES.items()):
        ruta = CARPETA / fitxer

        try:
            imatge = Image.open(ruta)
            imatge.thumbnail((100, 100))
            foto = ImageTk.PhotoImage(imatge)
            finestra.imatges.append(foto)

            boto = tk.Button(
                marc,
                text=nom,
                image=foto,
                compound="top",
                width=110,
                command=lambda opcio=nom: guardar_seleccio(opcio)
            )

        except (OSError, tk.TclError):
            # Si falta la imatge, encara es pot seleccionar pel nom
            boto = tk.Button(
                marc,
                text=nom,
                width=12,
                height=4,
                command=lambda opcio=nom: guardar_seleccio(opcio)
            )

        boto.grid(
            row=index // 3,
            column=index % 3,
            padx=8,
            pady=8
        )

    return finestra


if __name__ == "__main__":
    finestra = crear_finestra()
    finestra.mainloop()
