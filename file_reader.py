import csv

try:
    import thread
    import threading
except ImportError:
    thread = None


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
            self.header = self._reader.next()

        self.current_row = []

        if thread:
            self.lock = threading.RLock()
        else:
            self.lock = None

    def _acquire_lock(self):
        if self.lock:
            self.lock.acquire()

    def _release_lock(self):
        if self.lock:
            self.lock.release()

    def get_next_row(self):
        self._acquire_lock()
        try:
            self.current_row = self._reader.next()
            return self.current_row
        except StopIteration:
            return None
        finally:
            self._release_lock()

    def get_next_dict(self):
        self.get_next_row()
        return self.row_as_dict()

    def row_as_dict(self):
        if not self.has_header:
            raise NoHeaderException()
        return dict(zip(self.header, self.current_row))

    def rows(self):
        while self.get_next_row() is not None:
            yield self.current_row

    def dicts(self):
        while self.get_next_row() is not None:
            yield self.row_as_dict()

    def close(self):
        self._fh.close()
