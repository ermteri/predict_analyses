#!/usr/bin/env python3

import argparse
import sys
import csv
from statistics import mean, median
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib import interactive
import numpy as np

# The fields in the csv that contains the data
# net_manager,purchase_area,street,zipcode_from,zipcode_to,city,delivery_perc,num_connections,perc_of_active_connections,
# type_conn_perc,type_of_connection,annual_consume,annual_consume_lowtarif_perc,smartmeter_perc, year, energy_type
def open_csv_file(csv_file):
    '''
    :param csv_file: the file to open
    :return: the file content as a list of dicts
    '''
    with open(csv_file, newline='') as csvfile:
        result = list()
        reader = csv.DictReader(csvfile)
        # Append year and energy_type to the new csv
        for row in reader:
            result.append(dict(row))
    return result


def remove_noise(result):
    fieldnames = result[0].keys()
    years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    # for row in sorted(result, key=lambda i: (i['year'], i['energy_type'])):
    for row in result:
        if row['type_of_connection'] == '' or row['type_of_connection'] == 'OBK':
            continue
        row['type_of_connection'] = row['type_of_connection'].replace('X', 'x')
        writer.writerow(row)


def run(args):
    '''
    main function
    :param args: the argument list
    :return: nothing
    '''
    parser = argparse.ArgumentParser(description='Reduces noise from the data set.')
    parser.add_argument('-c', '--csvfile', type=str, required=True, help='The input csv file to read')

    args = parser.parse_args()
    result = open_csv_file(args.csvfile)
    remove_noise(result)


if __name__ == '__main__':
    run(sys.argv)

