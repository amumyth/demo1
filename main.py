# -*- coding:UTF-8 -*-
import requests, random, time, collections, window.py
from lxml import etree
from retrying import retry



#生成随机头
def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))],
        #'Cookie': 'ASP.NET_SessionId=qh5rnknn4o1ixayli3chofmw; ValidateToken=d167ec665c2592b00f7e67f68f2f12ac; CurrentSkin=t002; kangle_runat=1'
    }
    return header

class Amazon(object):
    def __init__(self, count):
        self.header = randHeader()
        self.period_count = count
        self.base_url = 'http://www.pkcp58.com/Result/GetLotteryResultList'
        self.dirc = {}
        self.result_dirc = {}
        self.dig_1 = []
        self.dig_2 = []
        self.dig_3 = []
        self.result = []

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        r = requests.get(url, headers=randHeader(),timeout=3)
        #print(r.status_code)
        assert r.status_code == 200
        return r

    def parse_url(self, url):
        try:
            html = self._parse_url(url)
        except:
            html = None
        return html

    def generate_url(self):
        url = []
        url.append(self.base_url)
        url.append('?')
        url.append('gameID=79')
        url.append('&pageSize=')
        url.append(str(self.period_count))
        url.append('&pageIndex=1&startDate=&endDate=&period=&_=')
        url.append(str(int(time.time())) + '000')
        return ''.join(url)

    def go(self):
        while True:
            url = self.generate_url()
            #print('url: ' + url)
            response = self.parse_url(url)
            if response == None:
                print('parse url error')
                return

            self.dirc = eval(response.text)
            for subDirc in self.dirc['list']:
                period = subDirc['date']
                result = subDirc['result']
                self.result_dirc[period] = result
                cnt = len(self.result_dirc)
                if cnt == self.period_count:
                    break

            self.dig_1.clear()
            self.dig_2.clear()
            self.dig_3.clear()
            self.result.clear()
            total = []
            for (period,result) in self.result_dirc.items():
                dig_1 = result.split(',')[4]
                dig_2 = result.split(',')[3]
                dig_3 = result.split(',')[2]
                self.dig_1.append(int(dig_1))
                self.dig_2.append(int(dig_2))
                self.dig_3.append(int(dig_3))
                total.append(int(dig_1))
                total.append(int(dig_2))
                total.append(int(dig_3))

            #self.dig_1.reverse()
            #self.dig_2.reverse()
            #self.dig_3.reverse()

            print(total)
            target = collections.Counter(total).most_common(1)[0][0]

            for i in range(0,10):
                if i != target:
                    self.result.append(i)

            print(self.result)
            time.sleep(5)

if __name__ == '__main__':
    window = window.myWidget()
    #count = 5
    #Amazon(count).go()