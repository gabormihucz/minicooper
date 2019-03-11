import sys
import os
import json
from mcwebapp.pdf2json import crop
from mcwebapp.pdf2json import simpleOCR

#recursively attempts to write copies of the json file until one can be written without overwriting anything
def write_output_recur(output_path, pdf_name, textOutput, iter = 0):
    try:
        with open(output_path + pdf_name + "(" + str(2+iter) + ").json","x",encoding="utf8") as f:
            f.write(textOutput)
        return iter + 2
    except:
        return write_output_recur(output_path, pdf_name, textOutput, iter+1)

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


    copies = 1
    # print(textTest)
    textOutput = json.dumps(textOutput, ensure_ascii=False)
    try:
        with open(output_path + pdf_name + ".json","x",encoding="utf8") as f:
            f.write(textOutput)
        copies = 1
    except:
        copies = write_output_recur(output_path, pdf_name, textOutput)


    return_dict = {"copies": copies, "mand_filled": mandatory_field_fulfilled}

    return return_dict
