# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymysql
from scrapy import settings


class KejianPipeline(object):
    def process_item(self, item, spider):
        return item


class SuNingPipeline(object):
    """
    同步插入数据库
    """

    @classmethod
    def from_crawler(cls, crawler):
        db_name = crawler.settings.get('DB_SETTINGS')
        db_params: dict = db_name.get('suning')
        cls.connect = pymysql.connect(**db_params)
        cls.cursor = cls.connect.cursor()
        logging.info('数据库连接成功')

    def process_item(self, item, spider):
        if not item.get('table_name'):
            raise Exception('必须要传表名table_name和字段名table_fields，表名或者字段名不能为空')
        keys = item.keys()
        values = item.vales()
        insert_sql = 'insert into %s (%s) values (%s)' % (item.get('table_name'), keys, values)
        try:
            self.cursor.execute(insert_sql)
            logging.info("数据插入成功 => " + '1')
        except Exception as e:
            logging.error("执行sql异常 => " + str(e))
            pass
        finally:
            # 要提交，不提交无法保存到数据库
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()
        self.cursor.close()
