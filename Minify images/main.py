from tkinter import Tk, filedialog
from PIL import Image, ImageFilter
import os
from pathlib import Path
import math
from concurrent.futures import ThreadPoolExecutor

def resize_and_replace_image(file_path, max_pixels=2359296):  # 2359296 1536x1536 / 262144 512x512 / 603648 768x768
    with Image.open(file_path) as img:
        total_pixels = img.size[0] * img.size[1]

        if total_pixels > max_pixels:
            factor = math.sqrt(total_pixels / max_pixels)
            new_size = (int(img.size[0] / factor), int(img.size[1] / factor))
            img = img.resize(new_size, Image.LANCZOS)
        #img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=100, threshold=3))

        new_file_path = file_path.with_suffix('.jpg')
        img.convert('RGB').save(new_file_path, 'JPEG', quality=95)



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