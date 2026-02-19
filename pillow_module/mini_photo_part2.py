import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageOps

class MiniPhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photo Editor")
        self.root.geometry("980x640")
        self.root.configure(bg="white")

        # === State ===
        self.original_img = None   # as loaded
        self.base_img = None       # after discrete edits (rotate/crop/filters)
        self.tk_img = None         # ImageTk reference (avoid GC)
        self.history = []          # undo stack of base_img
        self.max_history = 12

        # View/adjustments
        self.zoom = 1.0
        self.min_zoom, self.max_zoom = 0.2, 6.0
        self.canvas_w, self.canvas_h = 680, 520
        self.img_item = None
        self.drag_start = None

        # Live sliders (non-destructive)
        self.var_bright = tk.DoubleVar(value=1.0)
        self.var_contrast = tk.DoubleVar(value=1.0)
        self.var_sat = tk.DoubleVar(value=1.0)
        self.var_tint_strength = tk.DoubleVar(value=0.0)  # 0..1
        self.tint_color = (255, 0, 0)  # default red

        # === UI ===
        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        # Title
        title = tk.Label(self.root, text="Mini Photo Editor",
                         font=("Arial", 18, "bold"), bg="white", fg="#1f4aff")
        title.pack(pady=6)

        # Main frame
        main = tk.Frame(self.root, bg="white")
        main.pack(fill="both", expand=True, padx=10, pady=6)

        # Canvas (image area)
        canvas_frame = tk.Frame(main, bg="#f4f6fa", bd=1, relief="solid")
        canvas_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_w, height=self.canvas_h,
                                bg="#e9eef7", highlightthickness=0)
        self.canvas.pack(padx=6, pady=6)

        # Mouse bindings for pan + zoom
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_move)
        # Windows/Mac
        self.canvas.bind("<MouseWheel>", self.on_wheel_zoom)
        # Linux
        self.canvas.bind("<Button-4>", lambda e: self.adjust_zoom(1.1))
        self.canvas.bind("<Button-5>", lambda e: self.adjust_zoom(1/1.1))

        # Controls panel
        right = tk.Frame(main, bg="white")
        right.grid(row=0, column=1, sticky="ns")

        # Row 1: file ops
        row1 = tk.Frame(right, bg="white")
        row1.pack(fill="x", pady=2)
        tk.Button(row1, text="Open", width=10, command=self.open_image, bg="#87CEFA").pack(side="left", padx=2)
        tk.Button(row1, text="Save", width=10, command=self.save_image, bg="#20B2AA", fg="white").pack(side="left", padx=2)
        tk.Button(row1, text="Reset", width=10, command=self.reset_to_original, bg="#ffcdd2").pack(side="left", padx=2)
        tk.Button(row1, text="Undo", width=10, command=self.undo, bg="#ffe0b2").pack(side="left", padx=2)

        # Row 2: transforms
        row2 = tk.Frame(right, bg="white")
        row2.pack(fill="x", pady=6)
        tk.Button(row2, text="Rotate 90°", width=12, command=self.rotate).pack(side="left", padx=2)
        tk.Button(row2, text="Flip H", width=10, command=lambda: self.apply_discrete(self.base_img.transpose(Image.FLIP_LEFT_RIGHT))).pack(side="left", padx=2)
        tk.Button(row2, text="Flip V", width=10, command=lambda: self.apply_discrete(self.base_img.transpose(Image.FLIP_TOP_BOTTOM))).pack(side="left", padx=2)

        # Row 3: crop + zoom
        row3 = tk.Frame(right, bg="white")
        row3.pack(fill="x", pady=6)
        tk.Button(row3, text="Crop WxH", width=12, command=self.crop_dialog).pack(side="left", padx=2)
        tk.Button(row3, text="Zoom +", width=10, command=lambda: self.adjust_zoom(1.2)).pack(side="left", padx=2)
        tk.Button(row3, text="Zoom −", width=10, command=lambda: self.adjust_zoom(1/1.2)).pack(side="left", padx=2)
        tk.Button(row3, text="Fit View", width=10, command=self.fit_to_view).pack(side="left", padx=2)

        # Row 4: quick filters (discrete)
        row4 = tk.Frame(right, bg="white")
        row4.pack(fill="x", pady=6)
        tk.Button(row4, text="B&W", width=10, command=lambda: self.filter_bw()).pack(side="left", padx=2)
        tk.Button(row4, text="Sepia", width=10, command=lambda: self.filter_sepia()).pack(side="left", padx=2)
        tk.Button(row4, text="Invert", width=10, command=lambda: self.filter_invert()).pack(side="left", padx=2)
        tk.Button(row4, text="AutoContrast", width=12, command=lambda: self.filter_autocontrast()).pack(side="left", padx=2)

        # Sliders header
        tk.Label(right, text="Live Adjustments", bg="white", fg="#333", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10,2))

        # Row 5: brightness slider
        self.make_slider(right, "Brightness", self.var_bright, 0.2, 2.5, 1.0)
        # Row 6: contrast
        self.make_slider(right, "Contrast", self.var_contrast, 0.2, 2.5, 1.0)
        # Row 7: saturation
        self.make_slider(right, "Saturation", self.var_sat, 0.0, 2.5, 1.0)

        # Row 8: tint
        tint_row = tk.Frame(right, bg="white")
        tint_row.pack(fill="x", pady=(6,0))
        tk.Label(tint_row, text="Tint", bg="white").pack(side="left")
        tk.Button(tint_row, text="Pick Color", command=self.pick_tint_color).pack(side="left", padx=8)
        self.make_slider(right, "Tint Strength", self.var_tint_strength, 0.0, 1.0, 0.0, resolution=0.01)

        # Anytime a slider changes, re-render
        for var in (self.var_bright, self.var_contrast, self.var_sat, self.var_tint_strength):
            var.trace_add("write", lambda *_: self.render())

    def make_slider(self, parent, label, var, mn, mx, init, resolution=0.01):
        row = tk.Frame(parent, bg="white")
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, bg="white", width=12, anchor="w").pack(side="left")
        scale = tk.Scale(row, from_=mn, to=mx, orient="horizontal", resolution=resolution,
                         variable=var, length=220, showvalue=True, bg="white", highlightthickness=0)
        scale.pack(side="left", padx=4)

    # ---------------- Image I/O ----------------
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.webp;*.tif;*.tiff")])
        if not path:
            return
        img = Image.open(path).convert("RGB")
        self.original_img = img.copy()
        self.base_img = img.copy()
        self.history = []
        self.zoom = 1.0
        self.center_image()
        self.reset_sliders()
        self.render()

    def save_image(self):
        if not self.base_img:
            return
        final = self.compose_final()
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("BMP", "*.bmp"), ("WEBP", "*.webp")])
        if path:
            try:
                final.save(path)
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    # ---------------- View & Render ----------------
    def center_image(self):
        # Center or create image item
        if self.img_item is None:
            self.img_item = self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, image=None)
        else:
            self.canvas.coords(self.img_item, self.canvas_w//2, self.canvas_h//2)

    def fit_to_view(self):
        if not self.base_img: return
        w, h = self.base_img.size
        scale_w = self.canvas_w / w
        scale_h = self.canvas_h / h
        self.zoom = min(scale_w, scale_h) * 0.98  # small margin
        self.render()

    def adjust_zoom(self, factor):
        if not self.base_img: return
        self.zoom *= factor
        self.zoom = max(self.min_zoom, min(self.zoom, self.max_zoom))
        self.render()

    def render(self):
        if not self.base_img:
            return
        # Start from base image (discrete edits already applied)
        img = self.base_img

        # Live adjustments
        if self.var_sat.get() != 1.0:
            img = ImageEnhance.Color(img).enhance(self.var_sat.get())
        if self.var_bright.get() != 1.0:
            img = ImageEnhance.Brightness(img).enhance(self.var_bright.get())
        if self.var_contrast.get() != 1.0:
            img = ImageEnhance.Contrast(img).enhance(self.var_contrast.get())
        if self.var_tint_strength.get() > 0.001:
            tint = Image.new("RGB", img.size, self.tint_color)
            alpha = float(self.var_tint_strength.get())
            img = Image.blend(img.convert("RGB"), tint, alpha)

        # Zoom (purely visual)
        zw = max(1, int(img.width * self.zoom))
        zh = max(1, int(img.height * self.zoom))
        disp = img.resize((zw, zh), Image.LANCZOS)

        # Push to canvas
        self.tk_img = ImageTk.PhotoImage(disp)
        if self.img_item is None:
            self.img_item = self.canvas.create_image(self.canvas_w//2, self.canvas_h//2, image=self.tk_img)
        else:
            self.canvas.itemconfig(self.img_item, image=self.tk_img)

    def compose_final(self):
        """Apply current live adjustments to a copy for saving/export."""
        img = self.base_img.copy()
        img = ImageEnhance.Color(img).enhance(self.var_sat.get())
        img = ImageEnhance.Brightness(img).enhance(self.var_bright.get())
        img = ImageEnhance.Contrast(img).enhance(self.var_contrast.get())
        if self.var_tint_strength.get() > 0.001:
            tint = Image.new("RGB", img.size, self.tint_color)
            img = Image.blend(img.convert("RGB"), tint, float(self.var_tint_strength.get()))
        return img

    def reset_sliders(self):
        self.var_bright.set(1.0)
        self.var_contrast.set(1.0)
        self.var_sat.set(1.0)
        self.var_tint_strength.set(0.0)

    # ---------------- Discrete Edits (with Undo) ----------------
    def push_history(self):
        if self.base_img:
            self.history.append(self.base_img.copy())
            if len(self.history) > self.max_history:
                self.history.pop(0)

    def undo(self):
        if not self.history:
            return
        self.base_img = self.history.pop()
        self.render()

    def apply_discrete(self, new_img):
        if not self.base_img:
            return
        self.push_history()
        self.base_img = new_img.convert("RGB")
        self.render()

    def rotate(self):
        if not self.base_img: return
        self.apply_discrete(self.base_img.rotate(90, expand=True))
        self.fit_to_view()

    def crop_dialog(self):
        if not self.base_img: return
        w = simpledialog.askinteger("Crop Width", "Enter width (pixels):", minvalue=1)
        h = simpledialog.askinteger("Crop Height", "Enter height (pixels):", minvalue=1)
        if not w or not h: return
        bw, bh = self.base_img.size
        w = min(w, bw)
        h = min(h, bh)
        # Crop from top-left (0,0) -> (w,h). You can change to center-crop if you prefer.
        self.apply_discrete(self.base_img.crop((0, 0, w, h)))

    def filter_bw(self):
        if not self.base_img: return
        self.apply_discrete(self.base_img.convert("L").convert("RGB"))

    def filter_sepia(self):
        if not self.base_img: return
        gray = self.base_img.convert("L")
        sepia = ImageOps.colorize(gray, black="#704214", white="#C0A080")
        self.apply_discrete(sepia)

    def filter_invert(self):
        if not self.base_img: return
        self.apply_discrete(ImageOps.invert(self.base_img.convert("RGB")))

    def filter_autocontrast(self):
        if not self.base_img: return
        self.apply_discrete(ImageOps.autocontrast(self.base_img, cutoff=2))

    def pick_tint_color(self):
        color = colorchooser.askcolor(initialcolor="#ff0000", title="Pick Tint Color")
        if color and color[0]:
            r, g, b = map(int, color[0])
            self.tint_color = (r, g, b)
            self.render()

    def reset_to_original(self):
        if not self.original_img:
            return
        self.base_img = self.original_img.copy()
        self.history = []
        self.zoom = 1.0
        self.center_image()
        self.reset_sliders()
        self.render()

    # ---------------- Mouse interactions ----------------
    def on_drag_start(self, event):
        if self.img_item is None: return
        self.drag_start = (event.x, event.y)

    def on_drag_move(self, event):
        if self.drag_start is None or self.img_item is None: return
        dx = event.x - self.drag_start[0]
        dy = event.y - self.drag_start[1]
        self.canvas.move(self.img_item, dx, dy)
        self.drag_start = (event.x, event.y)

    def on_wheel_zoom(self, event):
        if event.delta > 0:
            self.adjust_zoom(1.1)
        else:
            self.adjust_zoom(1/1.1)

def main():
    root = tk.Tk()
    app = MiniPhotoEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
