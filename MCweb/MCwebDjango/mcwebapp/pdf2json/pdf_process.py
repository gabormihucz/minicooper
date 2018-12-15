
import sys
import os
import json
from mcwebapp.pdf2json import crop
from  mcwebapp.pdf2json import simpleOCR


def pdf_proccess(template_name, pdf_name,input_path, output_path):
    chosenTemplate = load_template(template_name, pdf_name)
    chosenPDF = input_path + pdf_name + ".pdf"
    #applying template on an image
    croppedImages = crop_from_template(chosenTemplate,chosenPDF)

    textOutput = {}

    #populating the dictionary
    for entry in croppedImages:
        textOutput[entry[0]] = image_to_text(entry[1])

    textOutput = json.dumps(textOutput, ensure_ascii=False)

    with open(output_path + pdf_name + ".json","w") as f:
        f.write(textOutput)