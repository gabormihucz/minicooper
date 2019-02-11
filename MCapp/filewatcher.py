import sys
import os
import json
import time
import post_to_server


WATCHED_FOLDER = './'

while True:
    time.sleep(1)
    filename_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)
    for filename in filename_list:
        post_to_server.post(filename) # upload them to the database


        # remove the filename from the list of files in the directory, and remove the file from the directory
        filename_list.remove(filename)
        os.remove(WATCHED_FOLDER + filename)
else:
    print("program could not deliver")