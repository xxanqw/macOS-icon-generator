import os
from os import path as p
from PIL import Image

def create_icns(png_files, output_path):

    required_sizes = [
        (16, 16, "icon_16x16.png"),
        (32, 32, "icon_16x16@2x.png"),
        (32, 32, "icon_32x32.png"),
        (64, 64, "icon_32x32@2x.png"),
        (128, 128, "icon_128x128.png"),
        (256, 256, "icon_128x128@2x.png"),
        (256, 256, "icon_256x256.png"),
        (512, 512, "icon_256x256@2x.png"),
        (512, 512, "icon_512x512.png"),
        (1024, 1024, "icon_512x512@2x.png"),
    ]

    temp_dir = "temp_icons"
    iconset_path = os.path.join(temp_dir, "icon.iconset")
    os.makedirs(iconset_path, exist_ok=True)

    for png_file_path in png_files:
        if not os.path.exists(png_file_path):
            print(f"Попередження: файл '{png_file_path}' не знайдено.")
            continue

        try:
            img = Image.open(png_file_path).convert("RGBA")  # Конвертуємо в RGBA
            width, height = img.size

            if (width, height) in [size[:2] for size in required_sizes]:
                iconset_file = os.path.join(iconset_path, next(size[2] for size in required_sizes if size[:2] == (width, height)))
                img.save(iconset_file, format="PNG")
            else:
                raise ValueError(f"Неправильний розмір зображення: {png_file_path}")
        except (ValueError, OSError) as e:
            print(f"Помилка при обробці файлу '{png_file_path}': {e}")
            continue

    cmd = f"iconutil -c icns -o {output_path} {iconset_path}"
    result = os.system(cmd)
    if result != 0:
        raise RuntimeError(f"Помилка при виконанні iconutil: {cmd}")
    
    os.system(f"rm -rf {temp_dir}")
