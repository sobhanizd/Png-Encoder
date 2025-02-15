import os
from tkinter import Tk, Label, Button, Scale, filedialog, HORIZONTAL, messagebox
from PIL import Image

def select_png():
    global png_file
    png_file = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if png_file:
        label_png.config(text=f"Selected: {os.path.basename(png_file)}")
    else:
        label_png.config(text="No file selected")

def select_jpeg():
    global jpeg_file
    jpeg_file = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpeg;*.jpg")])
    if jpeg_file:
        label_jpeg.config(text=f"Selected: {os.path.basename(jpeg_file)}")
    else:
        label_jpeg.config(text="No file selected")

def encode_png_to_jpeg():
    if not png_file:
        messagebox.showerror("Error", "No PNG file selected!")
        return
    output_size_kb = size_slider.get()
    output_file = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg;*.jpg")])
    if not output_file:
        return
    try:
        img = Image.open(png_file)
        if img.mode != "RGB":
            img = img.convert("RGB")
        quality = 95
        while True:
            img.save(output_file, "JPEG", quality=quality)
            if os.path.getsize(output_file) <= output_size_kb * 1024 or quality <= 10:
                break
            quality -= 5
        messagebox.showinfo("Success", f"Encoded to {os.path.basename(output_file)} with size {output_size_kb} KB")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encode PNG: {e}")

def decode_jpeg_to_png():
    if not jpeg_file:
        messagebox.showerror("Error", "No JPEG file selected!")
        return
    output_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not output_file:
        return
    try:
        img = Image.open(jpeg_file)
        img.save(output_file, "PNG")
        messagebox.showinfo("Success", f"Decoded to {os.path.basename(output_file)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode JPEG: {e}")
root = Tk()
root.title("PNG-JPEG Encoder/Decoder by Sobhan Izadi")
root.geometry("400x450")

png_file = None
jpeg_file = None

Label(root, text="Select PNG File for Encoding:").pack(pady=5)
Button(root, text="Select PNG", command=select_png).pack()
label_png = Label(root, text="No file selected", fg="gray")
label_png.pack(pady=5)

Label(root, text="Select Output Size (KB):").pack(pady=5)
size_slider = Scale(root, from_=10, to=5000, orient=HORIZONTAL)
size_slider.pack()

Button(root, text="Encode PNG to JPEG", command=encode_png_to_jpeg).pack(pady=10)

Label(root, text="Select JPEG File for Decoding:").pack(pady=5)
Button(root, text="Select JPEG", command=select_jpeg).pack()
label_jpeg = Label(root, text="No file selected", fg="gray")
label_jpeg.pack(pady=5)

Button(root, text="Decode JPEG to PNG", command=decode_jpeg_to_png).pack(pady=10)

root.mainloop()
