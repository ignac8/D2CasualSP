import csv
import os


def disable_no_drop(filename, row):
    if filename == 'treasureclassex.txt':
        if row['NoDrop']:
            row['NoDrop'] = 0
    return row


def more_common_drops(filename, row):
    if filename == 'itemratio.txt':
        for value in row.items():
            if value[1].isnumeric() and int(value[1]) and not (value[0].endswith("Divisor")) and not (
            value[0].endswith("Min")):
                row[value[0]] = int(int(value[1]) / 10)
    return row


def better_rune_drop(filename, row):
    pass


def disable_ladder_only(filename, row):
    pass


def more_monsters(filename, row):
    pass
