import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter

# ----------------------
# App Setup
# ----------------------
root = tk.Tk()
root.title("Mini Photo Editor — Zoom + Reset")
root.geometry("1000x750")
root.config(bg="#f5f5f5")

CANVAS_W, CANVAS_H = 700, 480
canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="lightgray", highlightthickness=1)
canvas.pack(pady=10)

# ----------------------
# Global state
# ----------------------
original_img = None
edit_base_img = None
current_img = None
display_tk = None
tint_color = (255, 0, 0)

undo_stack = []
redo_stack = []

zoom_factor = 1.0

# ----------------------
# Undo / Redo
# ----------------------
def push_undo():
    global edit_base_img
    if edit_base_img is None:
        return
    state = {
        "image": edit_base_img.copy(),
        "sliders": (brightness_var.get(), contrast_var.get(), saturation_var.get(), tint_var.get()),
        "zoom": zoom_factor
    }
    undo_stack.append(state)
    redo_stack.clear()

def restore_state(state):
    global edit_base_img, zoom_factor
    edit_base_img = state["image"].copy()
    b, c, s, t = state["sliders"]
    brightness_var.set(b); contrast_var.set(c); saturation_var.set(s); tint_var.set(t)
    zoom_factor = state["zoom"]
    apply_adjustments()

def do_undo():
    global edit_base_img
    if not undo_stack:
        messagebox.showinfo("Undo", "Nothing to undo")
        return
    redo_stack.append({
        "image": edit_base_img.copy(),
        "sliders": (brightness_var.get(), contrast_var.get(), saturation_var.get(), tint_var.get()),
        "zoom": zoom_factor
    })
    state = undo_stack.pop()
    restore_state(state)

def do_redo():
    global edit_base_img
    if not redo_stack:
        messagebox.showinfo("Redo", "Nothing to redo")
        return
    undo_stack.append({
        "image": edit_base_img.copy(),
        "sliders": (brightness_var.get(), contrast_var.get(), saturation_var.get(), tint_var.get()),
        "zoom": zoom_factor
    })
    state = redo_stack.pop()
    restore_state(state)

# ----------------------
# Display
# ----------------------
def show_image(pil_img):
    global display_tk
    if pil_img is None:
        canvas.delete("all")
        return
    img_copy = pil_img.copy()

    # Apply zoom factor
    w, h = img_copy.size
    w, h = int(w * zoom_factor), int(h * zoom_factor)
    img_copy = img_copy.resize((w, h), Image.Resampling.LANCZOS)

    display_tk = ImageTk.PhotoImage(img_copy)
    canvas.delete("all")
    canvas.create_image(CANVAS_W//2, CANVAS_H//2, anchor="center", image=display_tk)

# ----------------------
# Adjustments
# ----------------------
def apply_adjustments(*args):
    global current_img
    if edit_base_img is None:
        return
    img = edit_base_img.copy()
   
    b = max(0.25, min(2.0, brightness_var.get()))
    c = max(0.25, min(2.0, contrast_var.get()))
    s = max(0.0, min(3.0, saturation_var.get()))
    t = max(0.0, min(1.0, tint_var.get()))

    img = ImageEnhance.Brightness(img).enhance(b)
    img = ImageEnhance.Contrast(img).enhance(c)
    img = ImageEnhance.Color(img).enhance(s)

    if t > 0:
        overlay = Image.new("RGB", img.size, tint_color)
        img = Image.blend(img, overlay, t)

    current_img = img
    show_image(current_img)

# ----------------------
# File ops
# ----------------------
def open_image():
    global original_img, edit_base_img, undo_stack, redo_stack, zoom_factor
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not path:
        return
    original_img = Image.open(path).convert("RGB")
    edit_base_img = original_img.copy()
    undo_stack.clear()
    redo_stack.clear()
    zoom_factor = 1.0
    reset_sliders()
    apply_adjustments()

def save_image():
    if current_img is None:
        messagebox.showwarning("Save", "No image to save.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    if not path:
        return
    current_img.save(path)
    messagebox.showinfo("Saved", f"Saved to: {path}")

def reset_to_original():
    global edit_base_img, zoom_factor
    if original_img is None:
        return
    push_undo()
    edit_base_img = original_img.copy()
    zoom_factor = 1.0
    reset_sliders()
    apply_adjustments()

# ----------------------
# Edits
# ----------------------
def rotate_image():
    global edit_base_img
    if edit_base_img is None: return
    push_undo()
    edit_base_img = edit_base_img.rotate(90, expand=True)
    apply_adjustments()

def flip_h():
    global edit_base_img
    if edit_base_img is None: return
    push_undo()
    edit_base_img = edit_base_img.transpose(Image.FLIP_LEFT_RIGHT)
    apply_adjustments()

def flip_v():
    global edit_base_img
    if edit_base_img is None: return
    push_undo()
    edit_base_img = edit_base_img.transpose(Image.FLIP_TOP_BOTTOM)
    apply_adjustments()

def auto_contrast():
    global edit_base_img
    if edit_base_img is None: return
    push_undo()
    edit_base_img = ImageOps.autocontrast(edit_base_img)
    apply_adjustments()

def blur_image():
    global edit_base_img
    if edit_base_img is None: return
    push_undo()
    edit_base_img = edit_base_img.filter(ImageFilter.GaussianBlur(radius=2))
    apply_adjustments()

def sharpen_image():
    global edit_base_img
    if edit_base_img is None: return
    push_undo()
    edit_base_img = edit_base_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    apply_adjustments()

def resize_image():
    global edit_base_img
    if edit_base_img is None: return
    w = simpledialog.askinteger("Resize", "New width (px):", minvalue=1, initialvalue=edit_base_img.width)
    if w is None: return
    h = simpledialog.askinteger("Resize", "New height (px):", minvalue=1, initialvalue=edit_base_img.height)
    if h is None: return
    push_undo()
    edit_base_img = edit_base_img.resize((w, h), Image.Resampling.LANCZOS)
    apply_adjustments()

# ----------------------
# Tint color
# ----------------------
def pick_tint():
    global tint_color
    col = colorchooser.askcolor(title="Pick tint color")
    if col and col[0]:
        tint_color = tuple(map(int, col[0]))
        apply_adjustments()

# ----------------------
# Zoom
# ----------------------
def zoom_in():
    global zoom_factor
    if current_img is None: return
    zoom_factor = min(zoom_factor * 1.25, 5.0)
    apply_adjustments()

def zoom_out():
    global zoom_factor
    if current_img is None: return
    zoom_factor = max(zoom_factor * 0.8, 0.2)
    apply_adjustments()

def reset_zoom():
    global zoom_factor
    if current_img is None: return
    zoom_factor = 1.0
    apply_adjustments()

def reset_sliders():
    brightness_var.set(1.0)
    contrast_var.set(1.0)
    saturation_var.set(1.0)
    tint_var.set(0.0)
# ----------------------
# UI
# ----------------------
toolbar = tk.Frame(root, bg="#ddd")
toolbar.pack(fill="x", padx=8, pady=6)

for text, cmd in [
    ("Open", open_image), ("Save", save_image), ("Undo", do_undo), ("Redo", do_redo),
    ("Rotate", rotate_image), ("Flip H", flip_h), ("Flip V", flip_v),
    ("Resize", resize_image), ("Sharpen", sharpen_image), ("Blur", blur_image),
    ("Auto-Contrast", auto_contrast), ("Zoom In", zoom_in), ("Zoom Out", zoom_out),
    ("Reset Zoom", reset_zoom), ("Reset", reset_to_original)
]:
    tk.Button(toolbar, text=text, command=cmd).pack(side="left", padx=4)

# Sliders
slider_frame = tk.Frame(root, bg="#fff")
slider_frame.pack(pady=8, padx=8, fill="x")

brightness_var = tk.DoubleVar(value=1.0)
contrast_var = tk.DoubleVar(value=1.0)
saturation_var = tk.DoubleVar(value=1.0)
tint_var = tk.DoubleVar(value=0.0)

def make_slider(row, label, var, frm, to, res):
    tk.Label(slider_frame, text=label).grid(row=row, column=0, sticky="w")
    s = tk.Scale(slider_frame, from_=frm, to=to, resolution=res,
                 orient="horizontal", variable=var, length=300,
                 command=apply_adjustments)
    s.grid(row=row, column=1, padx=6, sticky="w")
    s.bind("<ButtonRelease-1>", lambda e: push_undo())
    return s

make_slider(0, "Brightness", brightness_var, 0.25, 2.0, 0.05)
make_slider(1, "Contrast", contrast_var, 0.25, 2.0, 0.05)
make_slider(2, "Saturation", saturation_var, 0.0, 3.0, 0.05)

tk.Button(slider_frame, text="Pick Tint", command=pick_tint).grid(row=3, column=0, sticky="w")
make_slider(3, "Tint Strength", tint_var, 0.0, 1.0, 0.02)



# Start
show_image(None)
root.mainloop()
