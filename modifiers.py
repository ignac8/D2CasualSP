import csv
import math
import os


def disable_no_drop(filename, row):
    if filename == 'treasureclassex.txt':
        if row['NoDrop']:
            row['NoDrop'] = int(False)
    return row


def more_common_drops(filename, row):
    if filename == 'itemratio.txt':
        for value in row.items():
            if value[0] == "Unique" or value[0] == "Rare" or value[0] == "Set" or value[0] == "Magic":
                row[value[0]] = math.ceil(int(value[1]) / 10)
    return row


def better_rune_drop(filename, row):
    if filename == 'treasureclassex.txt':
        if row['Treasure Class'].startswith('Runes'):
            for value in row.items():
                if value[1].isnumeric() and value[0].startswith("Prob"):
                    row[value[0]] = 1
    return row


def disable_ladder_only(filename, row):
    if filename == 'cubemain.txt':
        if row['ladder'] and int(row['ladder']):
            row['ladder'] = int(False)
    if filename == 'runes.txt':
        if row['server'] and int(row['server']):
            row['server'] = int(False)
    if filename == 'uniqueitems.txt':
        if row['ladder'] and int(row['ladder']):
            row['ladder'] = int(False)
    return row


def more_monsters(filename, row):
    if filename == 'levels.txt':
        for value in row.items():
            if value[0].startswith('MonDen') and value[1].isnumeric():
                row[value[0]] = int(int(value[1]) * 2)
    return row


def more_power(filename, row):
    if filename == 'charstats.txt':
        if row['StatPerLevel']:
            row['StatPerLevel'] = int(int(row['StatPerLevel']) * 2)
        if row['SkillsPerLevel']:
            row['SkillsPerLevel'] = int(int(row['SkillsPerLevel']) * 2)
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
        row['GambleRare'] = int(100000 / 2)
        row['GambleSet'] = int(100000 / 10)
        row['GambleUnique'] = int(100000 / 20)
    return row


def better_shrines(filename, row):
    if filename == 'shrines.txt':
        if row['Duration in frames']:
            row['Duration in frames'] = int(int(row['Duration in frames']) * 10)
    return row
