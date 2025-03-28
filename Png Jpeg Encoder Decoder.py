import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk

def compress_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(img_yuv)
    
    block_size = 32
    height, width = y.shape
    compressed_y = np.zeros_like(y)
    
    compression_rate = simpledialog.askinteger("Compression Rate", "Enter compression level (1-15):", minvalue=1, maxvalue=15)
    if compression_rate is None:
        return
    
    a = 16 - compression_rate
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = y[i:i+block_size, j:j+block_size]
            block_dct = cv2.dct(np.float32(block))
            h, w = block_dct.shape
            for m in range(min(a, h), h):
                for n in range(min(a, w), w):  
                    block_dct[m, n] = 0        

            compressed_y[i:i+block_size, j:j+block_size] = cv2.idct(block_dct)
    
    img_compressed = cv2.merge([compressed_y.astype(np.uint8), u, v])
    image_array = np.array(img_compressed)
    binary_data = img_compressed.tobytes()
    
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
    if not save_path:
        return
    
    with open(save_path, 'wb') as bin_file:
        bin_file.write(binary_data)
    
    img_decompressed = cv2.cvtColor(image_array.reshape((height, width, 3)), cv2.COLOR_YUV2BGR)
    cv2.imwrite(save_path, img_decompressed)

def decompress_image():
    file_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if not file_path:
        return
    
    with open(file_path, 'rb') as bin_file:
        binary_data = bin_file.read()
    
    image_array = np.frombuffer(binary_data, dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not save_path:
        return
    cv2.imwrite(save_path, img)

def create_ui():
    root = tk.Tk()
    root.title("Image Compressor")
    root.geometry("300x200")
    
    btn_compress = tk.Button(root, text="Compress PNG", command=compress_image)
    btn_compress.pack(pady=10)
    
    btn_decompress = tk.Button(root, text="Decompress JPG", command=decompress_image)
    btn_decompress.pack(pady=10)
    
    root.mainloop()

create_ui()
