import numpy as np
from pdf2image import convert_from_path
from PIL import Image

# takes a dictionary template and a string filename and saves cropped images according to the template
# format of template:
# template = {"label" : {"x1":100,"x2":300,"y1":400,"y2":600}, ...}
# page_num specifies which page is to be processed

def crop_from_template(template, filename, page_num = 0):
    images = convert_from_path(filename)
    page = images[page_num]
    page_array = np.asarray(page)

    for label,coords in template.items():
        croppped = page_array[coords["y1"]:coords["y2"],coords["x1"]:coords["x2"]]
        output_image = Image.fromarray(croppped)
        output_image.save(label + ".jpeg")



#t = {"test" : {"x1":100,"x2":300,"y1":400,"y2":600}}

#crop_from_template(t,"Test_file.pdf")