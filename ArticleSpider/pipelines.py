# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    # 同步写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='root', password='', database='article', port=3306,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            INSERT INTO jobble_article(url_object_id,title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s,%s);
        """
        self.cursor.execute(insert_sql,(item['url_object_id'],item['title'],item['url'],item['create_date'],item['fav_nums']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    # 异步写入mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error) # 处理异常

    def handle_error(self,failure):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql = """
            INSERT INTO jobble_article(url_object_id,title,url,create_date,fav_nums) VALUES (%s,%s,%s,%s,%s);
        """
        cursor.execute(insert_sql,(item['url_object_id'],item['title'],item['url'],item['create_date'],item['fav_nums']))


class JsonExporterPipeline(object):
    # 调用scrapy提供的json_export导出json
    def __init__(self):
        self.file = open('articleExport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_file_path = ''
        for (ok, value) in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item
