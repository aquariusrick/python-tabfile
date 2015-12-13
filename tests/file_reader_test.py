import os
import unittest

from file_reader import FileReader


class TestFileReader(unittest.TestCase):
    TEST_FILENAME = 'test_file.csv'
    CSV_STRING = 'header_a,header_b\nval_a,val_b\n'
    EXPECTED_ROWS = [
        ['val_a', 'val_b'],
    ]

    def setUp(self):
        with open(self.TEST_FILENAME, 'w') as f:
            f.write(self.CSV_STRING)

    def tearDown(self):
        if os.path.isfile(self.TEST_FILENAME):
            os.remove(self.TEST_FILENAME)

    def test_read_row(self):
        csv_file = FileReader(self.TEST_FILENAME, has_header=True)

        row = csv_file.get_next_row()
        self.assertEqual(row, self.EXPECTED_ROWS[0])
