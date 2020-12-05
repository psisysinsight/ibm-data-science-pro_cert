#!/usr/bin/env python3

import sys
import os
import re
import operator
import csv

log_file = "syslog.log"
error_message_csv = "error_message.csv"
error_message_html = "/var/www/html/error_message.html"
user_statistics_csv = "user_statistics.csv"
user_statistics_html = "/var/www/html/user_statistics.html"

error_messages = {}
user_statistics = {}

with open(log_file) as log:
  while True:
    # print("Reading log entry")
    log_entry = log.readline().strip()
    if not log_entry:
      # print("Last record read")
      break
    parsed_entry = re.search(r"^[\w :.]+ticky: ((?:INFO)|(?:ERROR)) (\w[\w ']*)[^(]*\(([\w.]*)\)$", log_entry)
    # print(parsed_entry)
    if parsed_entry == None:
      # print("Valid log entry not found. Getting next record")
      continue
    # print(parsed_entry)
    if parsed_entry.group(1).strip() == "ERROR":
      # print("ERROR entry found")
      if  parsed_entry.group(2).strip() not in error_messages:
        error_messages[parsed_entry.group(2).strip()] = 0
      error_messages[parsed_entry.group(2).strip()] += 1
      if parsed_entry.group(3) not in user_statistics:
        user_statistics[parsed_entry.group(3).strip()] = [0,0]
      user_statistics[parsed_entry.group(3).strip()][1] += 1
      continue
    if parsed_entry.group(1).strip() == "INFO":
      # print("INFO entry found")
      if parsed_entry.group(3).strip() not in user_statistics:
        user_statistics[parsed_entry.group(3).strip()] = [0,0]
      user_statistics[parsed_entry.group(3).strip()][0] += 1

error_messages_sorted = sorted(error_messages.items(), key=operator.itemgetter(1), reverse=True)
user_statistics_sorted = [(row[0],row[1][0],row[1][1])for row in  sorted(user_statistics.items())]
# print(user_statistics_sorted)
error_messages_sorted.insert(0, ("Error", "Count"))
# print(error_messages_sorted)
user_statistics_sorted.insert(0, ("Username", "INFO", "ERROR"))
# print(user_statistics_sorted)

with open(error_message_csv, "w", newline = "") as error_message_csv_file:
  error_writer = csv.writer(error_message_csv_file)
  error_writer.writerows(error_messages_sorted)

with open(user_statistics_csv, "w", newline="") as user_statistics_csv_file:
  user_writer = csv.writer(user_statistics_csv_file)
  user_writer.writerows(user_statistics_sorted)



