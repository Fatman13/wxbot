#!/usr/bin/env python
# coding=utf-8

import click

from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from classes.mopub_ad_impression import Mopub_ad_impression
from classes.app import App
# from classes import Mopub_ad_impression

@click.command()
@click.option('--d_from', default='2020-06-18')
@click.option('--d_to', default='2020-06-30')
def ilrd(d_from, d_to):
  # postgres://f91714cab30fd3e8d7e325ac077afba5:e8dDb62a4e76d519c7379c4bbaf8ac8f@windforce.dv.tenjin.com:5439/6e917fb2c33bd4b52d1bd1265b5e5fe9
  # db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"
  db_string = "postgres://f91714cab30fd3e8d7e325ac077afba5:e8dDb62a4e76d519c7379c4bbaf8ac8f@windforce.dv.tenjin.com:5439/6e917fb2c33bd4b52d1bd1265b5e5fe9"

  print('Conecting to {}...'.format(db_string))

  db = create_engine(db_string)  
  base = declarative_base()

  Session = sessionmaker(db)  
  session = Session()

  base.metadata.create_all(db)
  print('Init metadata of db...')

  res = session.query(App.name, App.platform, 
    func.sum(Mopub_ad_impression.revenue/100).label('rev_mopub'), 
    func.count(Mopub_ad_impression.impression_id)).join(App).filter(
    Mopub_ad_impression.created_at>=d_from).filter(
    Mopub_ad_impression.created_at<d_to)

  for ent in res:
    # print('')
    for key in ent.keys():
      print('key: {} value: {}'.format(key, ent[key]))

  return

  # Read
  mo_ad_imps = session.query(Mopub_ad_impression).limit(5).all()
  for mo_ad_imp in mo_ad_imps:
    # print('')
    print('adgroup_name: {} adunit_name: {} app_id: {} bundle_id: {} developer_device_id: {} impression_id: {} uuid: {}'.format(
      mo_ad_imp.adgroup_name, mo_ad_imp.adunit_name, mo_ad_imp.app_id, mo_ad_imp.bundle_id, mo_ad_imp.developer_device_id, mo_ad_imp.impression_id, mo_ad_imp.uuid ))
    print(mo_ad_imp)

if __name__ == '__main__':
  ilrd()