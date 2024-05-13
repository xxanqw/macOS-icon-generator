from PIL import Image, PngImagePlugin

def generate_image(background_path, overlay_path, output_path, overlay_resize=None):
    """
    Накладає одне зображення на інше, центруючи його, та зберігає результат.
    Якщо накладене зображення не PNG, конвертує його в PNG перед накладанням.

    Аргументи:
        background_path (str): Шлях до фонового зображення.
        overlay_path (str): Шлях до зображення, яке потрібно накласти.
        output_path (str): Шлях для збереження результуючого зображення.
        overlay_resize (tuple, optional): Кортеж (ширина, висота) для зміни розміру накладеного зображення (за замовчуванням None).
    """

    background = Image.open(background_path)
    overlay = Image.open(overlay_path)

    # Конвертація в PNG, якщо потрібно
    if overlay.format != "PNG":
        overlay = overlay.convert("RGBA")  # Конвертуємо в RGBA для збереження прозорості

    if overlay_resize:
        overlay = overlay.resize(overlay_resize)

    # Обчислення координат для центрування
    background_width, background_height = background.size
    overlay_width, overlay_height = overlay.size
    overlay_x = (background_width - overlay_width) // 2
    overlay_y = (background_height - overlay_height) // 2

    background.paste(overlay, (overlay_x, overlay_y), overlay)
    metadata = PngImagePlugin.PngInfo()
    background.save(output_path, format="PNG", pnginfo=metadata)
