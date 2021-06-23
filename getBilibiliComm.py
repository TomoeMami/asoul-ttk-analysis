'''
@Description: 爬取B站弹幕和评论
@Author: sikaozhifu
@Date: 2020-06-24 11:29:58
@LastEditTime: 2020-07-02 19:13:42
@LastEditors: Please set LastEditors
'''
import requests
import re
import time
import math
import json
import os
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

'''
@description: 日期格式转换
@param : value
@return: dt
'''
types={
    'repost':17,
    'post':11,
    'cv':12,
    'av':1
}

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    path=path.encode('utf-8')
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
#repost代表所有转发，post代表动态。
def timestamp_datetime(value):
    format = r'%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    # 经过localtime转换后变成
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt
def main():

    #以下区域每次使用时更新，复制粘贴

    timedate='2021-06-08'
    threads = [{'oid':533990865853845019,'mode':'repost'},
    {'oid':11637363,'mode':'cv'},
    {'oid':11634943,'mode':'cv'}
    ]

    #复制粘贴到此为止


    #cv的oid是cv后的数字，无转发动态的oid是地址栏数字。
    for i in range(len(threads)):
        oid = threads[i]['oid']
        gettype = types.get(threads[i]['mode'],None)
        if gettype == 11:
            get_url='https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=%s' % oid
            response = requests.get(get_url, headers=headers)
            oid = response.json()['data']['card']['desc']['rid']
        comment_url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=%s&oid=%s&sort=1' % (gettype,oid)
        response = requests.get(comment_url, headers=headers)
        count = response.json()['data']['page']['count']  # 评论总数
        page_count = math.ceil(int(count) / 20)  # 评论总页数
        comment_list = []
        #追加模式
        for pn in range(4, page_count + 1):
            comment_url = 'https://api.bilibili.com/x/v2/reply?pn=%s&type=%s&oid=%s&sort=1' % (pn, gettype,oid)
            time.sleep(2)
            response = requests.get(comment_url, headers=headers)
            if('data' in response.json().keys()):
                replies = response.json()['data']['replies']
                if replies is not None:
                    for reply in replies:
                        # reply_id = reply['member']['mid']
                        # reply_name = reply['member']['uname']
                        # reply_time = timestamp_datetime(int(reply['ctime']))  # 评论时间
                        # reply_like = reply['like']  # 评论点赞数
                        # reply_content = reply['content']['message']  # 评论内容
                        reply_info = {
                            'reply_id': reply['member']['mid'],  # 评论者id,
                            'reply_name': reply['member']['uname'],  # 评论者昵称
                            'reply_time': timestamp_datetime(int(reply['ctime'])),  # 评论时间
                            'reply_like': reply['like'],  # 评论点赞数
                            'reply_content': reply['content']['message']  # 评论内容
                        }
                        comment_list.append(reply_info)
                        rcount = reply['rcount']  # 表示回复的评论数
                        page_rcount = math.ceil(int(rcount) / 10)  # 回复评论总页数
                        root = reply['rpid']
                        for reply_pn in range(1, page_rcount + 1):
                            time.sleep(2)
                            reply_url = 'https://api.bilibili.com/x/v2/reply/reply?&pn=%s&type=%s&oid=%s&ps=10&root=%s' % (reply_pn,gettype, oid, root)
                            response = requests.get(reply_url, headers=headers)
                            if('data' in response.json().keys()):
                                rreplies = response.json()['data']['replies']
                                if rreplies is not None:
                                    for reply in rreplies:
                                        # reply_id = reply['member']['mid']  # 评论者id
                                        # reply_name = reply['member']['uname']  # 评论者昵称
                                        # reply_time = timestamp_datetime(int(reply['ctime']))  # 评论时间
                                        # reply_like = reply['like']  # 评论点赞数
                                        # reply_content = reply['content']['message']  # 评论内容
                                        reply_info = {
                                            'reply_id': reply['member']['mid'],  # 评论者id,
                                            'reply_name': reply['member']['uname'],  # 评论者昵称
                                            'reply_time': timestamp_datetime(int(reply['ctime'])),  # 评论时间
                                            'reply_like': reply['like'],  # 评论点赞数
                                            'reply_content': reply['content']['message']  # 评论内容
                                        }
                                        comment_list.append(reply_info)
                    filedir = './'+timedate+'/'
                    mkdir(filedir)
                    save_path=filedir+str(threads[i]['oid'])+'-2.json'
                    with open(save_path, "w", encoding='utf-8') as f:
                        json.dump(comment_list, f, ensure_ascii=False, indent=4, separators=(',', ':'))
                    with open('./pn.txt', "w", encoding='utf-8') as f:
                        f.write('pn='+str(pn)+'\n')
            
if __name__ == "__main__":
    main()