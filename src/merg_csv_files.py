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
    :return: the file content as a list of csv records
    '''
    year = re.search('.*(....).csv', csv_file).group(1)
    energy_type = 'None'
    if 'Gas' in csv_file:
        energy_type = 'Gas'
    elif 'Electricity' in csv_file:
        energy_type = 'Electricity'

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Append year and energy_type to the new csv
        for row in reader:
            row['year'] = year
            row['energy_type'] = energy_type
            result.append(dict(row))
    header = list(reader.fieldnames)
    header.append('year')
    header.append('energy_type')
    return result, header


def run(args):
    parser = argparse.ArgumentParser(description='Merge energy csv files into one.')
    parser.add_argument('-c', '--csvfiles', nargs='+', required=True, help='A list of csv files')
    args = parser.parse_args()
    result = list()
    for csvfile in args.csvfiles:
        result, field_names = open_csv_file(result, csvfile)
    header_form = ','.join(['{}' for i in range(len(field_names))])
    print(field_names)
    for row in sorted(result, key=lambda i: (i['year'], i['energy_type'])):
        out = row.values()
        print(header_form.format(*out))


if __name__ == '__main__':
    run(sys.argv)

