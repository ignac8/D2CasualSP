import math
import re


def disable_no_drop(filename, row):
    if filename == 'treasureclassex.txt':
        if row['NoDrop']:
            row['NoDrop'] = int(False)
    return row


def more_common_drops(filename, row):
    if filename == 'itemratio.txt':
        for value in row.items():
            if value[0] == 'Unique' or value[0] == 'Rare' or value[0] == 'Set' or value[0] == 'Magic':
                row[value[0]] = math.ceil(int(value[1]) / 10)
    return row


def better_rune_drop(filename, row):
    if filename == 'treasureclassex.txt':
        if row['Treasure Class'].startswith('Runes'):
            for value in row.items():
                if value[1].isnumeric() and value[0].startswith('Prob'):
                    row[value[0]] = 1
    return row


def disable_ladder_only_cube_recipes(filename, row):
    if filename == 'cubemain.txt':
        if row['ladder'] and int(row['ladder']):
            row['ladder'] = int(False)
    return row


def disable_ladder_only_runewords(filename, row):
    if filename == 'runes.txt':
        if row['server'] and int(row['server']):
            row['server'] = int(False)
    return row


def disable_ladder_only_unique_items(filename, row):
    if filename == 'uniqueitems.txt':
        if row['ladder'] and int(row['ladder']):
            row['ladder'] = int(False)
    return row


def more_monsters(filename, row):
    if filename == 'levels.txt':
        if row['NumMon']:
            row['NumMon'] = 25
    return row


def more_monster_types(filename, row):
    if filename == 'levels.txt':
        for value in row.items():
            if value[0].startswith('MonDen') and value[1].isnumeric():
                row[value[0]] = int(int(value[1]) * 2)
    return row


def easier_rune_cubing(filename, row):
    if filename == 'cubemain.txt':
        match = re.match('r(\d{2})', row['output'])
        if match:
            for value in row.items():
                if value[0].startswith('input'):
                    row[value[0]] = ''
                row['numinputs'] = str(2)
                row['input 1'] = f'r{str(int(match.group(1)) - 1).rjust(2, str(0))},qty=2'
    return row


def easier_socketing(filename, row):
    if filename == 'cubemain.txt':
        if 'nor,nos' in row['input 1']:
            row['numinputs'] = str(2)
            row['input 2'] = 'ibk'
            row['input 3'] = ''
            row['input 4'] = ''
    return row


def more_champions(filename, row):
    if filename == 'levels.txt':
        for value in row.items():
            if value[0].startswith('MonUMax') and value[1].isnumeric():
                number = int(int(value[1]) * 2)
                row[value[0]] = number
                row[value[0].replace('Max', 'Min')] = number
    return row


def more_stats_per_level(filename, row):
    if filename == 'charstats.txt':
        if row['StatPerLevel']:
            row['StatPerLevel'] = int(int(row['StatPerLevel']) * 2)
    return row


def more_skills_per_level(filename, row):
    if filename == 'charstats.txt':
        if row['SkillsPerLevel']:
            row['SkillsPerLevel'] = int(int(row['SkillsPerLevel']) * 2)
    return row


def more_power(filename, row):
    if filename == 'charstats.txt':
        if row['ManaRegen']:
            row['ManaRegen'] = int(int(row['ManaRegen']) / 2)
    return row


def higher_selling_price(filename, row):
    if filename == 'npc.txt':
        for value in row.items():
            if value[0].startswith('max buy'):
                row[value[0]] = int(int(value[1]) * 10)
    return row


def better_gambling(filename, row):
    if filename == 'difficultylevels.txt':
        max_chance = 100000
        row['GambleRare'] = int(max_chance / 2)
        row['GambleSet'] = int(max_chance / 5)
        row['GambleUnique'] = int(max_chance / 10)
        row['GambleUber'] = int(row['GambleUber']) * 10
        row['GambleUltra'] = int(row['GambleUltra']) * 10
    return row


def better_shrines(filename, row):
    if filename == 'shrines.txt':
        if row['Duration in frames']:
            row['Duration in frames'] = int(int(row['Duration in frames']) * 10)
    return row


def no_experience_penalty(filename, row):
    if filename == 'experience.txt':
        row['ExpRatio'] = 1024
    return row
