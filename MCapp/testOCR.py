import unittest
import simpleOCR
import os

class TestOCR(unittest.TestCase):
    def test_simple_ocr(self):
        print(os.getcwd())
        test_bob = simpleOCR.image_to_text(r"MCapp/pictures/bob.jpg")
        expected = "While Bob ate an apple was in the basket."
        self.assertEqual(test_bob,expected)

if __name__ == "__main__":
    unittest.main()