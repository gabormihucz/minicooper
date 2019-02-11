
import sys
import os
import json
from mcwebapp.pdf2json import crop
from mcwebapp.pdf2json import simpleOCR


def pdf_proccess(template_name, template_path,  pdf_name, input_path, output_path):
    chosenTemplate = crop.load_template_json(template_name, template_path)
    chosenPDF = input_path + pdf_name + ".pdf"
    #applying template on an image
    croppedImages = crop.crop_from_template(chosenTemplate,chosenPDF)

    textOutput = {}
    mandatory_field_fulfilled = True

    #populating the dictionary
    for entry in croppedImages:
        text = simpleOCR.image_to_text(entry[1])
        textOutput[entry[0]] = text
        if "mandatory" in chosenTemplate[entry[0]].keys():
            if chosenTemplate[entry[0]]["mandatory"] == True:
                if text == "":
                    print("mandatory field unfulfilled")
                    mandatory_field_fulfilled = False

    textOutput = json.dumps(textOutput, ensure_ascii=False)

    with open(output_path + pdf_name + ".json","w") as f:
        f.write(textOutput)

    return mandatory_field_fulfilled
