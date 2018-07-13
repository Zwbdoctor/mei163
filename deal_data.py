# error  warning info: Ignoring response
import time
import re

def err():
    f = open('/home/zwb/Documents/python_work/spider_pro/mei163/mei/yoka.log', 'r')
    i = 1
    while True:
        data = f.readline()
        if not data:
            break
        if 'ERROR' in data:
            url = re.search(r'<GET\shttp://(.*?)>', data).group(1)
            url = 'http://%s' % url
            print(url)
        print(i)
        i += 1
    f.close()


def rd():
    f = open('yoka.log', 'r')
    while True:
        data = f.readline()
        if not data:
            break
        print data
        time.sleep(0.5)
    f.close()


rd()