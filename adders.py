def devolve_runes(filename):
    rows = list()
    if filename == 'cubemain.txt':
        for i in range(1, 34):
            row = dict()
            row['description'] = f'r{str(i)}'
            row['enabled'] = str(int(True))
            row['version'] = '100'
            row['numinputs'] = '2'
            row['input 1'] = f'r{str(i + 1).rjust(2, str(0))}'
            row['input 2'] = 'ibk'
            row['output'] = f'r{str(i).rjust(2, str(0))},qty=2'
            rows.append(row)
    return rows
