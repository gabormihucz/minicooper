try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract as pt

def image_to_text(image):
<<<<<<< HEAD
    string_result = pt.image_to_string(Image.open(image))
    return string_result
=======
    string_result = pt.image_to_string(image)
    return string_result
>>>>>>> dev
