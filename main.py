from scrapy import cmdline

# 跑程序
cmdline.execute('scrapy crawl suning'.split())

# 保存爬取的东西到json
#cmdline.execute('scrapy crawl douban_spider -o ../json/豆瓣top250.csv'.split())