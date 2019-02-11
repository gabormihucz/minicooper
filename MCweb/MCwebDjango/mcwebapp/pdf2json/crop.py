import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pickle
import json

#loads a template directly from json
def load_template_json(name, path):
    with open(path + name +".json","r") as template:
        templateDictionary = json.loads(template.read())
        return templateDictionary

# takes a dictionary template and a string filename and saves cropped images according to the template
# format of template:
# template = {"label" : {"x1":100,"x2":300,"y1":400,"y2":600}, ...}
# page_num specifies which page is to be processed
def crop_from_template(template, filename, page_num = 0):
    images = convert_from_path(filename)
    page = images[page_num]
    page_array = np.asarray(page)

    if "size" in template.keys():
        y_scale = page_array.shape[0]/template["size"]["y"]
        x_scale = page_array.shape[1]/template["size"]["x"]
    else:
        y_scale = 1
        x_scale = 1

    croppedImages = []
    for label,coords in template.items():
        if label != "size":
            y1 = int(y_scale * min(coords["y1"], coords["y2"]))
            y2 = int(y_scale * max(coords["y1"], coords["y2"]))
            x1 = int(x_scale * min(coords["x1"], coords["x2"]))
            x2 = int(x_scale * max(coords["x1"], coords["x2"]))
            croppped = page_array[y1:y2,x1:x2]
            croppedImages += [[label,Image.fromarray(croppped)]]

    return croppedImages
