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


def plot_result(result, div, title, number):
    '''
    Plots the diagrams based on the result parameter
    :param result: A list of dict's that contains the data
    :param div: how much each data point should be divided with
    :param title: the title of the diagram
    :param number: how many top cities should be displayed
    :return: nothing
    '''
    x = list()
    y = list()
    top_cities = sorted(result.items(), key=lambda x: x[1], reverse=True)[0:number]

    for row in top_cities:
        x.append(row[0])
        y.append(row[1]/div)
    fig, y_ax = plt.subplots()
    bar_color = 'tab:blue'
    y_ax.set_xlabel('Top ' + str(number) + " cities")
    y_ax.bar(x, y, color=bar_color, width=0.8)
    y_ax.tick_params(axis='y', labelcolor=bar_color)
    plt.xticks(rotation=60, ha='right')
    y_ax.tick_params(axis='x', labelsize=8)
    y_ax.tick_params(axis='y', labelsize=8)
    plt.title(title)
    fig.tight_layout()


def gather_data(result):
    '''
    Gather the data from the provided csv file
    :param result: the csv file that contains the energy consumptions
    :return: four lists with dict's: total consumption for gas and energy and percentage smart consumption
    '''
    cities_annual_electricity = defaultdict(float)
    cities_annual_gas = defaultdict(float)
    cities_smart_electricity = defaultdict(float)
    cities_smart_gas = defaultdict(float)
    cities_smart_perc_electricity = defaultdict(float)
    cities_smart_perc_gas = defaultdict(float)

    for row in result:
        if row['energy_type'] == 'Electricity':
            cities_annual_electricity[row['city']] += float(row['annual_consume'] + '0')
            cities_smart_electricity[row['city']] += (float(row['annual_consume'] + '0') * float(row['smartmeter_perc'] + '0')) / 100
        elif row['energy_type'] == 'Gas':
            cities_annual_gas[row['city']] += float(row['annual_consume'] + '0')
            cities_smart_gas[row['city']] += (float(row['annual_consume'] + '0') * float(row['smartmeter_perc'] + '0')) / 100
    for city in cities_smart_electricity:
        cities_smart_perc_electricity[city] = cities_smart_electricity[city]/cities_annual_electricity[city] * 100
    for city in cities_smart_gas:
        cities_smart_perc_gas[city] = cities_smart_gas[city]/cities_annual_gas[city] * 100
    return cities_annual_electricity, cities_annual_gas, cities_smart_perc_electricity, cities_smart_perc_gas


def run(args):
    '''
    main function
    :param args: the argument list
    :return: nothing
    '''
    parser = argparse.ArgumentParser(description='Creates a csv with top cities consumption.')
    parser.add_argument('-c', '--csvfile', type=str, required=True, help='The input csv file to read')
    parser.add_argument('-n', '--number', type=int, default=10, help='How many top to view')

    args = parser.parse_args()
    result = open_csv_file(args.csvfile)
    annual_el, annual_gas, smart_el, smart_gas = gather_data(result)
    plot_result(annual_el, div=1000000, title='Electrical Energy consumption 2010-2018 (GWh)', number=args.number)
    interactive(True)
    plt.show()
    plot_result(annual_gas, div=1000000, title='Gas Energy consumption 2010-2018 (million m3)', number=args.number)
    plt.show()
    plot_result(smart_el, div=1, title='Smart Electrical Energy consumption 2010-2018 (%)', number=args.number)
    plt.show()
    plot_result(smart_gas, div=1, title='Smart Gas Energy consumption 2010-2018 (%)', number=args.number)
    interactive(False)
    plt.show()


if __name__ == '__main__':
    run(sys.argv)

