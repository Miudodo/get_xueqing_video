#-*- coding:utf-8 -*-
__author__ = 'miudodo'

import os

dir_base = r'E:\\Workspace\\PycharmProjects\\xueqing_data\\vedio\\'
to_dir = r'E:\\Workspace\\PycharmProjects\\xueqing_data\\vedios\\'

log = len(os.listdir(dir_base))

for i in range(1, log + 1):
    #print i ,str(i)
    dir_vedio_list = dir_base + str(i)
    logs = len(os.listdir(dir_vedio_list))
    for j in range(1,logs + 1):
        dir_vedio = dir_vedio_list + r'\\'+ str(j) + r'\\'
        command = 'copy/b ' + dir_vedio + '*.ts ' + to_dir + str(i) + '_' + str(j) + '.ts'
        #print dir_vedio, command
        os.system(command)
