#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import time
import re
import sys
from ADC_function import *
import json
import shutil
from configparser import ConfigParser
os.chdir(os.getcwd())

# ============global var===========

version='0.11.9'

config = ConfigParser()
config.read(config_file, encoding='UTF-8')

Platform = sys.platform

# ==========global var end=========

def UpdateCheck():
    if UpdateCheckSwitch() == '1':
        html2 = get_html('https://raw.githubusercontent.com/wenead99/AV_Data_Capture/master/update_check.json')
        html = json.loads(str(html2))

        if not version == html['version']:
            print('[*]        * New update ' + html['version'] + ' *')
            print('[*]             * Download *')
            print('[*] ' + html['download'])
            print('[*]=====================================')
    else:
        print('[+]Update Check disabled!')
def movie_lists():
    directory = config['directory_capture']['directory']
    a2=[]
    b2=[]
    c2=[]
    d2=[]
    e2=[]
    f2=[]
    g2=[]
    h2=[]
    if directory=='*':
        for i in os.listdir(os.getcwd()):
            a2 += glob.glob(r"./" + i + "/*.mp4")
            b2 += glob.glob(r"./" + i + "/*.avi")
            c2 += glob.glob(r"./" + i + "/*.rmvb")
            d2 += glob.glob(r"./" + i + "/*.wmv")
            e2 += glob.glob(r"./" + i + "/*.mov")
            f2 += glob.glob(r"./" + i + "/*.mkv")
            g2 += glob.glob(r"./" + i + "/*.flv")
            h2 += glob.glob(r"./" + i + "/*.ts")
        total = a2 + b2 + c2 + d2 + e2 + f2 + g2 + h2
        return total
    a2 = glob.glob(r"./" + directory + "/*.mp4")
    b2 = glob.glob(r"./" + directory + "/*.avi")
    c2 = glob.glob(r"./" + directory + "/*.rmvb")
    d2 = glob.glob(r"./" + directory + "/*.wmv")
    e2 = glob.glob(r"./" + directory + "/*.mov")
    f2 = glob.glob(r"./" + directory + "/*.mkv")
    g2 = glob.glob(r"./" + directory + "/*.flv")
    h2 = glob.glob(r"./" + directory + "/*.ts")
    total = a2 + b2 + c2 + d2 + e2 + f2 + g2 + h2
    return total
def CreatFailedFolder():
    if not os.path.exists('failed/'):  # 新建failed文件夹
        try:
            os.makedirs('failed/')
        except:
            print("[-]failed!can not be make folder 'failed'\n[-](Please run as Administrator)")
            os._exit(0)
def lists_from_test(custom_nuber): #电影列表
    a=[]
    a.append(custom_nuber)
    return a
def CEF(path):
    files = os.listdir(path)  # 获取路径下的子文件(夹)列表
    for file in files:
        try: #试图删除空目录,非空目录删除会报错
            os.removedirs(path + '/' + file)  # 删除这个空文件夹
            print('[+]Deleting empty folder',path + '/' + file)
        except:
            a=''
def rreplace(self, old, new, *max):
#从右开始替换文件名中内容，源字符串，将被替换的子字符串， 新字符串，用于替换old子字符串，可选字符串, 替换不超过 max 次
    count = len(self)
    if max and str(max[0]).isdigit():
        count = max[0]
    return new.join(self.rsplit(old, count))
def getNumber(filepath):
    try:  # 普通提取番号 主要处理包含减号-的番号
        filepath1 = filepath.replace("_", "-")
        filepath1.strip('22-sht.me').strip('-HD').strip('-hd')
        filename = str(re.sub("\[\d{4}-\d{1,2}-\d{1,2}\] - ", "", filepath1))  # 去除文件名中时间
        file_number = re.search('\w+-\d+', filename).group()
        return file_number
    except:  # 提取不含减号-的番号
        try:  # 提取东京热番号格式 n1087
            filename1 = str(re.sub("h26\d", "", filepath)).strip('Tokyo-hot').strip('tokyo-hot')
            filename0 = str(re.sub(".*?\.com-\d+", "", filename1)).strip('_')
            if '-C.' in filepath or '-c.' in filepath:
                cn_sub = '1'
            file_number = str(re.search('n\d{4}', filename0).group(0))
            return file_number
        except:  # 提取无减号番号
            filename1 = str(re.sub("h26\d", "", filepath))  # 去除h264/265
            filename0 = str(re.sub(".*?\.com-\d+", "", filename1))
            file_number2 = str(re.match('\w+', filename0).group())
            if '-C.' in filepath or '-c.' in filepath:
                cn_sub = '1'
            file_number = str(file_number2.replace(re.match("^[A-Za-z]+", file_number2).group(),
                                                   re.match("^[A-Za-z]+", file_number2).group() + '-'))
            return file_number
            # if not re.search('\w-', file_number).group() == 'None':
            # file_number = re.search('\w+-\w+', filename).group()
            #

def RunCore():
    if Platform == 'win32':
        if os.path.exists('core.py'):
            os.system('python core.py' + '   "' + i + '" --number "' + getNumber(i) + '"')  # 从py文件启动（用于源码py）
        elif os.path.exists('core.exe'):
            os.system('core.exe' + '   "' + i + '" --number "' + getNumber(i) + '"')  # 从exe启动（用于EXE版程序）
        elif os.path.exists('core.py') and os.path.exists('core.exe'):
            os.system('python core.py' + '   "' + i + '" --number "' + getNumber(i) + '"')  # 从py文件启动（用于源码py）
    else:
        if os.path.exists('core.py'):
            os.system('python3 core.py' + '   "' + i + '" --number "' + getNumber(i) + '"')  # 从py文件启动（用于源码py）
        elif os.path.exists('core.exe'):
            os.system('core.exe' + '   "' + i + '" --number "' + getNumber(i) + '"')  # 从exe启动（用于EXE版程序）
        elif os.path.exists('core.py') and os.path.exists('core.exe'):
            os.system('python3 core.py' + '   "' + i + '" --number "' + getNumber(i) + '"')  # 从py文件启动（用于源码py）

if __name__ =='__main__':
    print('[*]===========AV Data Capture===========')
    print('[*]           Version '+version)
    print('[*]=====================================')
    CreatFailedFolder()
    UpdateCheck()
    os.chdir(os.getcwd())

    count = 0
    count_all = str(len(movie_lists()))
    print('[+]Find',str(len(movie_lists())),'movies')
    for i in movie_lists(): #遍历电影列表 交给core处理
        count = count + 1
        percentage = str(count/int(count_all)*100)[:4]+'%'
        print('[!] - '+percentage+' ['+str(count)+'/'+count_all+'] -')
        try:
            print("[!]Making Data for   [" + i + "], the number is [" + getNumber(i) + "]")
            RunCore()
            print("[*]=====================================")
        except:  # 番号提取异常
            print('[-]' + i + ' Cannot catch the number :')
            print('[-]Move ' + i + ' to failed folder')
            shutil.move(i, str(os.getcwd()) + '/' + 'failed/')
            continue


    CEF('JAV_output')
    print("[+]All finished!!!")
    input("[+][+]Press enter key exit, you can check the error messge before you exit.\n[+][+]按回车键结束，你可以在结束之前查看和错误信息。")