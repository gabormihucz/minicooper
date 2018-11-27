try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract as pt

def image_to_text(image):
    string_result = pt.image_to_string(Image.open(image))
    return string_result