import csv
import os

if __name__ == '__main__':
    excel_dir = 'data/data/global/excel'
    templates_dir = 'templates'
    results_dir = 'results'
    for filename in os.listdir(f'{templates_dir}/{excel_dir}'):
        with open(f'{templates_dir}/{excel_dir}/{filename}', mode='r', newline='') as template_file:
            os.makedirs(f'{results_dir}/{excel_dir}', exist_ok=True)
            with open(f'{results_dir}/{excel_dir}/{filename}', mode='w', newline='') as result_file:
                reader = csv.DictReader(template_file, delimiter='\t', dialect="excel-tab", quoting=csv.QUOTE_NONE,
                                        quotechar=None)
                writer = csv.DictWriter(result_file, delimiter='\t', fieldnames=reader.fieldnames,
                                        dialect="excel-tab", quoting=csv.QUOTE_NONE, quotechar=None)
                writer.writeheader()
                for row in reader:
                    writer.writerow(row)
