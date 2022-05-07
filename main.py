import csv
import shutil
from pathlib import Path

import modifiers


def main():
    modifiers_list = list(filter(lambda x: callable(x) and not (x.__name__.startswith('__')),
                                 map(lambda x: getattr(modifiers, x), dir(modifiers))))
    templates = Path('templates')
    results = Path('results')
    excel = Path('D2RCasualSP').joinpath(Path('D2RCasualSP.mpq')).joinpath(Path('data')).joinpath(
        Path('global')).joinpath(Path('excel'))

    shutil.rmtree(results, ignore_errors=True)
    shutil.copytree(templates, results)

    for file in templates.joinpath(excel).iterdir():
        with open(file, mode='r', newline='') as template_file:
            with open(results.joinpath(excel).joinpath(file.name), mode='w', newline='') as result_file:
                reader = csv.DictReader(template_file, delimiter='\t', dialect='excel-tab', quoting=csv.QUOTE_NONE,
                                        quotechar=None)
                writer = csv.DictWriter(result_file, delimiter='\t', fieldnames=reader.fieldnames,
                                        dialect='excel-tab', quoting=csv.QUOTE_NONE, quotechar=None)
                writer.writeheader()
                for row in reader:
                    for modifier in modifiers_list:
                        row = modifier(file.name, row)
                    writer.writerow(row)


if __name__ == '__main__':
    main()
