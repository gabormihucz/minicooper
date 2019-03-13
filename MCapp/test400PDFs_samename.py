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

# This test assumes that the webserver is running, and there is a template that has a pattern that matches the pdf to copy

FOLDER_PDFS_ARE_COPIED_FROM = './pdfs/'
PDF_TO_COPY = 'bob.pdf'
WATCHED_FOLDER = './'
FOLDER_PDFS_ARE_MOVED_TO = "./file_watching_trial/"
NUMBER_OF_TIMES_TO_COPY = 400
start = time.time()

class Test1000PDFs(unittest.TestCase):
	def testAutomaticUploading(self):
		
		counter = 0
		# start file watching, break after 1000 PDFs
		while counter < NUMBER_OF_TIMES_TO_COPY:
			# wait 0.8 seconds before copying bob.pdf to the watched folder
			time.sleep(3)
			shutil.copyfile(FOLDER_PDFS_ARE_COPIED_FROM + PDF_TO_COPY, WATCHED_FOLDER + PDF_TO_COPY)

			file_list = [f for f in os.listdir(WATCHED_FOLDER) if f.endswith('.pdf')] # get all PDF files in the watched folder in a list (of string representing the file names)

			for file_item in file_list:
				post_to_server.post(WATCHED_FOLDER,file_item) # upload them to the database

				counter+=1
				# remove file from the folder, and remove the filename from the list of files in the directory
				file_list.remove(file_item)
				os.remove(file_item)
			

		# if the test finished within one hour, report pass
		end = time.time()
		runtime = end-start
		self.assertLessEqual(runtime, 3600)

if __name__ == "__main__":
	unittest.main()