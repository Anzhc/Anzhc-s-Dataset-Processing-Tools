from tkinter import Tk, filedialog
from PIL import Image, ImageFilter
import os
from pathlib import Path
import math
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import random

def parallel_lagrange_interpolate(args):
    x, y, new_xs, image_height = args
    results = []
    for new_x in new_xs:
        # Choose a random row (height) each time
        random_row = random.randint(0, image_height - 1)
        y_row = y[random_row * len(x): (random_row + 1) * len(x)]  # Select the row
        
        if len(x) < 2 or len(y_row) < 2:
            raise ValueError("Need at least two points for interpolation.")
        
        for i in range(len(x) - 1):
            if x[i] <= new_x <= x[i + 1]:
                x0, x1 = x[i], x[i + 1]
                y0, y1 = y_row[i], y_row[i + 1]
                results.append(y0 + (new_x - x0) * (y1 - y0) / (x1 - x0))
                break
    return results

def resize_and_replace_image(file_path, max_pixels=1):  # 1536x1536 = 2359296  768x768 = 589824
    with Image.open(file_path) as img:
        img = img.convert('RGB')  # Ensure image is in RGB format
        total_pixels = img.size[0] * img.size[1]

        if total_pixels > max_pixels:
            factor = 1 #math.sqrt(total_pixels / max_pixels)
            new_width = int(img.size[0] / factor)
            new_height = int(img.size[1] / factor)
            
            img_array = np.array(img)
            new_img_array = np.zeros((new_height, new_width, 3), dtype=np.uint8)

            x = np.arange(img.size[0])
            y = np.arange(img.size[1])
            new_x = np.linspace(0, img.size[0] - 1, new_width)
            new_y = np.linspace(0, img.size[1] - 1, new_height)

            with ProcessPoolExecutor() as executor:
                futures = []
                for channel in range(3):
                    args = (x, img_array[:, :, channel].flatten(), new_x, img.size[1])
                    futures.append(executor.submit(parallel_lagrange_interpolate, args))

                for i, future in enumerate(futures):
                    interpolated_rows = future.result()
                    for row_index, row in enumerate(interpolated_rows):
                        new_img_array[:, row_index, i] = np.array(row).astype(np.uint8)

                # Apply unsharp mask if needed
                img = Image.fromarray(new_img_array)
                img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        new_file_path = file_path.with_suffix('.jpg')
        img.save(new_file_path, 'JPEG', quality=95)

        # Delete the original file if it's not a JPEG
        if file_path.suffix.lower() not in ['.jpg', '.jpeg']:
            os.remove(file_path)

def process_images(folder_path):
    with ThreadPoolExecutor() as executor:
        futures = []
        for file in Path(folder_path).rglob("*"):
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                futures.append(executor.submit(resize_and_replace_image, file))

        for future in futures:
            future.result()

def main():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    folder_path = filedialog.askdirectory()  # show an "Open" dialog box and return the path to the selected folder
    
    if folder_path:
        process_images(folder_path)
        print("Processing complete.")
    else:
        print("Folder selection cancelled.")

if __name__ == "__main__":
    main()