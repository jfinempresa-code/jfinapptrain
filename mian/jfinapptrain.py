import json
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

import mimaquetaui
BASE_DIR = Path(__file__).resolve().parent
directori = BASE_DIR /".."/"jfinapptrain"
directori.mkdir(parents=True, exist_ok=True)

FITXER = BASE_DIR/".." /"jfinapptrain"/ "maqueta.json"


def llegir_json():
    try:
        with FITXER.open("r", encoding="utf-8") as f:
            dades = json.load(f)

        if not isinstance(dades, dict) or not isinstance(
            dades.get("routes", []), list
        ):
            raise ValueError("El JSON ha de contenir una llista 'routes'.")

        llista.delete(0, tk.END)

        for item in dades.get("routes", []):
            llista.insert(
                tk.END,
                f"{item.get('key', '')} | "
                f"{item.get('route', '')} | "
                f"{item.get('button', '')} | "
                f"{item.get('imatge', '')}"
            )

        messagebox.showinfo("JSON", "JSON llegit correctament.")

    except FileNotFoundError:
        llista.delete(0, tk.END)
        messagebox.showwarning(
            "JSON", "Encara no existeix maqueta.json."
        )
    except (json.JSONDecodeError, OSError, ValueError) as e:
        messagebox.showerror("Error", str(e))


def escriure_json():
    key = entry_key.get().strip()
    route = entry_route.get().strip()
    button = entry_button.get().strip()
    imatge = entry_imatge.get().strip()

    if not key or not route or not button:
        messagebox.showwarning("Atenció", "Omple tots els camps.")
        return

    if not route.startswith("/") or route.startswith("//"):
        messagebox.showwarning(
            "Atenció", "La ruta ha de començar amb una sola /."
        )
        return

    try:
        if FITXER.exists():
            with FITXER.open("r", encoding="utf-8") as f:
                dades = json.load(f)
        else:
            dades = {"routes": []}

        if not isinstance(dades, dict):
            raise ValueError("El contingut del JSON no és vàlid.")

        routes = dades.setdefault("routes", [])

        if not isinstance(routes, list):
            raise ValueError("'routes' ha de ser una llista.")

        nova_ruta = {
            "key": key,
            "route": route,
            "button": button,
            "imatge": imatge
        }

        existent = next(
            (
                r for r in routes
                if isinstance(r, dict) and r.get("key") == key
            ),
            None
        )

        if existent:
            existent.update(nova_ruta)
        else:
            routes.append(nova_ruta)

        with FITXER.open("w", encoding="utf-8") as f:
            json.dump(dades, f, ensure_ascii=False, indent=4)

        directori = BASE_DIR /".."/"jfinapptrain"/ route.lstrip("/")
        directori.mkdir(parents=True, exist_ok=True)

        llegir_json_sense_missatge()
        messagebox.showinfo(
            "JSON",
            f"Dades desades correctament.\nDirectori: {directori}"
        )

    except (json.JSONDecodeError, OSError, ValueError) as e:
        messagebox.showerror("Error", str(e))


def llegir_json_sense_missatge():
    """Actualitza la llista sense mostrar un avís."""
    llista.delete(0, tk.END)

    if not FITXER.exists():
        return

    with FITXER.open("r", encoding="utf-8") as f:
        dades = json.load(f)

    for item in dades.get("routes", []):
        llista.insert(
            tk.END,
            f"{item.get('key', '')} | "
            f"{item.get('route', '')} | "
            f"{item.get('button', '')} | "
            f"{item.get('imatge', '')}"
        )


def seleccionar(event=None):
    seleccio = llista.curselection()
    if not seleccio:
        return

    text = llista.get(seleccio[0])
    parts = text.split(" | ")

    if len(parts) >= 3:
        entry_key.delete(0, tk.END)
        entry_key.insert(0, parts[0])

        entry_route.delete(0, tk.END)
        entry_route.insert(0, parts[1])

        entry_button.delete(0, tk.END)
        entry_button.insert(0, parts[2])

        if len(parts) >= 4:
            entry_imatge.delete(0, tk.END)
            entry_imatge.insert(0, parts[3])


def obrir_detalls(event=None):
    route = entry_route.get().strip()

    if not route:
        messagebox.showwarning(
            "Atenció", "Selecciona una ruta primer."
        )
        return

    mimaquetaui.obrir_maqueta(
        root,
        ruta=route,
        nom=entry_key.get().strip() or "Maqueta"
    )


root = tk.Tk()
root.title("Mi maqueta tren")
root.geometry("850x720")

tk.Label(root, text="Nom / clau").pack(anchor="w", padx=15)
entry_key = tk.Entry(root)
entry_key.pack(fill="x", padx=15, pady=(0, 8))

tk.Label(root, text="Ruta").pack(anchor="w", padx=15)
entry_route = tk.Entry(root)
entry_route.pack(fill="x", padx=15, pady=(0, 8))

tk.Label(root, text="Text del botó").pack(anchor="w", padx=15)
entry_button = tk.Entry(root)
entry_button.pack(fill="x", padx=15, pady=(0, 8))

tk.Label(root, text="Imatge associada").pack(anchor="w", padx=15)
entry_imatge = tk.Entry(root)
entry_imatge.pack(fill="x", padx=15, pady=(0, 8))

fila_botons = tk.Frame(root)
fila_botons.pack(pady=5)

tk.Button(
    fila_botons,
    text="Llegir JSON",
    command=llegir_json
).pack(side="left", padx=5)

tk.Button(
    fila_botons,
    text="Desar / Actualitzar JSON",
    command=escriure_json
).pack(side="left", padx=5)

tk.Button(
    fila_botons,
    text="Obrir maqueta",
    command=obrir_detalls
).pack(side="left", padx=5)

tk.Label(root, text="Rutes guardades").pack(pady=(10, 0))

llista = tk.Listbox(root, height=10)
llista.pack(fill="both", expand=True, padx=15, pady=8)
llista.bind("<<ListboxSelect>>", seleccionar)
llista.bind("<Double-Button-1>", obrir_detalls)

if FITXER.exists():
    try:
        llegir_json_sense_missatge()
    except (json.JSONDecodeError, OSError, ValueError) as e:
        messagebox.showerror("Error en carregar el JSON", str(e))

root.mainloop()
