#-*- coding:utf-8 -*-
__author__ = 'miudodo'

import requests
import re
import urlparse
from get_xueqing.get_xueqing import get_xueqing_data


user = [username] #雪晴数据网账号
pwd = [password] #雪晴数据网密码

url = 'http://www.xueqing.cc/course/page/'

gdata = get_xueqing_data()
gdata.login(user, pwd)

for i in range(1,5):
    url = urlparse.urljoin(url,str(i))
    gdata.get_course_data(url)
