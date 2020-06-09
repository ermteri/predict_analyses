#!/usr/bin/env python3

import argparse
import sys
import csv
import re

# net_manager,purchase_area,street,zipcode_from,zipcode_to,city,delivery_perc,num_connections,perc_of_active_connections,
# type_conn_perc,type_of_connection,annual_consume,annual_consume_lowtarif_perc,smartmeter_perc
def open_csv_file(result, csv_file):
    '''
    :param csv_file: the file to open
    :return: the file content as a list of dicts
    '''
    year = re.search('.*(....).csv', csv_file).group(1)
    energy_type = 'None'
    if 'Gas' in csv_file:
        energy_type = 'Gas'
    elif 'Electricity' in csv_file:
        energy_type = 'Electricity'
    provider = csv_file.split('_')[0].split('/')[-1]

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Append year and energy_type to the new csv
        for row in reader:
            row['provider'] = provider
            row['year'] = year
            row['energy_type'] = energy_type
            result.append(dict(row))

    return result


def print_result(result):
    '''
    Prints the result as a csv on stdout sorted on year and energy_type
    :param result: The data as a list of dict's
    :return: Nothing
    '''
    fieldnames = result[0].keys()
    years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    # for row in sorted(result, key=lambda i: (i['year'], i['energy_type'])):
    for row in result:
        if row['year'] in years:
            writer.writerow(row)


def run(args):
    parser = argparse.ArgumentParser(description='Merge energy csv files into one.')
    parser.add_argument('-c', '--csvfiles', nargs='+', required=True, help='A list of csv files')
    args = parser.parse_args()
    result = list()
    for csvfile in args.csvfiles:
        result = open_csv_file(result, csvfile)
    print_result(result)


if __name__ == '__main__':
    run(sys.argv)

