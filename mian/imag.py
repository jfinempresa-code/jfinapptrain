import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent

IMATGES = {
    "Resvio": "resvio.png",
    "Via X": "viax.png",
    "Convaes": "convaes.png",
    "Conva": "conva.png",
    "Lina": "lina.png",
}


def carregar_imatge(nom_fitxer, mida=(110, 70)):
    ruta = BASE_DIR / nom_fitxer

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
