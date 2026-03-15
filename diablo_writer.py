from escape_utils import escape


class DiabloWriter:
    def __init__(self, file, fieldnames):
        self.file = file
        self.fieldnames = fieldnames

    def write_header(self):
        line = '\t'.join(map(escape, self.fieldnames)) + '\r\n'
        self.file.write(line)

    def write_row(self, row):
        line = '\t'.join(escape(row.get(key, '')) for key in self.fieldnames) + '\r\n'
        self.file.write(line)
