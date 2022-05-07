import requests
import re
import random
import onetimepass as otp
from time import sleep
import os
#from getver import GetVerificationCode
from multiprocessing import Pool
import config
import pickle


class Autoreply:
    result = None
    over = False
    flag = False
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    loginurl = 'http://t66y.com/login.php'
    url = 'http://t66y.com/thread0806.php?fid=7&search=today'
    headers = {
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/index.php',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': UserAgent
    }
    headers1 = {
        'Host': 't66y.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://t66y.com/login.php',
        'User-Agent': UserAgent
    }

    def __init__(self, user, password, secret):
        self.user = user
        self.password = password
        self.secret = secret
        self.s = requests.Session()

    def login1(self):
        sleep(2)
        Err = None
        data = {
            'pwuser': self.user,
            'pwpwd': self.password,
            'hideid': '0',
            'cktime': '0',
            'forward': 'http://t66y.com/post.php?',
            'jumpurl': 'http://t66y.com/post.php?',
            'step': '2'
        }
        login = self.s.post(self.loginurl, headers=self.headers, data=data)
        if login.content.decode('gbk', 'ignore').find('登录尝试次数过多') != -1:
            login = login.content.decode('gbk', 'ignore')
        else:
            login = login.content.decode('utf-8', 'ignore')
        if login.find('登录尝试次数过多') != -1:
            Err = '登录尝试次数过多,需输入验证码'
            return Err
        elif login.find('賬號已開啟兩步驗證') != -1:
            Err = '賬號已開啟兩步驗證'
            return Err

    def login2(self):
        sleep(2)
        my_token = self.secret
        print(my_token)
        data = {
            'step': '2',
            'cktime': '0',
            'oneCode': str(my_token)
        }
        login = self.s.post(self.loginurl, headers=self.headers, data=data)
        with open(f"./{self.user}", 'wb') as f:
            pickle.dump(login.cookies, f)
        self.cookies = login.cookies
        login = login.content.decode('utf-8', 'ignore')
        if login.find('您已經順利登錄') != -1:
            res = '已經順利登錄'
            self.s.close()
            return res

    def updateCookies(self, cookie):
        self.s.cookies.update(cookie)
        self.cookies = self.s.cookies

    def verifyLoginSuc(self):
        with self.s as s:
            index = s.get('http://t66y.com/index.php', headers={
                'Host': 't66y.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.UserAgent
            })
            index = index.content.decode('utf-8', 'ignore')
            if index.find('上次登錄時間') != -1:
                print('cookie有效登录')
                return True
            print('cookie无效登录, 切换为密码登录')
            return False

    def getcookies(self):
        return self.cookies

    def getverwebp(self):
        code = random.uniform(0, 1)
        code = round(code, 16)
        vercodeurl = 'http://t66y.com/require/codeimg.php?' + str(code)
        image = self.s.get(vercodeurl, headers=self.headers1)
        f = open('image.webp', 'wb')
        f.write(image.content)
        f.close()

    def inputvercode(self, vercode):
        sleep(2)
        vercode = vercode
        data = {
            'validate': vercode
        }
        login = self.s.post(self.loginurl, data=data, headers=self.headers1)
        login = login.content.decode('utf-8', 'ignore')
        if login.find('驗證碼不正確') != -1:
            Err = '验证码不正确，请重新输入'
            return Err

    def gettodaylist(self):
                black_list = []
        pat = ('htm_data/\w+/\w+/\w+.html')
        # con = requests.get(url, headers=headers,params=prams)
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}
        # 头部请求 通过 header 伪装成浏览器
        request = urllib.request.Request(url, headers=head, )  # method="get"
        # 把请求的信息通过urllib Request 封装给 自定义变量request 可以添加参数 method 默认get也可以post
        # print(resqust)
        response = urllib.request.urlopen(request)
        # 通过urlopen访问变量requst 并返回给 自定义参数
        con = response.read().decode("utf-8")
        # print(con)
        web_page = con
        theme = con.find('普通主題')
        #
        match = re.findall(pat, con[theme:])
        # self.match = match

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


    def getModerator(self):
        moderator = self.web_page.find('版主')
        moderator = self.web_page[moderator:moderator + 800]
        pat = 'username=(\w+)'
        moderator_list = re.findall(pat, moderator)
        print('版主列表:' + ','.join(moderator_list))
        self.moderator_list = moderator_list

    @staticmethod
    def getonelink(todaylist):
        geturl = ''
        m = random.randint(0, len(todaylist) - 1)
        geturl = 'http://t66y.com/' + todaylist[m]
        tid = todaylist[m][16:len(todaylist[m]) - 5]
        todaylist.remove(todaylist[m])
        # print('请求链接是: '+geturl)
        return geturl, tid

    @staticmethod
    def browse(geturl, cookies):
        headers = {
            'Host': 't66y.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://t66y.com/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': Autoreply.UserAgent
        }
        res = requests.get(url=geturl, headers=headers, cookies=cookies)

    @staticmethod
    def getmatch(geturl, cookies):
        headers = {
            'Host': 't66y.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://t66y.com/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': Autoreply.UserAgent
        }
        sleep(2)
        get = requests.get(geturl, headers=headers, cookies=cookies)
        sleep(2)
        get = get.content.decode('utf-8', 'ignore')
        pat = '<b>本頁主題:</b> .*</td>'
        res = re.search(pat, get)
        res = res.group(0).replace('<b>本頁主題:</b> ', '').replace('</td>', '')
        res = 'Re:' + res
        return res

    @staticmethod
    def getreply():
        # 自定义回复内容，记得修改随机数
        #         reply=['1024感谢分享','1024感谢你的分享','1024谢谢分享','1024多谢分享','1024感谢作者的分享','1024谢谢坛友分享','1024内容精彩','1024的确如此','1024感谢分享','1024涨知识了','1024很有意思']
        #         reply_m=random.randint(0,len(reply)-1)
        reply_news = "1024"
        print('本次回复消息是:' + reply_news)
        return reply_news

    @staticmethod
    def postreply(cookies, res, reply_news, tid):
        headers = {
            'Host': 't66y.com',
            'Origin': 'null',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': Autoreply.UserAgent
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
            'verify': 'verify'
        }
        post = requests.post(posturl, data=data, headers=headers, cookies=cookies)
        post = post.content.decode('utf-8', 'ignore')
        if post.find('發貼完畢點擊') != -1:
            status = '回复成功'
            return status
        if post.find('所屬的用戶組') != -1:
            status = '今日已达上限'
            return status

    @staticmethod
    def getnumber(cookies):
        indexurl = 'http://t66y.com/index.php'
        headers = {
            'Host': 't66y.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://t66y.com/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': Autoreply.UserAgent
        }
        sleep(2)
        index = requests.get(indexurl, headers=headers, cookies=cookies)
        index = index.content.decode('utf-8', 'ignore')
        pat = '共發表帖子: \d{1,5}'
        num = re.search(pat, index).group(0)
        num = num.replace('共發表帖子: ', '')
        return num

    @staticmethod
    def main(cookieslist, todaylist, ge):
        # 回复
        n = 0
        cookies = cookieslist[ge]
        m = Autoreply.getnumber(cookies)
        suc = False
        print('第' + str(ge + 1) + '个账号开始时发表帖子:' + m)
        while n < 10 and suc is False:
            try:
                au = ''
                print('第' + str(ge + 1) + '个账号当前在回复第' + str(n + 1) + '个。')
                geturl, tid = Autoreply.getonelink(todaylist)
                reply_news = Autoreply.getreply()
                res = Autoreply.getmatch(geturl, cookies)
                sleeptime = random.randint(1048, 2048)
                au = Autoreply.postreply(cookies, res, reply_news, tid)
                if au == '回复成功':
                    print('第' + str(ge + 1) + '个账号回复成功')
                    n = n + 1
                    print('第' + str(ge + 1) + '个账号休眠' + str(sleeptime) + 's...')
                    Autoreply.browse(geturl, cookies)
                    sleep(sleeptime)
                    print('第' + str(ge + 1) + '个账号休眠完成')
                elif au == '今日已达上限':
                    print('第' + str(ge + 1) + '个账号回复失败，今日次数已达10次')
                    suc = True
                else:
                    print('第' + str(ge + 1) + '个账号1024限制或者被禁言！！！')
                    print('第' + str(ge + 1) + '个账号休眠' + str(sleeptime) + 's...')
                    sleep(sleeptime)
                    print('第' + str(ge + 1) + '个账号休眠完成')
            except:
                print('第' + str(ge + 1) + '个账号回复失败，重试')
                sleep(60)
        n = Autoreply.getnumber(cookies)
        print('第' + str(ge + 1) + '个账号开始时发表帖子:' + m)
        print('第' + str(ge + 1) + '个账号结束时发表帖子:' + n)
        print('第' + str(ge + 1) + '个账号回复' + str(int(n) - int(m)) + '次')


if __name__ == "__main__":
    n = 0
    cookieslist = []
    todaylist = []
    user = os.environ["USER"]
    password = os.environ["PASSWORD"]
    secret = os.environ["SECRET"]

    userlist = user.split()
    passwordlist = password.split()
    secretlist = secret.split()




    cookies = "cookie: PHPSESSID=4gvkksn0pig268s7gut5rgf8q5; 227c9_ck_info=/	; 227c9_winduser=C1cHAVBTbwBRUVdSBlRVXFcHXlZWCQdTUAZdAlRVUAcAAAJTW1pSMAcDAgJdAAMCBlBfBVEEW1ABX1ADUAUHU1RRAg5SVFNX; 227c9_groupid=8"
    cookieslist.append(cookies)

    print('cookies获取完成')
    todaylist = Autoreply.gettodaylist()
    p = Pool(len(userlist))
    for i in range(len(userlist)):
        res = p.apply_async(Autoreply.main, args=[cookieslist, todaylist, i])
        print('第', str(i + 1), '个进程启动.。。')
    p.close()
    p.join()
    print(res.get())  # 查看错误信息
    print('完成')
