import sys
import os

from crop import *
from simpleOCR import *

fail = False

templates = os.listdir("templates/")

if len(sys.argv) != 3:
    print("not enough command line arguments passed")
    fail = True

if fail == False:
    if sys.argv[1]+".pkl" not in os.listdir("templates/") or sys.argv[2]+".pdf" not in os.listdir("pdfs/"):
        print("either template or pdf could not be located (enter just the file name title, without extension)")
        fail = True


if fail == False:
    chosenTemplate = load_template(sys.argv[1])
    chosenPDF = "pdfs/"+sys.argv[2]+".pdf"

    croppedImages = crop_from_template(chosenTemplate,chosenPDF)

    textOutput = {}

    for entry in croppedImages:
        textOutput[entry[0]] = image_to_text(entry[1])

    print(textOutput)

else:
    print("program could not deliver")
