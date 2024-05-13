from PIL import Image
from os import path as p

def resize_image(input_path, output_path, new_size):
    image = Image.open(input_path)
    resized_image = image.resize(new_size)
    resized_image.save(output_path)

def resize():
    base_path = p.dirname(p.abspath(__file__))
    input_path = p.join(base_path, "..", "img", "icnoutput", "icons", "icon_512x512@2x.png")
    output_dir = p.join(base_path, "..", "img", "icnoutput", "icons")

    sizes = [16, 32, 128, 256, 512]  # Список розмірів без @2x

    for size in sizes:
        # Створюємо іконку звичайного розміру
        output_path = p.join(output_dir, f"icon_{size}x{size}.png")
        resize_image(input_path, output_path, (size, size))

        # Створюємо іконку Retina (@2x)
        retina_size = (size * 2, size * 2)
        output_path = p.join(output_dir, f"icon_{size}x{size}@2x.png")
        resize_image(input_path, output_path, retina_size)
