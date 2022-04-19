#!/usr/bin/env python

import csv
import time 
import datetime 
import os 

from logger.Logger import Logger
from services.ConfigService import config
class CSVService:
  log = Logger(__name__)
  
  def __init__(self, hw_monitor, perf_monitor):
    self.time = time.time()
    self.sample = 1
    self.filename = ""
    self.fieldnames = ["time"]
    for hw_field_name in hw_monitor.get_field_names():
      self.fieldnames.append(hw_field_name)
    for perf_field_name in perf_monitor.get_field_names():
      self.fieldnames.append(perf_field_name)
    self.create_directory()
    self.create()
        

  def append(self, data):
    """
    Appends data to the .csv, if 4 hours have passed a new sample .csv file is created
    """
    if time.time() - self.time >= 432000:
      self.sample += 1
      self.time = time.time()
      self.create()
    with open(self.filename, "a", newline="", encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writerow(data)
  
  def create(self):
    """
    Creates a new .csv file
    """
    self.filename = "/tmp/thesis_monitor/BA_sample_{}_{}".format(self.sample,datetime.datetime.now().strftime("%d.%m.%y-%H.%M.%S")) + ".csv"
    with open(self.filename, "w", newline="", encoding='utf-8') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
      writer.writeheader()

  def create_directory(self):
    """
    Checks if the folder thesis_monitor exists, otherwise creates one
    """
    try:
        os.makedirs("/tmp/thesis_monitor")
    except:
        pass
        

