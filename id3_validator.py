#!/usr/bin/env python3

'''
****************************
* Created by: Matt Kiernan *
****************************
'''

import urllib.request
import sys
import re
import json

# base_url = "http://40.71.5.142:8080/"
base_url = "https://engineeringportal.nielsen.com/id3/"
#base_url = "http://id3.eastus.cloudapp.azure.com:8080/"

if len(sys.argv) <= 1:
    print('ID3 Validator for test cases',
          '\n\nEnter your log file as an argument\n(EX: ./id3_validator.py ~/Desktop/my_logs.txt)',
          '\n\nTo change number of tags tested (default is 8), enter a number after your log file\n(EX: ./id3_validator.py ~/Desktop/my_logs.txt 20)')
    exit(1)


path_to_file = sys.argv[1]

try:
    number_of_tags = int(sys.argv[2])
except:
    number_of_tags = 8

id3_file = open(path_to_file, 'r')
file_contents = id3_file.read()



try:
    # id3_tags = re.findall('www.nielsen.+?(?=\|)', file_contents)
    # id3_tags = re.findall('www.nielsen.*\/\d\d', file_contents)
    # id3_tags = re.findall('www.nielsen.+?(?=%|]|&)', file_contents)
    id3_tags = re.findall('www.nielsen.{238}', file_contents)
    
    if id3_tags == []:
        # id3_tags = re.findall('www.nielsen.*\/..', file_contents)
        id3_tags = re.findall('www.nielsen.{238}', file_contents)
       #id3_tags = re.findall('www.nielsen.*', file_contents)
       # id3_tags = re.findall('www.nielsen.+?(?=")', file_contents)
    if id3_tags == []:
        print("No ID3 tags detected")
        sys.exit()
except:
    print("No ID3 tags detected")
    sys.exit()

unique_id3_tags = list(set(id3_tags))
# print(unique_id3_tags)
print("\n\n")

def print_statement ( id3, sid, ts, cn ):
    "This prints out the format for the spreadsheet"
    print(id3)
    print(sid)
    print(ts)
    print(cn)
    print("")
    return;

for x in range(0,number_of_tags):
    id3_tag = unique_id3_tags[x]
    full_url = base_url + id3_tag
    
    f = urllib.request.urlopen(full_url)
    response = f.read().decode('utf-8')
    
    try:
        response_sid = re.search('[^sid":"][0-9]{2,4}', response).group()
    except:
        response_sid = "N/A"
    try:
        response_time = re.search('(?!timestamp":")[0-9]{2}\/[0-9]{2}\/[0-9]{4}\ [0-9]{2}\:[0-9]{2}\:[0-9]{2}', response).group()
    except:
        response_time = "N/A"
    try:
        response_channel = re.search('(?<=name":").+?(?=")', response).group()
    except:
        response_channel = "N/A"
    
    print_statement(id3_tag, response_sid, response_time, response_channel)
