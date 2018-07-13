import requests
import random
import time
from requests.auth import HTTPProxyAuth


class Image(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN, zh; q=0.9',
            # 'Connection': 'keep-alive',
            'Host': 'beauty.nosdn.127.net',
            'User-Agent': None
        }
        self.ua_pool = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"

        ]
        self.curent = int(time.time())
        proxyMeta = "http://http-dyn.abuyun.com:9020"
        self.proxyUser = "H15EK0717042RY6D"
        self.proxyPass = "077EE9B65130A2BF"
        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

    def get_img(self, url):
        self.headers['User-Agent'] = random.choice(self.ua_pool)
        s = requests.session()
        s.proxies = self.proxies
        s.auth = HTTPProxyAuth(self.proxyUser, self.proxyPass)
        if url.startswith('https'):
            url = "http://" + url[8:]
            self.headers['x-crawlera-use-https'] = "1"
        s.headers = self.headers

        # delay
        # start = time.time()
        # dur = start - self.curent
        # if start - self.curent < 0.3:
        #     time.sleep(dur)

        try:
            data = s.get(url, timeout=15).content
            # self.curent = start
            return data
        except Exception as e:
            print e
            return False
        finally:
            s.close()

    def save(self, id, count, img):
        filename = '/home/zwb/Documents/python_work/spider_pro/mei163/mei/imgs/%s-%s.jpeg' % (id, count)
        with open(filename, 'w') as f:
            f.write(img)

    def get_urls(self):
        with open('product_v2.csv', 'r') as f:
            data = f.readlines()
        us = []
        for each in data:
            each = each.replace('\r\n', '').replace('"', '').split(',')
            if each[1] == 'NULL':
                continue
            imgId = each[0]
            urls = [e.replace('thumbnail=140y140', 'thumbnail=840x730') for e in each[1:]]
            us.append((imgId, urls))
        return us

    def run(self, m=None, n=None):
        a = self.get_urls()
        for e in a:
            uid, urls = e[0], e[1]
            if int(uid) <= m:
                continue
            for count, url in enumerate(urls, 1):
                if count <= n:
                    continue
                img = self.get_img(url)
                i = 0
                while not img:
                    if i < 3:
                        time.sleep(0.1)
                        img = self.get_img(url)
                        print 'retry %s times' % i
                        i += 1
                    else:
                        break
                time.sleep(0.2)
                self.save(uid, count, img)
                print '%s-%s/%s' % (uid, count, len(a))
            n = 0
        m = 0
        print 'done!'
        return True

    def schedule(self):
        res, mm, nn = self.run(m=541, n=5)
        while not res:
            res, mm, nn = self.run(m=int(mm)-1, n=nn)


if __name__ == '__main__':
    imgs = Image()
    res = imgs.run(m=23829, n=6)
    # while not res:
    #     res, mm, nn = imgs.run(m=int(mm)-1, n=nn)
    # imgs.get_urls()
    #  399 2

