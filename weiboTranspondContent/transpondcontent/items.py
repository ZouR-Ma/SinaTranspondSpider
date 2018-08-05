#!/usr/bin/env python
# -*- coding: utf-8 -*-



import scrapy
from scrapy import Field,Item


class WeibocontentItem(scrapy.Item):
    # define the fields for your item here like:
    """
    # 原微博的基本信息
    prWeiboId = Field()       # 原微博的ID

    prId = Field()            # 原创人的ID
    prName = Field()          # 原微博的昵称

    prText = Field()          # 原微博的文字内容
    prPicInfo = Field()       # 原微博的图片信息，这里没有进行再次细化，因为那样在保存起来很麻烦，虽然没有细化但是粗细度也可以接受，处理起来不会太困难
    prRepost = Field()        # 原微博的转发次数
    prAttu = Field()          # 原微博的点赞数
    prComment = Field()       # 原微博的评论数
    prFrom = Field()          # 原微博的来源（设备）
    prTime = Field()          # 原微博的发布时间
    """

    # 微博的转发信息
    reWeiboId = Field()    # 转发后的微博的ID

    reId = Field()         # 转发人的ID
    reName = Field()       # 转发人的昵称
    reUrl = Field()        #转发人的主页url

    reText = Field()       # 转发时的文字内容
    rePicInfo = Field()    # 转发时的图片内容
    reRepost = Field()     # 转发博文从此处再次被转发的次数
    reAttu = Field()       # 转发博文在此处的点赞数
    reFrom = Field()       # 转发博文的来源（设备）
    reTime = Field()       # 转发博文的发布时间

    crawlTime = Field()    # 爬虫爬取的时间 √


