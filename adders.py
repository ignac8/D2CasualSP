def devolve_runes(filename):
    rows = list()
    if filename == 'cubemain.txt':
        for i in range(1, 34 - 1):
            row = dict()
            row['description'] = f'r{str(i)}'
            row['enabled'] = str(int(True))
            row['version'] = '0'
            row['numinputs'] = '2'
            row['input 1'] = f'r{str(i + 1).rjust(2, str(0))}'
            row['input 2'] = 'ibk'
            row['output'] = f'r{str(i).rjust(2, str(0))}'
            row['output b'] = f'r{str(i).rjust(2, str(0))}'
            rows.append(row)
    return rows


def prepare_for_runeword(filename):
    rows = list()
    if filename == 'cubemain.txt':
        row = dict()
        row['description'] = 'runeword ready weapon'
        row['enabled'] = str(int(True))
        row['version'] = '0'
        row['numinputs'] = '2'
        row['input 1'] = 'weap'
        row['input 2'] = 'ibk'
        row['output'] = 'usetype,nor'
        row['mod 1'] = 'sock'
        row['mod 1 min'] = str(1)
        row['mod 1 max'] = str(6)
        row['plvl'] = 50
        row['ilvl'] = 50
        rows.append(row)

        row = row.copy()
        row['description'] = 'runeword ready armor'
        row['input 1'] = 'armo'
        rows.append(row)
    return rows
