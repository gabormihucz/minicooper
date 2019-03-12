import sys
import os
import json
import time
import post_to_server
import argparse

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', default='./')
    parser.add_argument('--IP', default='127.0.0.1:8000')
    args = parser.parse_args(argv)
    args_dict = vars(args)
    WATCHED_FOLDER = args_dict['folder']
    IP_SERVER = args_dict['IP']

    while True:
        time.sleep(1)
        filename_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)
        for filename in filename_list:

            # remove the PDF file from the folder only if a template was found by the server
            if post_to_server.post(WATCHED_FOLDER, filename, IP_SERVER) != -1: # upload them to the database
                # remove the filename from the list of files in the directory, and remove the file from the directory
                os.remove(WATCHED_FOLDER +'/'+ filename)

            filename_list.remove(filename)
    else:
        print("program could not deliver")

if __name__ == "__main__":
    main(sys.argv[1:])
