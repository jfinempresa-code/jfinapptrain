
import tkinter as tk
from tkinter import ttk
from PIL import Image

# Dimensiones de la matriz
COLUMNAS = 1000
FILAS = 200

# Tamaño visual de cada botón, en píxeles
ANCHO_CELDA = 24
ALTO_CELDA = 24

COLOR_INACTIVO = "#E0E0E0"
COLOR_ACTIVO = "#32CD32"
COLOR_BORDE = "#A0A0A0"


class MatrizBotones:
    def __init__(self, root):
        self.root = root
        root.title("Matriz de 1000 x 200 botones")
        root.geometry("1000x650")

        # Solo guardamos las celdas activadas
        self.activados = set()

        barra = ttk.Frame(root, padding=5)
        barra.pack(fill="x")

        self.estado = ttk.Label(
            barra, text="Pulsa una celda para activarla"
        )
        self.estado.pack(side="left")

        ttk.Button(
            barra, text="Apagar todos",
            command=self.apagar_todos
        ).pack(side="right", padx=5)

        ttk.Button(
            barra, text="Activar todos",
            command=self.activar_todos
        ).pack(side="right", padx=5)

        # Zona de dibujo
        marco = ttk.Frame(root)
        marco.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            marco,
            background="white",
            highlightthickness=0
        )

        barra_x = ttk.Scrollbar(
            marco, orient="horizontal",
            command=self.desplazar_x
        )
        barra_y = ttk.Scrollbar(
            marco, orient="vertical",
            command=self.desplazar_y
        )

        self.canvas.configure(
            xscrollcommand=barra_x.set,
            yscrollcommand=barra_y.set,
            scrollregion=(
                0, 0,
                COLUMNAS * ANCHO_CELDA,
                FILAS * ALTO_CELDA
            )
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")
        barra_y.grid(row=0, column=1, sticky="ns")
        barra_x.grid(row=1, column=0, sticky="ew")

        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        # Eventos
        self.canvas.bind("<Button-1>", self.pulsar_celda)
        self.canvas.bind("<Configure>", self.redibujar)

        # Rueda del ratón
        self.canvas.bind("<MouseWheel>", self.rueda_vertical)

        # Linux: rueda del ratón
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-3, "units"))
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(3, "units"))

        self.root.after(100, self.redibujar)

    def limites_visibles(self):
        """Calcula las filas y columnas que se ven en pantalla."""
        x0 = self.canvas.canvasx(0)
        y0 = self.canvas.canvasy(0)
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()

        c0 = max(0, int(x0 // ANCHO_CELDA))
        f0 = max(0, int(y0 // ALTO_CELDA))
        c1 = min(COLUMNAS, int(x1 // ANCHO_CELDA) + 2)
        f1 = min(FILAS, int(y1 // ALTO_CELDA) + 2)

        return f0, f1, c0, c1

    def redibujar(self, evento=None):
        """Dibuja solamente las celdas visibles."""
        self.canvas.delete("celda")

        f0, f1, c0, c1 = self.limites_visibles()

        for fila in range(f0, f1):
            for columna in range(c0, c1):
                x0 = columna * ANCHO_CELDA
                y0 = fila * ALTO_CELDA
                x1 = x0 + ANCHO_CELDA
                y1 = y0 + ALTO_CELDA

                activo = (fila, columna) in self.activados
                color = COLOR_ACTIVO if activo else COLOR_INACTIVO

                self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=color,
                    outline=COLOR_BORDE,
                    tags="celda"
                )

    def pulsar_celda(self, evento):
        x = self.canvas.canvasx(evento.x)
        y = self.canvas.canvasy(evento.y)

        columna = int(x // ANCHO_CELDA)
        fila = int(y // ALTO_CELDA)

        if not (0 <= columna < COLUMNAS and 0 <= fila < FILAS):
            return

        celda = (fila, columna)

        if celda in self.activados:
            self.activados.remove(celda)
            accion = "desactivada"
        else:
            self.activados.add(celda)
            accion = "activada"

        self.estado.config(
            text=f"Fila: {fila + 1} | Columna: {columna + 1}"
                 f" | Celda {accion} | "
                 f"Activas: {len(self.activados):,}"
        )

        self.redibujar()

    def desplazar_x(self, *args):
        self.canvas.xview(*args)
        self.redibujar()

    def desplazar_y(self, *args):
        self.canvas.yview(*args)
        self.redibujar()

    def rueda_vertical(self, evento):
        self.canvas.yview_scroll(
            -1 if evento.delta > 0 else 1, "units"
        )
        self.redibujar()

    def apagar_todos(self):
        self.activados.clear()
        self.estado.config(text="Todas las celdas están apagadas")
        self.redibujar()

    def activar_todos(self):
        self.activados = {
            (fila, columna)
            for fila in range(FILAS)
            for columna in range(COLUMNAS)
        }
        self.estado.config(text="Las 200.000 celdas están activadas")
        self.redibujar()
# Panel de imágenes
panel_imagenes = ttk.Frame(root, padding=5)
panel_imagenes.pack(fill="x")

self.imagenes_tk = []

for nombre, imagen in [
    ("res", res),
    ("x", x),
    ("cones", cones),
    ("conva", conva),
]:
    imagen_copia = imagen.copy()
    imagen_copia.thumbnail((100, 100))

    imagen_tk = ImageTk.PhotoImage(imagen_copia)
    self.imagenes_tk.append(imagen_tk)

    bloque = ttk.Frame(panel_imagenes)
    bloque.pack(side="left", padx=8)

    ttk.Label(bloque, text=nombre).pack()
    ttk.Label(bloque, image=imagen_tk).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrizBotones(root)
    root.mainloop()