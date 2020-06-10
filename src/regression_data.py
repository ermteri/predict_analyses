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


def gather_data(result):
    el_annual_consumption = defaultdict(float)
    gas_annual_consumption = defaultdict(float)
    for row in result:
        if row['energy_type'] == 'Electricity':
            el_annual_consumption[row['year']] += float(row['annual_consume'])
        if row['energy_type'] == 'Gas':
            gas_annual_consumption[row['year']] += float(row['annual_consume'])

    return el_annual_consumption, gas_annual_consumption


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
    el_consumption, gas_consumption = gather_data(result)
    print('Year,Electricity consumption,Gas consumption')
    for row in sorted(el_consumption):
        print('{},{},{}'.format(row, el_consumption[row]/1000000, gas_consumption[row]/1000000))


if __name__ == '__main__':
    run(sys.argv)

