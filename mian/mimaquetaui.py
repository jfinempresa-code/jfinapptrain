
import tkinter as tk
import imag


def obrir_maqueta(parent, ruta="/", nom="Maqueta"):
    finestra = tk.Toplevel(parent)
    finestra.title(f"{nom} - {ruta}")
    finestra.geometry("900x650")

    files = 20
    columnes = 10

    capcalera = tk.Frame(finestra)
    capcalera.pack(fill="x", padx=10, pady=8)

    tk.Label(
        capcalera,
        text=f"Maqueta: {nom} | Ruta: {ruta}",
        font=("Arial", 12, "bold")
    ).pack(side="left")

    tk.Button(
        capcalera,
        text="Obrir imatges",
        command=lambda: imag.obrir_imatges(finestra, titol="Imatges generals")
    ).pack(side="right")

    contenidor = tk.Frame(finestra)
    contenidor.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(contenidor, highlightthickness=0)
    barra_vertical = tk.Scrollbar(
        contenidor, orient="vertical", command=canvas.yview
    )
    barra_horitzontal = tk.Scrollbar(
        contenidor, orient="horizontal", command=canvas.xview
    )

    canvas.configure(
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horitzontal.set
    )

    barra_vertical.grid(row=0, column=1, sticky="ns")
    barra_horitzontal.grid(row=1, column=0, sticky="ew")
    canvas.grid(row=0, column=0, sticky="nsew")

    contenidor.grid_rowconfigure(0, weight=1)
    contenidor.grid_columnconfigure(0, weight=1)

    marc = tk.Frame(canvas)
    finestra_canvas = canvas.create_window(
        (0, 0), window=marc, anchor="nw"
    )

    def actualitzar_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    marc.bind("<Configure>", actualitzar_scroll)

    def obrir_boto(fila, columna):
        imag.obrir_imatges(
            finestra,
            titol=f"Imatges - Fila {fila}, columna {columna}"
        )

    for fila in range(files):
        for columna in range(columnes):
            boto = tk.Button(
                marc,
                text=f"{fila},{columna}",
                width=8,
                height=2,
                command=lambda f=fila, c=columna: obrir_boto(f, c)
            )
            boto.grid(
                row=fila,
                column=columna,
                padx=2,
                pady=2,
                sticky="nsew"
            )

    return finestra

