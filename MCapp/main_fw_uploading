#main_file_watcher.py is supposed to take a name of template and name of pdf and in return save corresponding json (that is result of ocr) to a jsons folder

# run it as: python main_file_watcher.py <template_without_file_extension>

import sys
import os
import json
from crop import *
from simpleOCR import *
import time
import shutil
import post_to_server


WATCHED_FOLDER = './'
FOLDER_PDFS_ARE_MOVED_TO = "./file_watching_trial/"


#if fail == True, then some preconditions were not met and programme will not generate the expected output
fail = False

#cheking if enough command line arguments were passed
if len(sys.argv) != 2:
    print("not enough command line arguments passed")
    fail = True

#if everything was fine, use OCR
if fail == False:
    chosenTemplate = load_template(sys.argv[1])

    while True:
        time.sleep(1)
        file_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)
        for file_item in file_list:
            post_to_server.post(file_item)

 
            # move file to the folder we want it to, and remove the filename from the list of files in the directory
            shutil.move(WATCHED_FOLDER + file_item, FOLDER_PDFS_ARE_MOVED_TO + file_item)
            file_list.remove(file_item)
else:
    print("program could not deliver")
