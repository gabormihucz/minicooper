#main.py is supposed to take a name of template and name of pdf and in return save corresponding json (that is result of ocr) to a jsons folder

import sys
import os
import json
from crop import *
from simpleOCR import *


#if fail == True, then some preconditions were not met and programme will not generate the expected output
fail = False

#cheking if enough command line arguments were passed
if len(sys.argv) != 3:
    print("not enough command line arguments passed")
    fail = True

#checking if files passed as CLA could be found
if fail == False:
    if sys.argv[1]+".pkl" not in os.listdir("templates/") or sys.argv[2]+".pdf" not in os.listdir("pdfs/"):
        print("either template or pdf could not be located (enter just the file name title, without extension)")
        fail = True

#if everything was fine, use OCR
if fail == False:
    chosenTemplate = load_template(sys.argv[1])
    chosenPDF = "pdfs/"+sys.argv[2]+".pdf"
    #applying template on an image
    croppedImages = crop_from_template(chosenTemplate,chosenPDF)

    textOutput = {}

    #populating the dictionary
    for entry in croppedImages:
        textOutput[entry[0]] = image_to_text(entry[1])

    textOutput = json.dumps(textOutput, ensure_ascii=False)

    with open("jsons/"+sys.argv[2]+".json","w") as f:
        f.write(textOutput)

else:
    print("program could not deliver")
