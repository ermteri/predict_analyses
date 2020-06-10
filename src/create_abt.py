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


def show_hist(data, title):
    a = np.hstack(data)
    _ = plt.hist(a, bins='auto')  # arguments are passed to np.histogram
    plt.title('Histogram for '+ title)
    plt.show()


def create_abt(result):
    '''
    Gather the data from the provided csv file
    :param result: the csv file that contains the energy consumptions
    :return: four lists with dict's: total consumption for gas and energy and percentage smart consumption
    '''
    num_connections_el = list()
    num_connections_el_high = list()
    num_connections_gas = list()
    num_connections_gas_high = list()
    type_of_connection = defaultdict(int)
    annual_consume_el = list()
    annual_consume_gas = list()
    for instance in result:
        try:
            if instance['energy_type'] == 'Electricity':
                num_connections_el.append(int(instance['num_connections']))
                if int(instance['num_connections']) > 200:
                    num_connections_el_high.append(int(instance['num_connections']))
                annual_consume_el.append(float(instance['annual_consume']))
            if instance['energy_type'] == 'Gas':
                num_connections_gas.append(int(instance['num_connections']))
                if int(instance['num_connections']) > 200:
                    num_connections_gas_high.append(int(instance['num_connections']))
                annual_consume_gas.append(float(instance['annual_consume']))
            type_of_connection[instance['type_of_connection']] += 1
        except Exception as e:
            print(instance, e)
        print('energy_type,num_connections,type_of_connection,annual_consume')
        print('{},{},{},{}'.format(instance['energy_type'],
                                   instance['num_connections'],
                                   instance['type_of_connection'],
                                   instance['annual_consume']))
    print('Number of connections descriptive variable, Electricity:')
    print('========================================================')
    print('Min:', min(num_connections_el))
    print('Max:', max(num_connections_el))
    print('Mean:', mean(num_connections_el))
    print('Median:', median(num_connections_el))
    # print('>100', num_connections_el_high)
    show_hist(num_connections_el_high, 'Electricity')

    print('Number of connections descriptive variable, Gas:')
    print('================================================')
    print('Min:', min(num_connections_gas))
    print('Max:', max(num_connections_gas))
    print('Mean:', mean(num_connections_gas))
    print('Median:', median(num_connections_gas))
    # print('>100', num_connections_gas_high)
    show_hist(num_connections_gas_high, 'Gas')

    print('Type of connection descriptive variable')
    print('=======================================')
    for type in sorted(type_of_connection):
        print('{} ({})'.format(type, type_of_connection[type]))

    print('Annual consumption target variable, Electricity')
    print('===============================================')
    print('Min:', min(annual_consume_el))
    print('Max:', max(annual_consume_el))
    print('Mean:', mean(annual_consume_el))
    print('Median:', median(annual_consume_el))
    show_hist(annual_consume_el, 'Electricity')

    print('Annual consumption target variable, Gas')
    print('=======================================')
    print('Min:', min(annual_consume_gas))
    print('Max:', max(annual_consume_gas))
    print('Mean:', mean(annual_consume_gas))
    print('Median:', median(annual_consume_gas))
    show_hist(annual_consume_gas, 'Electricity')


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

