import unittest
import simpleOCR, crop
import os
import hashlib
from PIL import Image
from pdf2image import convert_from_path
import numpy as np



class TestOCR(unittest.TestCase):

    #test checks if py tesseract works corectly
    def test_simple_ocr(self):

        test_bob = convert_from_path("pdfs/bob.pdf")
        test_bob = test_bob[0]
        test_bob = np.asarray(test_bob)
        test_bob = Image.fromarray(test_bob)
        test_bob = simpleOCR.image_to_text(test_bob)

        self.assertEqual(test_bob,"While Bob ate an apple was in the basket.")

    #test check if template was loaded correctly
    def test_load_template(self):
        #loading template eturns a dictionary, test check if hash of that dictionary matches the precomputed correct hash
        loadedTemplate = crop.load_template("SampleTemplate")
        loadedTemplate = hashlib.md5(str(loadedTemplate).encode())

        self.assertEqual(loadedTemplate.hexdigest(),"1655bedf1f0b2c3c411315d2a5bb1de7")

if __name__ == "__main__":
    unittest.main()
