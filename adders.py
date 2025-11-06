from pathlib import Path
from diablo_reader import DiabloReader


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


def add_missing_gamble_items(filename):
    rows = list()
    if filename == 'gamble.txt':
        # Get the templates directory path
        templates_dir = Path('templates')
        excel_path = templates_dir.joinpath('D2RCasualSP').joinpath('D2RCasualSP.mpq').joinpath('data').joinpath('global').joinpath('excel')

        # Read existing gamble items to avoid duplicates
        existing_codes = set()
        gamble_path = excel_path.joinpath('gamble.txt')
        with open(gamble_path, mode='r', newline='') as gamble_file:
            reader = DiabloReader(gamble_file)
            for row in reader:
                if row.get('code'):
                    existing_codes.add(row['code'])

        # Read all weapons
        weapons_path = excel_path.joinpath('weapons.txt')
        with open(weapons_path, mode='r', newline='') as weapons_file:
            reader = DiabloReader(weapons_file)
            for row in reader:
                code = row.get('code', '')
                rarity = row.get('rarity', '')
                name = row.get('name', '')
                # Skip if code is empty, already in gamble, or has null rarity (quest items/potions/markers)
                if code and code not in existing_codes and rarity:
                    rows.append({'name': name, 'code': code})

        # Read all armor
        armor_path = excel_path.joinpath('armor.txt')
        with open(armor_path, mode='r', newline='') as armor_file:
            reader = DiabloReader(armor_file)
            for row in reader:
                code = row.get('code', '')
                rarity = row.get('rarity', '')
                name = row.get('name', '')
                # Skip if code is empty, already in gamble, or has null rarity (quest items)
                if code and code not in existing_codes and rarity:
                    rows.append({'name': name, 'code': code})

    return rows
