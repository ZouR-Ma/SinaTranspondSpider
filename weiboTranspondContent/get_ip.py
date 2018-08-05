#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
获取IP代理
代理直接写到了文件中，没有push到redis中
好处是各个机器之间的ip池之间有差异不会全部都崩
缺点是不好维护
editor:  邹佳旭
'''

import urllib
import time
import threading
import os, sys

import redis
from redis import Redis
import requests


ips = [

]



# 获取代理IP的线程类
# 这里有存入文件和存入redis两种方式，集群使用的是redis
class GetIpThread(threading.Thread):

    def __init__(self,fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond = fetchSecond

    def run(self):

        while True:

            # 获取最新的IP代理
            try :
                res = urllib.urlopen(apiUrl).read().strip("\n")
                # 有时IP接口会出现too many requests 的提示而不是正经的代理IP
                if (res.find('too') != -1 or res.find('false') != -1):
                    print '---------------------------------------------------'
                    print time.strftime(' %Y-%m-%d   %H:%M:%S ', time.localtime(time.time()))
                    print '---------------------------------------------------'
                    print u'-->> 获取代理IP失败 <<-- '
                    print u'-->>    正在重试    <<-- '
                    print '---------------------------------------------------'
                    time.sleep(1)
                    continue
                # 按照\n分割获取到的IP
                ips = res.split("\n")
            except :
                print u' 获取IP代理过程中出现错误！'
                time.sleep(1)
                continue

            # 获取IP列表
            print '\t---------------------------------------------------'
            print '\t', time.strftime(' %Y-%m-%d   %H:%M:%S ', time.localtime(time.time()))
            print '\t---------------------------------------------------'

            # 获取ippool中存在的ip
            IPOOL_SIZE = 8
            r = redis.Redis(host='222.27.227.116', port=6379, db=1)

            # 先将最新IP验证之后加入ip池中
            for proxy in ips :
                # 校验代理
                try :
                    # 爬取的是移动端的api，所以ping的是weibo的移动端首页
                    #proxies = {'http://': + proxy}
                    real_proxy = 'http://' + proxy
                    if requests.get('https://passport.weibo.cn/signin/login', proxies={'http:':real_proxy}, timeout=3 ).status_code == 200 :

                      # 验证成功加入IP代理池，队尾入队
                        r.rpush('weibo:ippool', proxy)
                        print u' 代理IP  %-25s 加入了 当前IP池  ' % proxy
                    else :
                        # 校验失败
                        print  u' 代理IP  %-25s 已被过滤  ' % proxy
                        continue
                except:
                    # 校验失败
                    print  u' 代理IP  %-25s 已被过滤  ' % proxy
                    continue

            print '\t---------------------------------------------------'


            # 删除多余的IP代理
            # print 'len ippool :  ', r.llen("weibo:ippool")
            while r.llen("weibo:ippool") > IPOOL_SIZE :
                proxy = r.lpop('weibo:ippool')
                print u' 代理IP  %-25s 离开了 当前IP池  ' % proxy

            # 打印提示信息
            print '\t---------------------------------------------------'
            print u'\t 当前IP池中容量为：  %-4d ' % r.llen("weibo:ippool")
            print '\t---------------------------------------------------\n'

            # 向redis中push更新时间
            # 该队列长度始终为2，左边是最新的时间，右边是上次更新的时间
            r.lpush('weibo:refreshTime', str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
            while ( r.llen("weibo:refreshTime") > 2 ):
                r.rpop('weibo:refreshTime')

            # 休眠
            time.sleep(self.fetchSecond)


if __name__ == '__main__':
    # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
    order = "3fd557b2c2b953911e6d232a58a7d121"
    # 获取IP的API接口
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    # 要抓取的目标网站地址
    targetUrl = "http://1212.ip138.com/ic.asp"
    # 获取IP时间间隔，建议为5秒
    fetchSecond = 5
    # 开始自动获取IP
    GetIpThread(fetchSecond).start()
