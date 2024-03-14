import asyncio
import aiofiles
from PIL import Image
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

def categorize_brightness(brightness):
    if brightness < 10:
        return "extremely dark"
    elif brightness < 30:
        return "very dark"
    elif brightness < 65:
        return "dark"
    elif brightness < 135:
        return "normal"
    elif brightness < 190:
        return "bright"
    elif brightness < 220:
        return "very bright"
    else:
        return "extremely bright"

async def process_image(tag_file_path, brightness_category):
    # Async operation for reading and optionally updating tag files
    update_tag = brightness_category != "normal"
    if update_tag:
        async with aiofiles.open(tag_file_path, 'r') as tag_file:
            tags = await tag_file.read()
        tags = tags.strip()
        tags_updated = f"{tags},{brightness_category}" if tags else brightness_category

        async with aiofiles.open(tag_file_path, 'w') as tag_file:
            await tag_file.write(tags_updated)

async def process_images(input_dir):
    tasks = []
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(('.jpg', '.png')):
                image_path = os.path.join(root, filename)
                tag_file_path = os.path.join(root, os.path.splitext(filename)[0] + '.txt')

                # Process image (CPU-bound, synchronous operation)
                with Image.open(image_path) as img:
                    grayscale_img = img.convert("L")
                    img_array = np.array(grayscale_img)
                    brightness = np.mean(img_array)
                    brightness_category = categorize_brightness(brightness).replace(" ", "_")

                # Schedule the processing of each tag file as an asynchronous task
                task = process_image(tag_file_path, brightness_category)
                tasks.append(task)

    await asyncio.gather(*tasks)

def main():
    root = tk.Tk()
    root.withdraw()  # Don't need a full GUI, so keep the root window from appearing
    input_dir = filedialog.askdirectory()  # Show an "Open" dialog box and return the path to the selected directory

    if input_dir:  # If a directory was selected
        asyncio.run(process_images(input_dir))

if __name__ == "__main__":
    main()
