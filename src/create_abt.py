#!/usr/bin/env python3

import argparse
import sys
import csv
import matplotlib.pyplot as plt
from matplotlib import interactive
from collections import defaultdict

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


def create_abt(result):
    '''
    Gather the data from the provided csv file
    :param result: the csv file that contains the energy consumptions
    :return: four lists with dict's: total consumption for gas and energy and percentage smart consumption
    '''
    num_connections = defaultdict(int)
    type_of_connection = defaultdict(int)
    for instance in result:
        num_connections[instance['num_connections']] += 1
        type_of_connection[instance['type_of_connection']] += 1
        print('{},{},{}'.format(instance['num_connections'],
                                instance['type_of_connection'],
                                instance['annual_consume']))
    print(dict(type_of_connection))
    print(sorted(dict(num_connections)))


def run(args):
    '''
    main function
    :param args: the argument list
    :return: nothing
    '''
    parser = argparse.ArgumentParser(description='Creates a csv with top cities consumption.')
    parser.add_argument('-c', '--csvfile', type=str, required=True, help='The input csv file to read')

    args = parser.parse_args()
    result = open_csv_file(args.csvfile)
    create_abt(result)


if __name__ == '__main__':
    run(sys.argv)

