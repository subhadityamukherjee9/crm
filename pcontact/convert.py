import csv
from elasticsearch import Elasticsearch
import sys
import re
import json
import logging
logger = logging.getLogger('uploadcsv')

class Connect(object):

    def __init__(self):
        self.json = {}
        self.json['tags'] = ''
        self.json['summary'] = ''
        self.json['role'] = ''
        self.json['visibility']=''
        self.json['profile_url']=''


    def add_position(self, str):
        start = 0
        pos_item = {}
        while True:
            pos1 = str.find('Company Name', start)
            pos2 = str.find("Dates Employed", start)
            pos3 = str.find("Employment Duration",start)
            pos4 = str.find("Location", start)
            if pos1 == -1:
                pos_item['title']=str.strip()
            else:
                pos_item['title'] = str[start: pos1 - 1].strip()

            if pos2 == -1:
                pos_item['company']= str[pos1+12:].strip()
            else:
                pos_item['company']= str[pos1+12:pos2].strip()

            if pos3 == -1:
                pos_item['dates_employed']='-'.join(str[pos2+14:].strip().split(b'\xe2\x80\x93')).replace(" \u00e2\u0080\u0093 ","-")
            else:
                pos_item['dates_employed']='-'.join(str[pos2+14:pos3].strip().split(b'\xe2\x80\x93'.decode('utf-8'))).replace(" \u00e2\u0080\u0093 ","-")

            if pos4 == -1:
                pos_item['duration']=re.split("[\r\n]+",str[pos3+20:])[0].strip()
                pos_item['location']=""
                if pos3 == -1:
                    pos_item['duration']=""
                if pos2 == -1:
                    pos_item['dates_employed']=""
                if pos1 == -1:
                    pos_item['company']=""
            else:
                pos_item['duration']=str[pos3+19:pos4].strip()
                pos_item['location']=re.split("[\r\n]+",str[pos4+9:])[0].strip()
                if pos3 == -1:
                    pos_item['duration']=""
                if pos2 == -1:
                    pos_item['dates_employed']=""
                if pos1 == -1:
                    pos_item['company']=""
            break
        self.json['positions'].append(pos_item)
        summary = ''
        keys = ['title','company', 'location', 'dates_employed']
        for k in keys:
            if k in pos_item:
                summary += (pos_item[k] + ',')
        self.json['summary'] += (summary +' | ')

    def add_education(self, str):
        start = 0
        pos_item = {}
        while True:
            pos1 = str.find('Degree Name', start)
            pos2 = str.find("Field Of Study", start)
            pos3 = str.find("Dates attended or expected graduation",start)

            if pos1 == -1:
                pos_item['college_name']= str[start:].strip()
            else:
                pos_item['college_name'] = str[start: pos1 - 1].strip()

            if pos2 == -1:
                pos_item['degree']= str[pos1+12:pos3].strip()
            else:
                pos_item['degree']= str[pos1+12:pos2].strip()
                if pos1 == -1:
                    pos_item['college_name'] = str[start: pos2 - 1].strip()

            if pos3 == -1:
                pos_item['field_study']=str[pos2+14:].strip()
                pos_item['dates']=""
                if pos2 == -1:
                    pos_item['field_study']=""
                if pos1 == -1:
                    pos_item['degree']=""
            else:
                pos_item['field_study']=str[pos2+14:pos3].strip()
                if pos2 == -1:
                    pos_item['field_study']=""
                    if pos1 == -1:
                        pos_item['college_name'] = str[start: pos3 - 1].strip()
                if pos1 == -1:
                    pos_item['degree']=""
                pos_item['dates']=str[pos3+50:pos3+70].strip().replace(" \u00e2\u0080\u0093 ","-")
            break
        self.json['education'].append(pos_item)
        # summary = ''
        # keys = ['title','company', 'location', 'dates_employed']
        # for k in keys:
        #     if k in pos_item:
        #         summary += (pos_item[k] + ',')
        # self.json['summary'] += (summary +' | ')

    """ Initialize fields from linedin  """
    def init_from_linkedin(self, row, count):
        try:
            self.json['name'] = row[5]
        except Exception as e:
            logger.error(count)
            logger.error("Error With Name Field")

        try:
            self.json['location'] = row[6]
        except Exception as e:
            logger.error(count)
            logger.error("Error With location Field")

        try:
            self.json['title'] = row[7]
        except Exception as e:
            logger.error(count)
            logger.error("Error With Title Field")

        try:
            # self.json['key_positions'] = row[12]
            self.json['profile_url'] = "https://www.linkedin" + row[9].split("linkedin",1)[1]
        except Exception as e:
            logger.error(count)
            logger.error("Error With linkedin_url Field")

        try:
            self.json['email'] = ' '.join(row[10].strip().split()).replace('Email ', '')
        except Exception as e:
            logger.error(count)
            logger.error("Error With Email Field")

        try:
            self.json['positions'] = []
            for i in range(0,5):
               tmp = row[i].strip()
               if tmp is not None and tmp != '':
                self.add_position(row[i])
        except Exception as e:
            logger.error(count)
            logger.error("Error With Company Field")

        try:
            self.json['education'] = []
            for i in range(11,13):
               tmp = row[i].strip()
               if tmp is not None and tmp != '':
                self.add_education(row[i])
        except Exception as e:
            logger.error(count)
            logger.error("Error With Education Field")

        try:
            self.json['img_url'] = row[13]
        except Exception as e:
            logger.error(count)
            logger.error("Error With Name Field")
