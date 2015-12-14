import csv
import os
import unittest

from file_reader import FileReader


class TestFileReader(unittest.TestCase):
    TEST_FILENAME = 'test_file.csv'
    EXPECTED_HEADER = ('header_a', 'header_b')
    EXPECTED_ROWS = (
        ('val_a1', 'val_b1'),
        ('val_a2', 'val_b2'),
        ('val_a3', 'val_b3'),
        ('val_a4', 'val_b4'),
        ('val_a5', 'val_b5'),
    )

    @classmethod
    def setUpClass(cls):
        with open(cls.TEST_FILENAME, 'w') as f:
            csv_writer = csv.writer(f)
            rows = (cls.EXPECTED_HEADER, ) + cls.EXPECTED_ROWS
            for r in rows:
                csv_writer.writerow(r)

    def setUp(self):
        self._csv_file = FileReader(self.TEST_FILENAME, has_header=True)

    def tearDown(self):
        self._csv_file.close()

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.TEST_FILENAME):
            os.remove(cls.TEST_FILENAME)

    def test_read_first_row(self):
        row = self._csv_file.get_next_row()
        self.assertEqual(tuple(row), self.EXPECTED_ROWS[0])

    def test_header(self):
        self.assertEqual(
            tuple(self._csv_file.header),
            self.EXPECTED_HEADER
        )

    def test_iterable(self):
        for rows, expected in zip(self._csv_file, self.EXPECTED_ROWS):
            self.assertEqual(tuple(rows), expected)
