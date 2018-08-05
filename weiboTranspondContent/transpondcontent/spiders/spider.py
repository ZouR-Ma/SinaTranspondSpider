#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random
from json import loads
import time
import scrapy
from scrapy.spiders import Spider, CrawlSpider
from scrapy.http import Request
from transpondcontent.items import WeibocontentItem
from transpondcontent.user_agents import agents
from transpondcontent.settings import INPUTFILE_POSITION
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class TranspondcontentSpider(Spider) :
    name = "weibo"

    allowed_domains = ["m.weibo.cn"]

    #在start_requests方法中构建url

    def start_requests(self):
        # 从文件里读取ID
        #此处的id为该条微博的id，转发后id会不一样

        f = open(INPUTFILE_POSITION)
        for user_id in f.readlines():
            url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + str(user_id) + '&page=1'
            # 通过上方的url，爬取到该条微博转发的页数
            # 如果能成功连接就进行请求
            yield scrapy.Request(url, meta={'id': user_id}, callback=self.parse, dont_filter=True)
            #由于接下来的url需要微博id，所以用meta携带id


    def parse(self, response):

        curPage = response.body
        # \n是正常时回车，\r是win下的回车，这是防止有些微博里有换行而存入时不规整设计的
        curPage = curPage.replace('\n', '').replace('\r\n', '').replace('\r', '')
        content = json.loads(curPage)   #对爬取到的页面，进行转json的处理

        data = content.get("data")
        count = data.get("max")         # 原微博的转发数

        id = response.meta['id']        #将id从meta中取出

        for i in range(1,count):
            weibo_Repost_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=%s' %id +'&page=' +str(i)
            #构建每页评论的url
            yield  scrapy.Request(weibo_Repost_url, callback=self.get_weibo_repost)


    def get_weibo_repost(self, response):
        # 爬取所需要的数据

        curPage = response.body
        # \n是正常时回车，\r是win下的回车，这是防止有些微博里有换行而存入时不规整设计的
        curPage = curPage.replace('\n', '').replace('\r\n', '').replace('\r', '')
        content = json.loads(curPage)

        datas = content.get('data')
        data = datas.get('data')


        for i in range(0, 12):

            weiboItem = WeibocontentItem()
            weiboItemdata = data[i]

            weiboItem['reWeiboId'] = weiboItemdata.get('id')        # 转发后的微博的ID
            weiboItem['reText'] = weiboItemdata.get('raw_text')     # 转发时的文字内容
            weiboItem['reTime'] = self.time_form(weiboItemdata.get('created_at').encode('utf-8'))   # 转发博文的发布时间

            weiboUser = weiboItemdata.get('user')
            weiboItem['reId'] =  weiboUser.get('id')                # 转发人的id
            weiboItem['reName'] = weiboUser.get('screen_name')      # 转发人的昵称
            weiboItem['reUrl'] = weiboUser.get('profile_url')       # 转发人的url

            print u'正在处理第 %d 条微博：  %s  %s' % (i, weiboItem['reTime'], str(time.strftime('%H:%M:%S', time.localtime(time.time()))))
            yield weiboItem

    def time_form(self, time_str):
        if '刚刚' in time_str:
            real_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
            return real_time
        elif '分钟' in time_str:
            time_str = time_str.split('分钟')
            seconds = int(time_str[0]) * 60
            real_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - seconds))
            return real_time
        elif '小时' in time_str:
            time_str = time_str.split('小时')
            seconds = int(time_str[0]) * 60 * 60
            real_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - seconds))
            return real_time
        elif '今天' in time_str:
            time_str = time_str.split('今天')
            today = time_str[1]
            real_time = time.strftime('%Y-%m-%d', time.localtime(time.time())) + today
            return real_time
        elif '昨天' in time_str:
            time_str = time_str.split('昨天')
            yesterday = time_str[1]
            real_time = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60)) + yesterday
            return real_time
        elif len(time_str) == 5:
            real_time = time.strftime('%Y-', time.localtime(time.time())) + time_str
            return real_time
        else:
            real_time = time_str
            return real_time