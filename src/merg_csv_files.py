#!/usr/bin/env python3

import argparse
import sys
import csv
import re


def open_csv_file(result, csv_file):
    '''
    :param csv_file: the file to open
    :return: the file content as a list of csv records
    '''
    year = re.search('.*(....).csv', csv_file).group(1)
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['year'] = year
            result.append(row)
    return result


def run(args):
    parser = argparse.ArgumentParser(description='Merge energy csv files into one.')
    parser.add_argument('-c', '--csvfiles', nargs='+', required=True, help='A list of csv files')
    args = parser.parse_args()
    result = list()
    for csvfile in args.csvfiles:
        open_csv_file(result, csvfile)
    for row in result:
        print(row['year'],row['annual_consume'])


if __name__ == '__main__':
    run(sys.argv)

