#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOT_NAME = 'transpondcontent'

SPIDER_MODULES = ['transpondcontent.spiders']

NEWSPIDER_MODULE = 'transpondcontent.spiders'

INPUTFILE_POSITION = '//Long//input.txt'

# 这里设置ip池文件的位置
IPPOOL_FILE_POSITION = './/transpondcontent//ippool'

# 这里设置当前机器的系统类型，关系到IP代理代理样式
LOCALHOST_OP_TYPE = 'LINUX'
#LOCALHOST_OP_TYPE = 'WINDOWS'


# IP代理高频率检测的频率
IPPROXY_FILETER = 1

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 连接失败后尝试的最大次数
# 20次基本可以保证没有数据的丢失
RETRY_TIMES = 20

# 在错误码为下列之一时进行重试
# 用代理常出现的是10060和10061，403和414是卜用代理是常出现的
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 414, 10060, 10061]

# 设置爬取时间，数字越小爬取越快，但是也容易被禁IP
DOWNLOAD_DELAY = 0.5

# 随机请求延迟
RANDOMIZE_DOWNLOAD_DELAY = False

# 并发请求的最大数量
# 设为4时，五分钟测试每秒22.60条（24.02），平均一天190.5w
# 设为8时，五分钟测试每秒31.23条，第二次测试每秒19.00条
# 设为16时，每天单机349.57w微博，第二次测试每秒30.49条（下午15点），第三次测试每秒17.32条（夜间18点），第四次测试20.26秒（夜间20点）
CONCURRENT_REQUESTS = 16

# 日志信息打印
#LOG_ENABLED = True
#LOG_ENCODING = 'utf-8'
#LOG_LEVEL = 'DEBUG'
#LOG_FILE = "weiboContentLog.log"


# 禁用cookie
COOKIES_ENABLED = False

# IPPOOL的大小
IPPOOL_SIZE = 8


# 读取文件的位置
# 由于使用分布式，uid从redis中读取
#INPUTFILE_POSITION = 'E://python/input.txt'
#INPUTFILE_POSITION = 'E://input.txt'

# 下边是mongodb的相关配置
MONGO_HOST = "XXXXXXXXXXXXX"  # hadoop-104、hadoop-107、hadoop-110、hadoop-113
MONGO_PORT = 27017  # 端口号
MONGO_DB = "weiboTranspondContent"  # 库名
MONGO_COLL = "collections"  # collection名
# MONGO_USER = "zhangsan"
# MONGO_PSW = "123456"

# 设置中间件
DOWNLOADER_MIDDLEWARES = {

    # 用户代理池的中间件
    "transpondcontent.middlewares.AgentMiddleware": 401,
    # IP代理池的中间件，
    "transpondcontent.middlewares.IPMiddleware" : 402,

}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'scrapy_redis.pipelines.RedisPipeline':300,            # redis的pipeline
    'transpondcontent.pipelines.transpondcontentPipeline': 301,   # mongodb的pipeline
    #'commentcontent.pipelines.commentcontentPipeline_mysql': 302, # mysql的pipeline
}

# 下载的超时时间设置，由于这里优先考虑速度，所以最大等待从180 -> 3
# 因为IP更新速度为5秒一次，3秒近似更新的中间值
DOWNLOAD_TIMEOUT = 3

# 一定要加这一句!!!!!!!!!!!!!!!确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#不清空redis queue，允许爬取过程中暂停并恢复
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

#链接远程的redis数据库
# 集群中所有机器共用116的redis
REDIS_URL = 'redis://XXXXXXXXX'



