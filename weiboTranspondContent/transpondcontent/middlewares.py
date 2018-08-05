#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests

import random
import threading
import time
import redis
from transpondcontent.user_agents import agents
from transpondcontent.settings import IPPOOL_SIZE
from transpondcontent.settings import LOCALHOST_OP_TYPE
import sys
from transpondcontent.settings import IPPOOL_FILE_POSITION
from scrapy.http import Request, request
from redis import Redis
from transpondcontent.settings import REDIS_URL
from transpondcontent.settings import IPPROXY_FILETER

reload(sys)
sys.setdefaultencoding('utf8')

class AgentMiddleware(object):

    # 设置请求头，从请求池中随机抽取
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        request.headers["Connection"] = 'keep-alive'
        request.headers["Accept-Language"] = 'zh-CN,zh;q=0.8'
        request.headers["Accept-Encoding"] = 'gzip, deflate, sdch'
        request.headers["Accept"] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'


# ip代理的中间件类
class IPMiddleware(object) :

    #  该ippool始终被另外一个线程更新
    ippool = [ ]

    def __init__(self, ip=''):
        # 更新代理池
        print u'查询IP代理池更新状态...'
        RefreshIpThread_redis().start()
        while self.ippool.__len__() == 0 :
            time.sleep(1)
            continue
        time.sleep(1)
        print u'IP代理池更新完毕'

    def process_request(self, request, spider):
        # 如果IP池为空，则等待，绝对不用本机IP
        # 这里没有设置循环上线，也就是说如果始终没有可用的IP出现它会一直空转，这样可以避免数据丢失
        while (IPMiddleware.ippool.__len__() == 0) :
            time.sleep(3)
            print '---------------------------------------------------'
            print u'-->>     当前IP池为空     <<-- '
            print u'-->>    获取代理IP失败    <<-- '
            print '---------------------------------------------------'
            continue

        if LOCALHOST_OP_TYPE == 'LINUX' :
            # linux下用这个
            proxy = str('http://' + random.choice(self.ippool))
        elif LOCALHOST_OP_TYPE == 'WINDOWS':
            # windows 下用这个
            proxy = random.choice(self.ippool)
        else :
            proxy = random.choice(self.ippool)

        # 将ip代理加入请求中
        request.meta['proxy'] =  proxy




# 获取代理IP的线程类，从redis中读取代理IP
# 这里还需要进行二次校验，因为redis爬取ip和这里从redis中取ip的过程间最多相差十秒，足够一个代理失效了

class RefreshIpThread_redis(threading.Thread):

    def run(self) :

        print u'IP代理池自动更新已开启'
        print 'method:  get from redis list'

        while True :
            # 首先给临时代理池赋初值，将新代理加入到临时的ip池中
            r = redis.Redis(host='222.27.227.116', port=6379, db=1)

            if (r.llen('weibo:ippol') < IPPOOL_SIZE) :
                ippool_ori = r.lrange('weibo:ippool', 0, r.llen('weibo:ippool'))
            else :
                ippool_ori = r.lrange('weibo:ippool', 0, IPPOOL_SIZE)

            # 二次校验
            # tmp_ippool中存放检验成功的IP
            tmp_ippool = []

            for proxy in ippool_ori :
                # 校验代理
                try :
                    proxies = {'http://': proxy}
                    #real_proxy = 'http://' + proxy
                    if requests.get('https://passport.weibo.cn/signin/login', proxies=proxies, timeout=2 ).status_code == 200 :
                        # 验证成功加入IP代理池则验证下一个
                        tmp_ippool.insert(0, proxy)
                    else :
                        # 校验失败
                        print  u' 失效代理 %25s 已被过滤' % proxy
                        continue
                except:
                    # 校验失败
                    print  u' 失效代理 %25s 已被过滤' % proxy
                    continue

            # 转存
            IPMiddleware.ippool = tmp_ippool

            # 如果ip池为空

            # 打印一点提示信息
            index = 0
            print '\n----------------------------------------------------------------------'
            for proxy in tmp_ippool :
                index = index + 1
                print ' ', index, u' 代理IP  %-25s 加入了 当前IP池  ' % proxy
            print '----------------------------------------------------------------------'
            print u'  IP代理池更新成功 ...'
            print u'    当前IP代理池的大小为 :  %4d' % len(IPMiddleware.ippool)
            print '----------------------------------------------------------------------\n'


            # 休眠
            time.sleep(5)
