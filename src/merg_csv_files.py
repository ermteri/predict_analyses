#!/usr/bin/env python3

import argparse
import sys
import csv
import re


def open_csv_file(csv_file):
    '''
    :param csv_file: the file to open
    :return: the file content as a list of csv records
    '''
    result = list()
    year = re.search('.*(....).csv', csv_file).group(1)
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['year'] = year
            result.append(row)
    return result


def run(args):
    parser = argparse.ArgumentParser(description='Merge energy csv files into one.')
    parser.add_argument('-c', '--csvfile', type=str, required=True, help='A csv file')
    args = parser.parse_args()
    result = open_csv_file(args.csvfile)
    for row in result:
        print(row)


if __name__ == '__main__':
    run(sys.argv)

