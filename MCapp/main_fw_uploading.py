import sys
import os
import json
import time
import shutil
import post_to_server


WATCHED_FOLDER = './'
FOLDER_PDFS_ARE_MOVED_TO = "./file_watching_trial/"

while True:
    time.sleep(1)
    file_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)
    for file_item in file_list:
        post_to_server.post(file_item) # upload them to the database


        # move file to the folder we want it to, and remove the filename from the list of files in the directory
        shutil.move(WATCHED_FOLDER + file_item, FOLDER_PDFS_ARE_MOVED_TO + file_item)
        file_list.remove(file_item)
else:
    print("program could not deliver")
