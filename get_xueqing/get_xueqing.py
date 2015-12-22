#-*- coding:utf-8 -*-
__author__ = 'miudodo'

import requests
import re
import urlparse
import os
import urllib


class get_xueqing_data():
    s = requests.Session()

    #获取页面内容
    def get_data(self, url, p):
        try:
            response = self.s.get(url)
            r_text = response.text.encode('GB18030')
            r_groups = re.findall(p, r_text)
            return r_groups
        except Exception, e:
            print e
            return 0


    #下载视频文件
    def get_vedio_file(self, file_url, course_name, course_list, lesson, classes):
        p = r'[0-9]+?.ts'
        file_name = ''.join(re.findall(p, file_url))

        base_dir = "E:\\Workspace\\PycharmProjects\\xueqing_data\\vedio\\"
        file_dir = base_dir + lesson + '\\' + classes + '\\'

        #判断文件夹是否存在
        if os.path.isdir(file_dir):
            pass
        else:
            os.makedirs(file_dir)
        os.chdir(file_dir)

        try:
            r = self.s.get(file_url)
            with open(file_name ,"wb") as code:
                code.write(r.content)
        except IOError:
            return "Error: Can\'t download Course %s List %s file %s" % (course_name, course_list, file_name)
        else:
            print "Download Course %s List %s file %s successfully" % (course_name, course_list, file_name)


    #下载存储视频链接的文件，调用下载函数，返回成功信息
    def get_vedio(self, video_url, course_name, course_list, lesson, classes):
        try:
            r = self.s.get(video_url)
            r_txt = r.content

            p = r'(http://.*?)\n'
            file_url = re.findall(p, r_txt)
            #print file_url

            for f in file_url:
                #print f,type(f)
                self.get_vedio_file(f, course_name, course_list, lesson, classes)

        except Exception, e:
            print e
            return 0

    def get_course_data(self, start_url):
        try:
            p_list = r'class="course-card"><a title="(.*?)" href="(\/course/[0-9]+)">'
            p_course =  r'<a href="(.*?)">(.*?)</a><span class="item-free">'
            p_video = r'<source src="(.+?)"  type="video/mp4">'
            #课程列表信息
            item = self.get_data(start_url, p_list)
            lesson = 1
            for i in item:
                course_list_url = urlparse.urljoin('http://www.xueqing.cc/', i[1])
                course_name = i[0]
                p_no_buy = r'class="elective-course-btn" href="(.*?)">'
                buy_url = self.get_data(course_list_url, p_no_buy)

                #未选修课程时处理
                if buy_url <> []:
                    buy_url = urlparse.urljoin('http://www.xueqing.cc/', ''.join(buy_url))
                    self.s.get(buy_url)
                    c_groups = self.get_data(course_list_url, p_course)
                else:
                    c_groups = self.get_data(course_list_url, p_course)

                classes = 1
                for c in c_groups:
                    course_url = urlparse.urljoin('http://www.xueqing.cc/', c[0])
                    #print c[0],course_url
                    video_url = self.get_data(course_url, p_video)
                    #print video_url
                    video_url = ''.join(video_url)
                    print video_url, course_name,c[1],str(lesson),str(classes)
                    self.get_vedio(video_url, course_name, c[1], str(lesson), str(classes))
                    classes = classes + 1
                lesson = lesson + 1
        except Exception, e:
            print e
            return 0

    #登录
    def login(self, user, pwd):
        try:
            '''
            p = r'type="hidden" value="(.+?)" name="YII_CSRF_TOKEN"'

            response = self.s.get(login_url)
            r_text = response.text.encode('GB18030')
            token = re.findall(p, r_text)

            print token
            '''
            login_url = 'http://www.xueqing.cc/u/login'
            data = {
                #'YII_CSRF_TOKEN': token[0],
                'LoginForm[username]': user,
                'LoginForm[password]': pwd,
                'LoginForm[rememberMe]' : '0',
                #'LoginForm[rememberMe]' : '1',
                'yt0' : r'登陆'
            }

            header = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded',
                'Host':'www.xueqing.cc',
                'Origin':'http://www.xueqing.cc',
                'Pragma':'no-cache',
                'Referer':'http://www.xueqing.cc/u/login',
                'Upgrade-Insecure-Requests':1,
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
            }

            self.s.post(login_url, data=urllib.urlencode(data), headers = header, allow_redirects=False)
            #r_text2 = r.text.encode('GB18030')
            #token2 = re.findall(p, r_text2)
            #print token2

        except Exception, e:
            print e
            return 0