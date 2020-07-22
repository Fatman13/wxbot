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

@click.command()
# @click.option('--org', default='db8417df-3379-45a4-a684-376923e19c58')
# @click.option('--u', default='867ab46b-4106-49b8-ab73-b642421a4406')
@click.option('--u', default='gamesunion')
# @click.option('--days', default=1, type=int)
# @click.option('--session_id', default='2171486e6c13b61ad78b34a59f337ab0')
# def collector(secrets, url, session_id):
def openu(u):
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

  time.sleep(3)

  # impersonate_url = 'https://www.tenjin.com/dashboard/admin/users/{}/become'.format(u)
  impersonate_btn = driver.find_element_by_css_selector(data['impersonate_css'])
  impersonate_btn.click()
  # driver.get(impersonate_url)

  input("Press Enter to continue...")
  driver.close()
  return 

if __name__ == '__main__':
  openu()

# https://www.tenjin.com/dashboard/admin/organizations/db8417df-3379-45a4-a684-376923e19c58