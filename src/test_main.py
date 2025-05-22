import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title_1(self):
        actual_output = extract_title("# Hello")
        expected_output = "Hello"
        self.assertEqual(actual_output, expected_output)

    def test_extract_title_2(self):
        with self.assertRaises(ValueError):
            extract_title("Hello")


if __name__ == "__main__":
    unittest.main()
