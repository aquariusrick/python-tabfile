import csv

try:
    import thread
    import threading
except ImportError:
    thread = None


class FileWriterException(Exception):
    pass


class RecordsAlreadyWritten(FileWriterException):
    pass


class FileWriter(object):
    def __init__(self, filename):
        self._fh = open(filename, 'w')
        self._writer = csv.writer(self._fh)
        self.record_count = 0
        self.header = tuple()
        self.buffer_output = False
        self._create_lock()

    def _create_lock(self):
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

    def write_next_row(self, row):
        if isinstance(row, dict):
            row = [row.get(k, "") for k in self.header]

        self._acquire_lock()
        try:
            # if not isinstance(row, basestring):
            #     row = unicode(row)
            self._writer.writerow(row)
        except:
            raise
        else:
            self.record_count += 1
            if not self.buffer_output:
                self._fh.flush()
        finally:
            self._release_lock()

    def write_header(self, *header, **kwargs):
        if not kwargs.get('force') and self.record_count > 0:
            raise RecordsAlreadyWritten("Header or data already written")

        self.header = tuple(header)
        self.write_next_row(self.header)

    def write_next_dict(self, row):
        self.write_next_row(row)

    def close(self):
        self._fh.close()