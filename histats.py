#!/usr/bin/env python
# coding=utf-8

# import pprint
import csv
import click 
# import requests
import datetime as datetime
# from bs4 import BeautifulSoup
# from splinter import Browser
import time
# import re
# import copy
import os
import json
# import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotVisibleException   
from selenium.common.exceptions import StaleElementReferenceException   
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
# from requests.exceptions import ConnectionError
# from requests.exceptions import ChunkedEncodingError
# from requests.exceptions import ReadTimeout
# from selenium.webdriver import ChromeOptions

SCROLL_PAUSE_TIME = 3

histats_url = 'https://www.tenjin.com/dashboard/admin/historical_stats_requests/new'

san = ['tiktok']
non_san = ['mobvista']

@click.command()
# @click.option('--org', default='db8417df-3379-45a4-a684-376923e19c58')
# @click.option('--u', default='867ab46b-4106-49b8-ab73-b642421a4406')
@click.option('--u', default='kwalee')
# tiktok, mobvista
@click.option('--ch', default='tiktok')
@click.option('--d_from', default='2020-06-01')
@click.option('--d_to', default='2020-06-30')
# @click.option('--days', default=1, type=int)
# @click.option('--session_id', default='2171486e6c13b61ad78b34a59f337ab0')
# def collector(secrets, url, session_id):
def histats(u, ch, d_from, d_to):
  with open('secrets.json') as f:
    data = json.load(f)
  print('Secrets... {}'.format(data))

  org_url = 'https://www.tenjin.com/dashboard/admin/organizations'
  url = '/'.join([org_url, data[u]['org']])

  driver = webdriver.Chrome('/Users/yuleng/wxbot/chromedriver')
  driver.get(url)

  username = driver.find_element_by_id(data['tenjin']['login_id'])
  username.send_keys(data['tenjin']['login'])
  password = driver.find_element_by_id(data['tenjin']['password_id'])
  password.send_keys(data['tenjin']['password'])
  btn = driver.find_element_by_id(data['tenjin']['login_btn_id'])
  btn.click()

  time.sleep(10)

  # impersonate_url = 'https://www.tenjin.com/dashboard/admin/users/{}/become'.format(u)
  impersonate_btn = driver.find_element_by_css_selector(data['impersonate_css'])
  impersonate_btn.click()
  # driver.get(impersonate_url)

  time.sleep(10)

  market_ch_ids = []
  int_url = 'https://www.tenjin.com/dashboard/integrations'
  channel_url = '/'.join([int_url, ch])
  driver.get(channel_url)

  if ch in san:
    # #ad_accounts > div.content > div > div:nth-child(1) > div > div > div > div > div.listing-card-content-inner-header.listing-card-content-inner-header--ellipsis > h4 > a
    market_chs = driver.find_elements_by_css_selector('h4 > a')
    for market_ch in market_chs:
      market_ch_id = market_ch.get_attribute('href')
      print('Getting market ch id {}...'.format(market_ch_id))
      market_ch_id = market_ch_id.rsplit('/', 1)[-1]
      # print(market_ch_id)
      market_ch_ids.append(market_ch_id)

  if ch in non_san:
    # listing-card.panel.panel-default.listing-card--integrations
    market_ch = driver.find_element_by_css_selector('a.listing-card.panel.panel-default.listing-card--integrations')
    market_ch_id = market_ch.get_attribute('href')
    print('Getting market ch id {}...'.format(market_ch_id))
    market_ch_id = market_ch_id.rsplit('/', 1)[-1]
    market_ch_ids.append(market_ch_id)

  time.sleep(10)

  driver.get(histats_url)
  # historical_stats_request_ad_account_id
  for i, market_ch_id in enumerate(market_ch_ids):
    print('+++ {} out of {} market_ch_ids +++'.format(i+1, len(market_ch_ids)))
    print(market_ch_id)
    market_ch_acc = driver.find_element_by_id('historical_stats_request_ad_account_id')
    market_ch_acc.send_keys(market_ch_id)
    d_start = driver.find_element_by_id('historical_stats_request_start_date')
    d_start.send_keys(d_from)
    d_end = driver.find_element_by_id('historical_stats_request_end_date')
    d_end.send_keys(d_to)
    time.sleep(3)
    btn = driver.find_element_by_name('commit').submit()
    # btn.click()
    time.sleep(3)

  print('Done...')

  input("Press Enter to continue...")
  driver.close()
  return 

if __name__ == '__main__':
  histats()

# https://www.tenjin.com/dashboard/admin/organizations/db8417df-3379-45a4-a684-376923e19c58