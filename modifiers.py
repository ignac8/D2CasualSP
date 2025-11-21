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


def equal_rune_drop(filename, row):
    if filename == 'treasureclassex.txt':
        tc_name = row.get('Treasure Class', '')
        if tc_name.startswith('Runes '):
            tier_str = tc_name.replace('Runes ', '')
            if tier_str.isdigit():
                tier = int(tier_str)
                if tier == 1:
                    row['Item1'] = 'r01'
                    row['Prob1'] = '1'
                    row['Item2'] = 'r02'
                    row['Prob2'] = '1'
                elif tier <= 16:
                    row['Item1'] = f'r{str(2*tier - 1).zfill(2)}'
                    row['Prob1'] = '1'
                    row['Item2'] = f'r{str(2*tier).zfill(2)}'
                    row['Prob2'] = '1'
                    row['Item3'] = f'Runes {tier - 1}'
                    row['Prob3'] = str(2 * (tier - 1))
                elif tier == 17:
                    row['Item1'] = 'r33'
                    row['Prob1'] = '1'
                    row['Item2'] = 'Runes 16'
                    row['Prob2'] = '32'
    return row


def disable_ladder_only(_, row):
    row['firstLadderSeason'] = ''
    row['lastLadderSeason'] = ''
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
        match = re.match('r(\\d{2})', row['output'])
        if match:
            for value in row.items():
                if value[0].startswith('input'):
                    row[value[0]] = ''
                row['numinputs'] = str(2)
                row['input 1'] = f'r{str(int(match.group(1)) - 1).rjust(2, str(0))},qty=2'
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
            row['ManaRegen'] = int(int(row['ManaRegen']) / 10)
        if row['WalkVelocity']:
            row['WalkVelocity'] = int(int(row['WalkVelocity']) * 1.25)
        if row['RunVelocity']:
            row['RunVelocity'] = int(int(row['RunVelocity']) * 1.25)
        if row['RunDrain']:
            row['RunDrain'] = int(int(row['RunDrain']) / 2)
        if row['LightRadius']:
            row['LightRadius'] = int(int(row['LightRadius']) * 2)
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
        row['GambleSet'] = int(max_chance / 10)
        row['GambleUnique'] = int(max_chance / 5)
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


def max_stats_unique_items(filename, row):
    if filename == 'uniqueitems.txt':
        for i in range(1, 13):
            max_field = f'max{i}'
            min_field = f'min{i}'
            if max_field in row and row[max_field]:
                row[min_field] = row[max_field]
    return row


def max_stats_set_items(filename, row):
    if filename == 'setitems.txt':
        for i in range(1, 10):
            max_field = f'max{i}'
            min_field = f'min{i}'
            if max_field in row and row[max_field]:
                row[min_field] = row[max_field]
        for i in range(1, 6):
            for suffix in ['a', 'b']:
                max_field = f'amax{i}{suffix}'
                min_field = f'amin{i}{suffix}'
                if max_field in row and row[max_field]:
                    row[min_field] = row[max_field]
    return row


def max_stats_magic_affixes(filename, row):
    if filename in ['magicprefix.txt', 'magicsuffix.txt']:
        for i in range(1, 4):
            max_field = f'mod{i}max'
            min_field = f'mod{i}min'
            if max_field in row and row[max_field]:
                row[min_field] = row[max_field]
    return row
