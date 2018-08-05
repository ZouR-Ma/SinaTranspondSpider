#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.spiders import Spider
import json
import codecs
import pymongo
import pymysql
from pymongo import MongoClient
from transpondcontent.settings import MONGO_COLL
from transpondcontent.settings import MONGO_DB
from transpondcontent.settings import MONGO_HOST
from transpondcontent.settings import MONGO_PORT

# 定义数据输出方式
class transpondcontentPipeline(object):

    '''
    def process_item(self, item, spider):
        file = codecs.open('weiboData.json', mode='ab', encoding='utf-8')
        line = json.dumps(dict(item)) + '\n'
        file.write(line.decode("unicode_escape"))
        return item
    '''

    # 将记录存入mongodb中
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host='xxxxxxxxxxxxxx',port=27017)
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client['weiboTranspondContent']  # 获得数据库的句柄
        self.coll = self.db['collections']  # 获得collection的句柄

    def process_item(self, item, spider):
        #postItem = dict(Redis_conn.blpop(["weibo:items"]))  # 把item转化成字典形式
        postItem = dict(item)
        self.coll.insert(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写
        # 将文件的记录存入mysql中


# 用mysql的输出方式
# failed and gave up, no continue ...
"""
class WeibocontentPipeline_mysql(object):
    # 初始化连接
    def __init__(self):
        self.conn = pymysql.connect(user='root', passwd='199628', db='weibo', host='localhost',port=3306, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    # 存放数据
    def process_item(self, item, spider):
        sql = 'insert into weibo (content) values (' +  str(json.dumps(dict(item))) + ');'
        self.cursor.execute(sql)
        self.conn.commit()
        return item
"""


