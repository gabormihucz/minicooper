import sys
import os
import json
import time
import shutil
import post_to_server
import unittest

import urllib.request
import json
import base64


FOLDER_PDFS_ARE_COPIED_FROM = './pdfs/'
WATCHED_FOLDER = './'
FOLDER_PDFS_ARE_MOVED_TO = "./file_watching_trial/"
NUMBER_OF_FILES_TO_COPY = 3
NUMBER_OF_TIMES_TO_COPY = 333

class Test1000PDFs(unittest.TestCase):
	def setUp(self):
		start = time.time()

		
		file_list = [f for f in os.listdir(FOLDER_PDFS_ARE_COPIED_FROM) if f.endswith('.pdf')]
		for i in range(NUMBER_OF_FILES_TO_COPY):
			for j in range(NUMBER_OF_TIMES_TO_COPY):
				shutil.copyfile(FOLDER_PDFS_ARE_COPIED_FROM + file_list[i], WATCHED_FOLDER + file_list[i] + str(j) + '.pdf')

		shutil.copyfile(FOLDER_PDFS_ARE_COPIED_FROM + file_list[i], WATCHED_FOLDER + file_list[i] + str(j) + '.pdf')

	def testAutomaticUploading(self):
		while True:
			time.sleep(1)
			file_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)
			if not file_list:
				break
			for file_item in file_list:
				post_to_server.post(file_item) # upload them to the database


				# remove file from the folder, and remove the filename from the list of files in the directory
				file_list.remove(file_item)
				os.remove(file_item)

		end = time.time()
		runtime = end-start
		self.assertLessEqual(runtime, 3600)




if __name__ == "__main__":
	unittest.main()