from gen import PDFConfig, Entry, GridPDF


def ensure_dummy_image(path: str, title: str = "Sample") -> str:
    """
    Create a dummy image if it doesn't exist.
    Requires: pip install pillow
    """
    if os.path.exists(path):
        return path

    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (800, 600), color=(70, 130, 180))
        d = ImageDraw.Draw(img)
        d.text((50, 50), title, fill=(255, 255, 255), font_size=40)
        img.save(path)
        print(f"Created dummy image: {path}")
        return path
    except ImportError:
        print("⚠️  Pillow not installed. Images will show placeholders.")
        return ""


def generate_test_data(number = 16):
    image_dir = "images"
    os.makedirs(image_dir, exist_ok=True)

    file_name = 'placeholder_img'
    image_path = ensure_dummy_image(f"{image_dir}/{file_name}.jpg", "SAMPLE")
    return [
        Entry(id=f"{i:03d}", title=f"Entry_{i}", summary=f"Details for entry {i}.", image_path=image_path)
        for i in range(1, 81)
    ]


def run_test():
    # Configuration
    config_dict = {
        'page': {'width': 210, 'height': 297},
        'margins': {'left': 15, 'right': 15, 'top': 15, 'bottom': 15},
        'layout': {
            'column_count': 4,
            'cell_height': 15,
            'image_padding': 10,
        },
        'colors': {
            'primary': (0, 0, 0),
            'secondary': (60, 60, 60),
            'light': (140, 140, 140),
            'line': (180, 180, 180),
        },
        'fonts': {
            'name': 24,
            'section_title': 14,
            'default': 10,
        },
        'spacing': {
            'small': 4,
            'medium': 6,
        },
    }

    config = PDFConfig.from_dict(config_dict)
    pdf = GridPDF(config)
    pdf.generate_document(generate_test_data(), "output_with_images.pdf")

