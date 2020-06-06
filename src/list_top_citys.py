#!/usr/bin/env python3

import argparse
import sys
import csv
import matplotlib.pyplot as plt
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


def plot_result(result, number, energy):
    x = list()
    y = list()
    if energy == 'Electricity':
        div = 1000000
        energy = 'Electrical'
        unit = 'GWh'
    else:
        div = 1000000
        energy = 'Gas'
        unit = 'Million m3'
    for idx, row in enumerate(result):
        x.append(row[0])
        y.append(row[1]/div)
        if idx > number:
            break
    fig, y_ax = plt.subplots()
    bar_color = 'tab:blue'
    y_ax.set_xlabel('Top ' + str(number) + " cities")
    y_ax.bar(x, y, color=bar_color, width=0.8)
    y_ax.tick_params(axis='y', labelcolor=bar_color)
    plt.xticks(rotation=60, ha='right')
    y_ax.tick_params(axis='x', labelsize=8)
    y_ax.tick_params(axis='y', labelsize=8)
    plt.title('{} Energy consumption 2010-2018 ({})'.format(energy, unit))
    fig.tight_layout()
    plt.show()


def show_result(result, data_type, energy, number):
    cities = defaultdict(int)
    n = 1
    for row in result:
        if row['energy_type'] == energy:
            if data_type == 'annual_consume':
                cities[row['city']] += float(row[data_type] + '0')
            else:
                cities[row['city']] += (float(row[data_type] + '0') - cities[row['city']]) / n;
                n += 1
    top_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
    print('City,Consume')
    plot_result(top_cities, number, energy)
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
    show_result(result, data_type, energy, args.number)


if __name__ == '__main__':
    run(sys.argv)

