import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pickle
#fns that loads pickele changes it to json, returning the actual template that is required by OCR
def load_template(name):
    with open("templates/" + name + ".pkl", "rb") as f:
        return pickle.load(f)


# takes a dictionary template and a string filename and saves cropped images according to the template
# format of template:
# template = {"label" : {"x1":100,"x2":300,"y1":400,"y2":600}, ...}
# page_num specifies which page is to be processed
def crop_from_template(template, filename, page_num = 0):
    images = convert_from_path(filename)
    page = images[page_num]
    page_array = np.asarray(page)
    #test = Image.fromarray(page_array)
    #test.save("test.jpeg")

    croppedImages = []
    for label,coords in template.items():
        y1 = min(coords["y1"], coords["y2"])
        y2 = max(coords["y1"], coords["y2"])
        x1 = min(coords["x1"], coords["x2"])
        x2 = max(coords["x1"], coords["x2"])
        croppped = page_array[y1:y2,x1:x2]
        croppedImages += [[label,Image.fromarray(croppped)]]

    return croppedImages
