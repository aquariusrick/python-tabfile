from collections import namedtuple

import csv


class FileReaderException(Exception):
    pass


class NoHeaderException(FileReaderException):
    pass


class FileReader(object):
    def __init__(self, filename, has_header=True):
        self.filename = filename
        self._fh = open(filename, 'rU')
        self._reader = csv.reader(self._fh)
        self.has_header = has_header

        if self.has_header:
            self._reader = csv.reader(self._fh)
            self._namedtuple = namedtuple(
                'FileReaderRow',
                self._reader.next()
            )
        else:
            self._namedtuple = None

        self.current_row = None

    def __iter__(self):
        return self

    def next(self):
        return self.get_next_row()

    @property
    def header(self):
        if not self.has_header:
            raise NoHeaderException()

        return self._namedtuple._fields

    def get_next_row(self):
        try:
            new_row = self._reader.next()
        except StopIteration:
            return None

        if self._namedtuple is None:
            self.current_row = tuple(new_row)
        else:
            self.current_row = self._namedtuple(*new_row)

        return self.current_row

    def get_next_dict(self):
        if not self.has_header:
            raise NoHeaderException()
        return self.get_next_row()._asdict()

    def row_as_dict(self):
        if not self.has_header:
            raise NoHeaderException()
        return self.current_row._asdict()

    def rows(self):
        while self.get_next_row() is not None:
            yield self.current_row

    def dicts(self):
        while self.get_next_row() is not None:
            yield self.row_as_dict()

    def close(self):
        self._fh.close()
