import shutil
from pathlib import Path

import adders
import modifiers
from diablo_reader import DiabloReader
from diablo_writer import DiabloWriter


def get_methods(package):
    return list(filter(lambda x: callable(x) and
                               not x.__name__.startswith('__') and
                               hasattr(x, '__module__') and
                               x.__module__ == package.__name__,
                       map(lambda x: getattr(package, x), dir(package))))


if __name__ == '__main__':
    modifiers_list = get_methods(modifiers)
    adders_list = get_methods(adders)
    templates = Path('templates')
    results = Path('results')
    excel = Path('D2RCasualSP').joinpath(Path('D2RCasualSP.mpq')).joinpath(Path('data')).joinpath(
        Path('global')).joinpath(Path('excel'))
    shutil.rmtree(results, ignore_errors=True)
    shutil.copytree(templates, results)
    for file in templates.joinpath(excel).iterdir():
        with open(file, mode='r', newline='') as template_file:
            with open(results.joinpath(excel).joinpath(file.name), mode='w', newline='') as result_file:
                reader = DiabloReader(template_file)
                writer = DiabloWriter(result_file, fieldnames=reader.fieldnames)
                writer.write_header()
                for row in reader:
                    for modifier in modifiers_list:
                        row = modifier(file.name, row)
                    writer.write_row(row)
                for adder in adders_list:
                    for row in adder(file.name):
                        writer.write_row(row)
