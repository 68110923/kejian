import logging

import scrapy

from scrapy_redis.spiders import RedisSpider,RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import Request
from kejian.items import SuNingItem


# class SuningSpider(scrapy.Spider):
class SuningSpider(RedisSpider):
    name = 'suning'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url
    # start_urls = ['https://movie.douban.com/top250']
    redis_key = 'suning'

    def start_requests(self):
        yield Request(
            url='https://movie.douban.com/review/best/',
            # meta={},
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
            },
            errback=self._errback
        )

    def _errback(self, response=None):
        logging.error(f'{"*"*50}errback{response}')

    #默认的请求方法
    def parse(self, response, *args, **kwargs):
        #循环电影的条目
        movie_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')
        for i_itme in movie_list:
            #倒入itme文件
            douban_itme = SuNingItem()
            #解析详情
            douban_itme['serial_number'] = i_itme.xpath('./div/div[1]/em/text()').extract_first()
            douban_itme['movie_name'] =i_itme.xpath('./div/div[2]/div[1]/a/span[1]/text()').extract_first()
            #若遇到不够规范的数据，进行清洗
            jieshao=i_itme.xpath('./div/div[2]/div[2]/p[1]/text()').extract()
            douban_itme['introduce'] = ''.join((''.join(jieshao)).split())
            douban_itme['star'] = i_itme.xpath('./div/div[2]/div[2]/div/span[2]/text()').extract_first()
            douban_itme['evaluate'] = i_itme.xpath('./div/div[2]/div[2]/div/span[4]/text()').extract_first()
            douban_itme['describe'] = i_itme.xpath('./div/div[2]/div[2]/p[2]/span/text()').extract_first()
            yield douban_itme
        #解析下一页规则，提取下一页的xpath
        next_link=response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        #如果下一页为真，把拼接后的url打回self.parse
        # if next_link:
        #     next_link=next_link[0]
        #     yield scrapy.Request('https://movie.douban.com/top250'+next_link,callback=self.parse)



if __name__ == '__main__':
    from scrapy import cmdline

    # 跑程序
    cmdline.execute('scrapy runspider suning.py'.split())