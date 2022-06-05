import re

from escape_utils import unescape


class DiabloReader:
    def __init__(self, file):
        self.file = file
        self.fieldnames = self._readline()

    def __iter__(self):
        return self

    def __next__(self):
        line = self._readline()
        if line:
            return dict(zip(self.fieldnames, line))
        else:
            raise StopIteration

    def _readline(self):
        line = self.file.readline()
        if line:
            return list(map(unescape, re.split('\t', line)))
        else:
            return []
