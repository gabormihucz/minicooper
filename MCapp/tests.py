import unittest
import simpleOCR, crop
import os
import hashlib
from PIL import Image
from pdf2image import convert_from_path
import numpy as np


class TestOCR(unittest.TestCase):
    #test check if template was loaded correctly
    def test_load_template(self):
        #loading template eturns a dictionary, test check if hash of that dictionary matches the precomputed correct hash
        print(os.getcwd())
        loadedTemplate = crop.load_template("SampleTemplate")
        loadedTemplate = hashlib.md5(str(loadedTemplate).encode())

        self.assertEqual(loadedTemplate.hexdigest(),"1655bedf1f0b2c3c411315d2a5bb1de7")


    def test_crop_from_template(self):
        cropLoadTemplateOutput = {'allContent': {'x1': 0, 'x2': 1000, 'y1': 0, 'y2': 1000}}
        croppedImages = crop.crop_from_template(cropLoadTemplateOutput,"pdfs/bob.pdf",0)
        self.assertEqual(len(str(croppedImages)),83)


    #test checks if py tesseract works corectly
    def test_simple_ocr(self):
        cropLoadTemplateOutput = {'allContent': {'x1': 0, 'x2': 1000, 'y1': 0, 'y2': 1000}}
        croppedImages = crop.crop_from_template(cropLoadTemplateOutput,"pdfs/bob.pdf")
        # populating the dictionary
        textOutput = {}
        for entry in croppedImages:
            textOutput[entry[0]] = simpleOCR.image_to_text(entry[1])

        self.assertEqual(textOutput,{'allContent': 'While Bob ate an apple'})


if __name__ == "__main__":
    unittest.main()
