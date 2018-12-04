import os
import time
import shutil

WATCHED_FOLDER = './'
FILE_EXTENSION = '.pdf'
DESTINATION_FOLDER = "./trial/"


while True:
	time.sleep(3)
	file_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith(FILE_EXTENSION)] # get all PDF files in the watched folder in a list (of string representing the file names)
	for file_item in file_list:
		# move file to the folder we want it to, and remove the filename from the list of files in the directory
		shutil.move(WATCHED_FOLDER + file_item, DESTINATION_FOLDER + file_item)
		file_list.remove(file_item)