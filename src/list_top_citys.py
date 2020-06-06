#!/usr/bin/env python3

import argparse
import sys
import csv
from collections import defaultdict

# net_manager,purchase_area,street,zipcode_from,zipcode_to,city,delivery_perc,num_connections,perc_of_active_connections,
# type_conn_perc,type_of_connection,annual_consume,annual_consume_lowtarif_perc,smartmeter_perc
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


# net_manager,purchase_area,street,zipcode_from,zipcode_to,city,delivery_perc,num_connections,\
# perc_of_active_connections,type_conn_perc,type_of_connection,annual_consume,\
# annual_consume_lowtarif_perc,smartmeter_perc,year,energy_type
def print_result(result, data_type, energy, number):
    cities = defaultdict(int)
    for row in result:
        if row['energy_type'] == energy:
            cities[row['city']] += float(row[data_type] + '0')
    top_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
    print('City,Consume')
    for idx, city in enumerate(top_cities):
        print('{},{}'.format(city[0], city[1]))
        if idx > number:
            break


def check_input(args):
    if args.type == 'a':
        data_type = 'annual_consume'
    elif args.type == 's':
        data_type = 'smartmeter_perc'
    else:
        print("Invalid type:" + type)
        exit(2)
    if args.energy == 'e':
        energy = 'Electricity'
    elif args.energy == 'g':
        energy= 'Gas'
    else:
        print("Invalid type:" + type)
        exit(2)

    return data_type, energy
def run(args):
    parser = argparse.ArgumentParser(description='Creates a csv with top cities consumption.')
    parser.add_argument('-c', '--csvfile', type=str, required=True, help='The input csv file to read')
    parser.add_argument('-t', '--type', type=str, required=True, help='a (annual_consume) or s (smartmeter_perc)')
    parser.add_argument('-e', '--energy', type=str, required=True, help='e (electricity) or g (gas)')
    parser.add_argument('-n', '--number', type=int, default=10, help='How many top to view')

    args = parser.parse_args()
    data_type, energy = check_input(args)
    result = open_csv_file(args.csvfile)
    print_result(result, data_type, energy, args.number)


if __name__ == '__main__':
    run(sys.argv)

