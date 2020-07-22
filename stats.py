#!/usr/bin/env python
# coding=utf-8

import click 
import glob
import datetime
import re
import csv
import calendar
from pathlib import Path

def get_date(filename):
  date = re.search('enjin_watch_(\d+)_', d).group(1)
  # return datetime.datetime.fromtimestamp(os.path.getctime(filename)).date()

def find_ent(res, strftime):
  for ent in res:
    if ent['date'] == strftime:
      return ent
  return None

CONFIRMED = 'Confirmed or Completed'

# datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

@click.command()
@click.option('--days', default=-21, type=int)
# @click.option('--days', default=1, type=int)
def stats(days):

  today_date = datetime.datetime.today().date()
  target_date = today_date + datetime.timedelta(days=days)

  mondays = []

  for single_date in daterange(target_date, today_date):
    if calendar.day_name[single_date.weekday()] == 'Monday':
      mondays.append(single_date)
  print('List of Modays...{}'.format(mondays))

  week_no_to_date = {}
  for monday in mondays:
    # week_nos.append(monday.strftime('%V'))
    week_no_to_date[monday.strftime('%V')] = monday

  log_path = '/'.join([str(Path.home()), 'wechaty-getting-started/log', 'cn_sup_*.csv']) 
  f_list = [ f_name for f_name in glob.iglob(log_path)]
  print('CN Sup list: {}'.format(f_list))

  # 逻辑重组
  f_dict = {}
  for monday in mondays:
    f_dict[monday.strftime('%V')] = []

  for f_name in f_list:
    # print('?')
    try:
      # date_m = re.search('cn_sup_(\d+-\d+-\d+)_', f_name).group(1)
      match = re.search(r'\d{4}-\d{2}-\d{2}', f_name)
      # print(match)
      f_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
      # print(f_date)
      # print(f_date.strftime('%V'))
    except AttributeError:
      print('Warning: fail to extract date from file name...')
      continue

    # if f_date < mondays[0]:
    #   break

    # f_date = (datetime.datetime.strptime(date_m, '%y%m%d')).date()
    try:
      f_dict[f_date.strftime('%V')].append(f_name)
    except KeyError:
      print('WARNING: KeyError...')

  print(f_dict)

  tag_dict_ent = { 'support/rma': 0, 'support/cma': 0, 'support/ema': 0,
    'support/tracking': 0, 'data_issue/tracking': 0,
    'support/callbacks':0, 'data_issue/callbacks': 0,
    'data_issue/credentials': 0, 'support/new_integration': 0,
    'support/data_exporter': 0, 'support/channel': 0, 'support/campaigns': 0, 'support/app': 0, 'support/metrics': 0, 
    'support/datavault': 0, 'support/query': 0,
    'other/on-boarding': 0, 'other': 0, 'other/partners': 0, 'other/gdpr': 0, 'agency': 0, 'ios14': 0, 'demo': 0, 'smallTalk': 0,
    'data_issue/spend': 0, 'data_issue/purchase': 0, 'data_issue/metrics': 0, 'data_issue/ad_revenue': 0, 'data_issue/data_delay': 0,
    'support/sdk': 0}

  # tag_dict
  # key: week_no value: []
  tag_dict = {}
  for monday in mondays:
    tag_dict[monday.strftime('%V')] = tag_dict_ent.copy()

  # f_dict
  # key: week_no value: [f_name1, f_name2, f_name3...]
  res = []
  for week_no in f_dict.keys():
    ent = {}
    ent['date'] = 'Week of {}'.format(str(week_no_to_date[week_no]))
    ent['source'] = 'WeChat'
    ent['conversations'] = 0
    ent['conversation_time'] = 0
    ent['response_time'] = 0

    conversation_time = datetime.timedelta()
    response_time = datetime.timedelta()

    for f_name in f_dict[week_no]:
      with open(f_name, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
          start_date = datetime.datetime.strptime(row['started_at'], '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)')
          end_date = datetime.datetime.strptime(row['ended_at'], '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)')
          response_date = datetime.datetime.strptime(row['1st_responded_at'], '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)')
          response_time = response_time+(response_date-start_date)
          conversation_time = conversation_time+(end_date-start_date)
          # 计算不同tag事件数量
          if row['tag'] == None or row['tag'].lower() not in tag_dict_ent.keys():
            tag_dict[week_no]['other'] = tag_dict[week_no]['other'] + 1
          else:
            tag_dict[week_no][row['tag'].lower()] = tag_dict[week_no][row['tag'].lower()] + 1
      ent['conversations'] = ent['conversations']+1
    if ent['conversations'] != 0:
      ent['response_time'] = response_time/ent['conversations']
      ent['conversation_time'] = conversation_time/ent['conversations']
    res.append(ent)

  target_filename = '_'.join(['sup_stats', datetime.datetime.now().strftime('%y%m%d_%H%M')]) + \
            '.csv'

  keys = res[0].keys()
  with open(target_filename, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(res)

  print('New Supp Stats: {}'.format(target_filename))

  # 每一行是tag名称
  res2 = []
  for tag in tag_dict_ent.keys():
    ent = {}
    ent['tag'] = tag

    for week_no in week_no_to_date.keys():
      ent['Week of {}'.format(str(week_no_to_date[week_no]))] = tag_dict[week_no][tag]
    res2.append(ent)

  target_filename = '_'.join(['sup_tag_stats', datetime.datetime.now().strftime('%y%m%d_%H%M')]) + \
            '.csv'

  keys = res2[0].keys()
  with open(target_filename, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(res2)

  print('New Tag Stats: {}'.format(target_filename))

  # for key in f_dict.keys():
  #   ent = {}
  #   ent['date'] = 'Week of {}'.format(str(week_no_to_date[key]))
  #   ent['source'] = 'WeChat'
  #   ent['conversations'] = 0
  #   ent['conversation_time'] = 0
  #   ent['response_time'] = 0

  #   conversation_time = datetime.timedelta()
  #   response_time = datetime.timedelta()

  #   for f_name in f_dict[key]:
  #     with open(f_name, encoding='utf-8-sig') as csvfile:
  #       reader = csv.DictReader(csvfile)
  #       for row in reader:
  #         start_date = datetime.datetime.strptime(row['started_at'], '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)')
  #         end_date = datetime.datetime.strptime(row['ended_at'], '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)')
  #         response_date = datetime.datetime.strptime(row['1st_responded_at'], '%a %b %d %Y %H:%M:%S GMT+0800 (China Standard Time)')
  #         response_time = response_time+(response_date-start_date)
  #         conversation_time = conversation_time+(end_date-start_date)
  #     ent['conversations'] = ent['conversations']+1
  #   if ent['conversations'] != 0:
  #     ent['conversation_time'] = conversation_time/ent['conversations']
  #     ent['response_time'] = response_time/ent['conversations']
  #   res.append(ent)

  return

if __name__ == '__main__':
  stats()