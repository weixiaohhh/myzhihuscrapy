# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class ZhihuspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        
        
        
from  random  import choice
import scrapy
import logging
import urllib2
import re
import requests
from bs4 import BeautifulSoup as bs
# def get_ip():
    # url = 'http://www.xicidaili.com/'
    # headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    # res = requests.get(url, headers=headers)
    # proxy_list = []
    # soup = bs(res.text,'lxml')
    # for i in range(1, 5):
        # ip = soup.find_all('tr',{'class':'odd'})[i].find_all("td")[1].text
        # port = soup.find_all('tr',{'class':'odd'})[i].find_all("td")[2].text
        # proxy_list.append(str(ip)+':'+str(port))
    # return proxy_list
class proxMiddleware(object):

    def __init__(self):
        # self.ip_url = 'http://api.xicidaili.com/free2016.txt'
        # self.info = urllib2.urlopen(self.ip_url).read()
        # self.proxy_list = re.sub(r'\r\n',',',self.info).split(',')
        self.proxy_list = [
        '118.76.191.70:80',
        '221.204.137.185:9797',
        '121.30.197.38:8080',
        '61.152.81.193:9100',
        '116.226.101.93:9999',
        '117.143.109.138:80',
        '117.143.109.138:80',
        '111.13.2.138:80',
        '119.57.105.224:8080'
        ]


    
    def test_proxy(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',\
    'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
        while 1:
            try:
                proxy = choice(self.proxy_list)
                proxies = {'http':proxy}
                test = requests.get('http://www.zhihu.com',proxies=proxies,headers=headers,timeout=5)
                print test.status_code
                if test.status_code == 200:
                    ip = proxy
                    print '{} is over test'.format(ip)
                    break
                else:
                    self.proxy_list.remove(proxy)
                    print '{} is remove'.format(proxy)
            except (requests.exceptions.ReadTimeout ,requests.exceptions.ConnectTimeout) as e:
                print e 
                self.proxy_list.remove(proxy)
                print '{} is remove'.format(proxy)

        return ip
    
    def add_proxy(self):
        # 随机爬取某个城市
        url = 'http://www.66ip.cn/areaindex_{}/1.html'.format(choice(range(1,10)))
        print url
        proxy = self.test_proxy()
        res = requests.get(url, proxies=proxy,timeout=5)
        soup = bs(res.text,'lxml')
        # 爬取第一个IP代理
        for i in range(1, 2):
            ip = soup.find_all('div',{'class':'footer'})[0].find_all('tr')[i].td.text
            port = soup.find_all('div',{'class':'footer'})[0].find_all('tr')[i].td.next_sibling.text
            #ip = soup.find_all('tr',{'class':'odd'})[i].find_all("td")[1].text  西刺解析
            # port = soup.find_all('tr',{'class':'odd'})[i].find_all("td")[2].text
            address = str(ip)+':'+str(port)

            if address not in self.proxy_list:
                self.proxy_list.append(str(ip)+':'+str(port))
                print '{} is storing in list'.format(address)
        return proxy
    
    def process_request(self,request,spider):
        # if not request.meta['proxies']:

        # 测试成功的随机代理爬取 66ip 网站，并且增加到proxy_list,返回测试成功的IP
        ip = self.add_proxy()
        print '{} is using'.format(ip)
        #print 'ip=' %ip
        request.meta['proxy'] = ip
