#main_file_watcher.py is supposed to take a name of template and name of pdf and in return save corresponding json (that is result of ocr) to a jsons folder

# run it as: python main_file_watcher.py <template_without_file_extension>

import sys
import os
import json
from crop import *
from simpleOCR import *
import time
import shutil

WATCHED_FOLDER = './'
FOLDER_PDFS_ARE_MOVED_TO = "./file_watching_trial/"
FOLDER_THAT_STORES_PDFS = "./pdfs/"
FOLDER_THAT_STORES_JSONS = "./jsons/"

#if fail == True, then some preconditions were not met and programme will not generate the expected output
fail = False

#cheking if enough command line arguments were passed
if len(sys.argv) != 2:
    print("not enough command line arguments passed")
    fail = True

#checking if files passed as CLA could be found
if fail == False:
    if sys.argv[1]+".pkl" not in os.listdir("templates/"):
        print("template could not be located (enter just the file name title, without extension)")
        fail = True

#if everything was fine, use OCR
if fail == False:
    chosenTemplate = load_template(sys.argv[1])

    while True:
        time.sleep(3)
        file_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)
        for file_item in file_list:

            #applying template on an image
            chosenPDF = FOLDER_THAT_STORES_PDFS + file_item
            croppedImages = crop_from_template(chosenTemplate,chosenPDF)

            textOutput = {}

            #populating the dictionary
            for entry in croppedImages:
                textOutput[entry[0]] = image_to_text(entry[1])

            textOutput = json.dumps(textOutput, ensure_ascii=False)

            with open(FOLDER_THAT_STORES_JSONS+file_item[:-4]+".json","w") as f:
                f.write(textOutput)

            # move file to the folder we want it to, and remove the filename from the list of files in the directory
            shutil.move(WATCHED_FOLDER + file_item, FOLDER_PDFS_ARE_MOVED_TO + file_item)
            file_list.remove(file_item)
else:
    print("program could not deliver")
