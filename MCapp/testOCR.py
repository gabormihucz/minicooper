import unittest
import simpleOCR

class TestOCR(unittest.TestCase):
    def test_simple_ocr(self):
        test_bob = simpleOCR.image_to_text(r"bob.jpg")
        expected = "While Bob ate an apple was in the basket."
        self.assertEqual(test_bob,expected)

if __name__ == "__main__":
    unittest.main()