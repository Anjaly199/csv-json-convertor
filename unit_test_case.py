import unittest

from converter import *


class TestMain(unittest.TestCase):

    def test_valid_format(self):
        self.assertTrue(main(), "/home/anjaly/Desktop/data1.csv")

    def test_filepath_format(self):
        self.assertRaises(FileNotFoundError, main(), "/home/anjaly/Desktop/", " ",
                          "File format error or no input given")

    def test_file_not_found(self):
        self.assertRaises(FileNotFoundError, read_csv(filepath="/home/anjaly/Desktop/one.csv"), "File does not exist")


if __name__ == "__main__":
    unittest.main()

