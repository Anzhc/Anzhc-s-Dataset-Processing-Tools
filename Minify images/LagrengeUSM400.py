from tkinter import Tk, filedialog
from PIL import Image, ImageFilter
import os
from pathlib import Path
import math
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from concurrent.futures import ProcessPoolExecutor

def lagrange_interpolate(channel_data, new_dimension):
    # Reshape channel data to 2D image shape for interpolation
    original_height, original_width = channel_data.shape
    new_width, new_height = new_dimension
    # Prepare for interpolation
    x = np.arange(original_width)
    y = np.arange(original_height)
    new_x = np.linspace(0, original_width - 1, new_width)
    new_y = np.linspace(0, original_height - 1, new_height)
    # Interpolate over x-axis
    interp_x = np.array([np.interp(new_x, x, channel_data[row, :]) for row in range(original_height)])
    # Interpolate over y-axis
    interp_xy = np.array([np.interp(new_y, y, interp_x[:, col]) for col in range(new_width)]).T
    return interp_xy

def resize_and_replace_image(file_path, max_pixels=2359296):  # 1536x1536 = 2359296  768x768 = 589824
    with Image.open(file_path) as img:
        img = img.convert('RGB')  # Ensure image is in RGB format
        total_pixels = img.size[0] * img.size[1]

        if total_pixels > max_pixels:
            factor = math.sqrt(total_pixels / max_pixels)
            #factor=1
            new_width = int(img.size[0] / factor)
            new_height = int(img.size[1] / factor)

            img_array = np.array(img)
            new_img_array = np.zeros((new_height, new_width, 3), dtype=np.uint8)

            # Use ProcessPoolExecutor to parallelize interpolation across channels
            with ProcessPoolExecutor() as executor:
                results = executor.map(lagrange_interpolate, [img_array[:, :, i] for i in range(3)], [(new_width, new_height)]*3)
            
            for i, channel_data in enumerate(results):
                new_img_array[:, :, i] = channel_data.astype(np.uint8)

            # Apply unsharp mask to the resized image
            img = Image.fromarray(new_img_array)
            img = img.filter(ImageFilter.UnsharpMask(radius=4, percent=400, threshold=3))

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