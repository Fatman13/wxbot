#!/usr/bin/env python
# coding=utf-8

import click 
import glob
import datetime
import re
import csv
import calendar
from pathlib import Path

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

@click.command()
# @click.option('--column1', default='ip_address_duplicate_column_name_1')
# @click.option('--column2', default='ip_address')
@click.option('--column1', default='advertising_id_duplicate_column_name_1')
@click.option('--column2', default='advertising_id')
@click.option('--file', default='cn_supp_misc-hk_stellar_organic_install_idfv_2-b41edf56a8b1-2020-07-17-08-39-35.csv')
# @click.option('--days', default=1, type=int)
def dup_count(column1, column2, file):

  columns = ['acquired_at', 'advertising_id_duplicate_column_name_1',
    'developer_device_id_duplicate_column_name_1', 'country',
    'app_version', 'device', 'ip_address_duplicate_column_name_1',
    'advertising_id', 'developer_device_id', 'ip_address']

  countries = set()
  by_countries = {}
  ips = set()
  by_ips = {}
  idfas = set()
  by_idfas = {}
  res2 = []
  with open(file, encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      idfa = row['advertising_id_duplicate_column_name_1'] 
      if idfa in idfas:
        by_idfas[idfa] = by_idfas[idfa] + 1
      else:
        by_idfas[idfa] = 1
        idfas.add(idfa)

  print(by_idfas)

  with open(file, encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      idfa = row['advertising_id_duplicate_column_name_1']
      if by_idfas[idfa] > 50:
        # print('We have {}'.format(idfa))
        ent = {}
        for column in columns:
          ent[column] = row[column]
        res2.append(ent)

  target_filename = '_'.join(['dup_count', datetime.datetime.now().strftime('%y%m%d_%H%M')]) + \
            '.csv'

  keys = res2[0].keys()
  with open(target_filename, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(res2)

  print('Finding dups: {}'.format(target_filename))

  return

if __name__ == '__main__':
  dup_count()