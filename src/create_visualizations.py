#!/usr/bin/env python3

import argparse
import sys
import csv
import matplotlib.pyplot as plt
from matplotlib import interactive
from collections import defaultdict

# The fields in the csv that contains the data:
# net_manager,purchase_area,street,zipcode_from,zipcode_to,city,delivery_perc,num_connections,
# perc_of_active_connections, type_conn_perc,type_of_connection,annual_consume,annual_consume_lowtarif_perc,
# smartmeter_perc,provider,year, energy_type
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


def plot_result(result, div, title, number, aggregate):
    '''
    Plots the diagrams based on the result parameter
    :param result: A list of dict's that contains the data
    :param div: how much each data point should be divided with
    :param title: the title of the diagram
    :param number: how many top cities should be displayed
    :param aggregate: kind of aggregate
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
    y_ax.set_xlabel(aggregate)
    y_ax.bar(x, y, color=bar_color, width=0.8)
    y_ax.tick_params(axis='y', labelcolor=bar_color)
    plt.xticks(rotation=60, ha='right')
    y_ax.tick_params(axis='x', labelsize=8)
    y_ax.tick_params(axis='y', labelsize=8)
    plt.title(title)
    fig.tight_layout()


def gather_data(result, aggregate_field, compare_field):
    '''
    Gather the data from the provided csv file
    :param result: the csv file that contains the energy consumptions
    :param aggregate_field: the field to aggregate on
    :param compare_field: the field used to compare to the annual_consume
    :return: four lists with dict's: total consumption for gas and energy and percentage the compare field consumption
    '''
    annual_electricity = defaultdict(float)
    annual_gas = defaultdict(float)
    compare_electricity = defaultdict(float)
    compare_gas = defaultdict(float)
    compare_perc_electricity = defaultdict(float)
    compare_perc_gas = defaultdict(float)

    for row in result:
        try:
            if row['energy_type'] == 'Electricity':
                annual_electricity[row[aggregate_field]] += float(row['annual_consume'])
                # Percentage number must not be > 100
                if float(row[compare_field]) <= 100:
                    compare_electricity[row[aggregate_field]] += (float(row['annual_consume']) *
                                                                  float(row[compare_field]) / 100)
            elif row['energy_type'] == 'Gas':
                annual_gas[row[aggregate_field]] += float(row['annual_consume'])
                if float(row[compare_field]) <= 100:
                    compare_gas[row[aggregate_field]] += (float(row['annual_consume']) *
                                                          float(row[compare_field])) / 100
        except Exception as e:
            pass
    for row in compare_electricity:
        compare_perc_electricity[row] = compare_electricity[row]/annual_electricity[row] * 100
    for row in compare_gas:
        compare_perc_gas[row] = compare_gas[row]/annual_gas[row] * 100
    return annual_electricity, annual_gas, compare_perc_electricity, compare_perc_gas


def run(args):
    '''
    main function
    :param args: the argument list
    :return: nothing
    '''
    parser = argparse.ArgumentParser(description='Creates visualizations of the input file.')
    parser.add_argument('-c', '--csvfile', type=str, required=True, help='The input csv file to read.')
    parser.add_argument('-a', '--aggregate', type=str, help='What to aggregate on, city or provider.')
    parser.add_argument('-n', '--number', type=int, default=10, help='How many top to view.')

    args = parser.parse_args()
    result = open_csv_file(args.csvfile)
    if args.aggregate == 'city':
        annual_el, annual_gas, smart_el, smart_gas = gather_data(result, 'city', 'smartmeter_perc')
        plot_result(annual_el, div=1000000, title='Electrical Energy consumption 2010-2018 (GWh)',
                    number=args.number, aggregate='City')
        interactive(True)
        plt.show()
        plot_result(annual_gas, div=1000000, title='Gas Energy consumption 2010-2018 (million m3)',
                    number=args.number, aggregate='City')
        plt.show()
        plot_result(smart_el, div=1, title='Electricity smart meter usage 2010-2018 (%)',
                    number=args.number, aggregate='City')
        plt.show()
        plot_result(smart_gas, div=1, title='Gas smart meter usage 2010-2018 (%)',
                    number=args.number, aggregate='City')
        interactive(False)
        plt.show()
    else:
        annual_el, annual_gas, lowtariff_el, lowtariff_gas = gather_data(result, 'provider',
                                                                         'annual_consume_lowtarif_perc')
        plot_result(lowtariff_el, div=1, title='Low tariff Electrical Energy consumption 2010-2018 (%)',
                    number=args.number, aggregate='Provider')
        interactive(True)
        plt.show()
        plot_result(lowtariff_gas, div=1, title='Low tariff Gas Energy consumption 2010-2018 (%)',
                    number=args.number, aggregate='Provider')
        interactive(False)
        plt.show()


if __name__ == '__main__':
    run(sys.argv)

