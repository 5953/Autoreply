import requests
import re
import random
import onetimepass as otp
from time import sleep
import os
#from getver import GetVerificationCode
from multiprocessing import Pool
#from config import config
import pickle
import requests,os,urllib
import urllib.parse
result = None
over = False
flag = False
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.213 Safari/537.36"
loginurl = 'https://t66y.com/login.php'
url = 'https://t66y.com/thread0806.php?fid=7&search=today'
headers = {
    'Host': 't66y.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'https://t66y.com/index.php',
    'Upgrade-Insecure-Requests': '1',
    'user-agent': UserAgent
}
headers1 = {
    'Host': 't66y.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'https://t66y.com/login.php',
    'User-Agent': UserAgent
}

def gettodaylist():
#  black_list = []
#  url = 'https://t66y.com/thread0806.php?fid=7&search=today'
#  pat = ('htm_data/\w+/\w+/\w+.html')
#  con = requests.get(url, headers=headers,params=prams)
#  #head = {
#   #  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
# # 头部请求 通过 header 伪装成浏览器
#  #request = urllib.request.Request(url, headers=head, )  # method="get"
# # 把请求的信息通过urllib Request 封装给 自定义变量request 可以添加参数 method 默认get也可以post
# # print(resqust)
#  #response = urllib.request.urlopen(request)
#     # 通过urlopen访问变量requst 并返回给 自定义参数
#  con = response.read().decode("utf-8")
#print(con)
#  black_list = []
#  pat = ('htm_data/\w+/\w+/\w+.html')
#  con = requests.get(url, headers=headers)
#  con = con.content.decode('utf-8', 'ignore')
#
#  web_page = con
#  theme = con.find('普通主題')
# #
#  match = re.findall(pat, con[theme:])
# self.match = match
 url = 'http://t66y.com/thread0806.php?fid=7&search=today'
 UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
 headers = {
    'Host': 't66y.com',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://t66y.com/index.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': UserAgent
           }
 black_list = []
 pat = ('htm_data/\w+/\w+/\w+.html')
 con = requests.get(url, headers=headers)
 con = con.content.decode('utf-8', 'ignore')
 web_page = con
 theme = con.find('普通主題')

 match = re.findall(pat, con[theme:])

 remove_list = []
 moderator = web_page.find('版主')
 moderator = web_page[moderator:moderator + 800]
 pat = 'username=(\w+)'
 moderator_list = re.findall(pat, moderator)
 print('版主列表:' + ','.join(moderator_list))
 moderator_list = moderator_list

 content = con[theme:]
 pat = 'class="bl">(.*)?</a>'
 all_user = re.findall(pat, content)
 pat = '<h3><a href="([\s\S]*?)"'
 match = re.findall(pat, content)
 print('帖子数量为:' + str(len(all_user)))
 if len(all_user) != len(match):
        print('移除版主列表功能失效，请重试或者联系开发者更新')
        os._exit(0)
 for i in range(len(all_user)):
    if all_user[i] in moderator_list:
            remove_list.append(match[i])
 for data in remove_list:
         print('移除的版主帖子为:' + data)
         match.remove(data)
 print('版主帖子移除完毕')
 return match
def getreply():
    # 自定义回复内容，记得修改随机数
    #         reply=['1024感谢分享','1024感谢你的分享','1024谢谢分享','1024多谢分享','1024感谢作者的分享','1024谢谢坛友分享','1024内容精彩','1024的确如此','1024感谢分享','1024涨知识了','1024很有意思']
    #         reply_m=random.randint(0,len(reply)-1)
    reply_news = "1024"
    print('本次回复消息是:' + reply_news)
    return reply_news
def getnumber(cookies):

    


    sleep(2)
    indexurl = 'http://t66y.com/index.php'
    # cookie = "PHPSESSID=r06oi43udb09qhkj1okr9htin5; 227c9_ck_info=/	; 227c9_winduser=UAdTXAAFMQMIUQlUBVMGAwcBBgtRAVdQAAYGXlxVBgAOVARRWwRUbVZRC1IDBwhQBVQCBAUAVAMBXAVQC1dWVw8BBgZQUQMG; 227c9_groupid=8; 227c9_lastvisit=0	1651976637	/index.php?"
    headers2 = {
        'Host': 't66y.com',
        'Cookie': cookies,
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39",
    }
    sleep(2)
    index = requests.get(indexurl, headers=headers2)
    index = index.content.decode('utf-8', 'ignore')
    # print(index)
    pat = '共發表帖子: \d{1,5}'
    num = re.search(pat, index).group(0)
    num = num.replace('共發表帖子: ', '')
    return num
def getonelink(todaylist):
    geturl = ''
    m = random.randint(0, len(todaylist) - 1)
    geturl = 'http://t66y.com/' + todaylist[m]
    tid = todaylist[m][16:len(todaylist[m]) - 5]
    todaylist.remove(todaylist[m])
    # print('请求链接是: '+geturl)
    return geturl, tid
def getmatch(geturl):
    headers = {
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent
    }
    sleep(2)
    get = requests.get(geturl, headers=headers)
    sleep(2)
    get = get.content.decode('utf-8', 'ignore')
    pat = '<b>本頁主題:</b> .*</td>'
    res = re.search(pat, get)
    res = res.group(0).replace('<b>本頁主題:</b> ', '').replace('</td>', '')
    res = 'Re:' + res
    return res
def postreply(rcookies, res, reply_news, tid):
    headers = {
        'Host': 't66y.com',
        'Origin': 'null',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': rcookies,
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
    }
    posturl = 'http://t66y.com/post.php?'
    data = {
        'atc_usesign': '1',
        'atc_convert': '1',
        'atc_autourl': '1',
        'atc_title': res,
        'atc_content': reply_news,
        'step': '2',
        'action': 'reply',
        'fid': '7',
        'tid': tid,
        'atc_attachment': 'none',
        'pid': '',
        'article': '',
        'touid': '',
        'verify': 'verify',

    }
    post = requests.post(posturl, data=data, headers=headers)
    post = post.content.decode('utf-8', 'ignore')
    #print(post)
    if post.find('認證碼不正確或已過期') != -1:
        status = '回复失败，请检查cookies是否过期'
        print('回复失败，请检查cookies是否过期')
        return status

    if post.find('發貼完畢點擊') != -1:
        status = '回复成功'
        return status
    if post.find('所屬的用戶組') != -1:
        status = '今日已达上限'
        return status
def browse(geturl, cookies):
    headers = {
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent
    }
    res = requests.get(url=geturl, headers=headers, cookies=cookies)
def main(cookies, todaylist,rcookies):
    # 回复
    n = 0
    m = getnumber(cookies)#获取发帖时的数量
    suc = False
    print('账号开始时发表帖子:' + m)
    while n < 10 and suc is False:
        try:
            au = ''
            print('账号当前在回复第' + str(n + 1) + '个。')
            geturl, tid = getonelink(todaylist)
            reply_news = getreply()
            res = getmatch(geturl)
            sleeptime = random.randint(1048, 2048)
            au = postreply(rcookies, res, reply_news, tid)


            if au == '回复成功':
                print('账号回复成功')
                n = n + 1
                print('账号休眠' + str(sleeptime) + 's...')
                browse(geturl, cookies)
                sleep(sleeptime)
                print('账号休眠完成')
                pass
            elif au == '今日已达上限':
                print('账号回复失败，今日次数已达10次')
                suc = True
            else:
                print('账号1024限制或者被禁言！！！')
                print('账号休眠' + str(sleeptime) + 's...')
                sleep(sleeptime)
                print('账号休眠完成')
                pass
        except:
            print('账号回复失败，重试')
            sleep(60)
            pass
    n = getnumber(cookies)
    print('账号开始时发表帖子:' + m)
    print('账号结束时发表帖子:' + n)
    print('账号回复' + str(int(n) - int(m)) + '次')

if __name__ == "__main__":
    todaylist = []
    # user = os.environ["USER"]
    # password = os.environ["PASSWORD"]
    cookies =os.environ["COOKIE"]

      
    rcookies=os.environ["RCOOKIE"]

    todaylist =gettodaylist()
    main(cookies, todaylist, rcookies)
    # m = getnumber(cookies)
    # n = 0
    # au = ''
    # geturl, tid = getonelink(todaylist)
    # reply_news = getreply()
    # res = getmatch(geturl)
    # postreply(rcookies, res, reply_news, tid)
